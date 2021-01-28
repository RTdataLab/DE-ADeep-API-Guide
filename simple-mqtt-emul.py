from __future__ import division
import paho.mqtt.client as mqtt
import random
import time
from datetime import datetime
import threading
import logging
import json

import login
import provisioning

# LOG LEVEL settings
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(module)s - %(lineno)d - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

# Host Information
AIRDEEP_HTTP_HOST = "https://dev-api-airdeep.rtdata.co.kr"
AIRDEEP_MQTT_HOST = "mqtt-airdeep.rtdata.co.kr"
AIRDEEP_MQTT_PORT = 1883

ATTRIBUTES_TOPIC = "v1/devices/me/attributes"
ATTRIBUTES_REQUEST_TOPIC = "v1/devices/me/attributes/request/1"
ATTRIBUTES_RESPONSE_TOPIC = ATTRIBUTES_REQUEST_TOPIC.replace("request", "response")
TELEMETRY_TOPIC ="v1/devices/me/telemetry"
RPC_REQUEST_TOPIC ="v1/devices/me/rpc/request/+"
RPC_RESPONSE_TOPIC ="v1/devices/me/rpc/response/"

#https://slproweb.com/products/Win32OpenSSL.html 설치 해야 할수도 있음 ssl 적용시

# User Information
username = ""
password = ""

# Device Information
DEVICE_NAME = ""
DEVICE_ACCESS_TOKEN = ""

# Device client attribute
uploadFrequency = 1 # Data upload frequency is 1, it can be changed from server

# Get device name from user (Device name should be in form of AIRDEEP + wifi mac address), in case of emulator only device name provided by user is uploaded
while not DEVICE_NAME:
    DEVICE_NAME = input("Please write \033[93mdevice name\033[0m: ")

# Read local persisted device credentialsId
logging.debug("Check device credentials from local file "+DEVICE_NAME)
try:
    with open(DEVICE_NAME,'r') as file:
        data = json.load(file)
        DEVICE_ACCESS_TOKEN     = data.get("msg").get("credentialInfo").get("credentialsId")
        AIRDEEP_MQTT_HOST = data.get("msg").get("connectionInfo").get("host")
        AIRDEEP_MQTT_PORT = data.get("msg").get("connectionInfo").get("port")
except:
    logging.debug("Can not read local file with name "+DEVICE_NAME)


if not DEVICE_ACCESS_TOKEN:
    
    # Get mobideep username from user
    while not username:
        username = input("Please write \033[93mmobideep username\033[0m: ")
    
    # Get mobideep password from user
    while not password:
        password = input("Please write \033[93mmobideep password\033[0m: ")

    provisioning_info = {
        "msgId": "100",
        "msgDate": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "msgDateFormat": "yyyy-MM-dd HH:mm:ssZ",
        "msgType": 100,
        "msg": {
            "auth" : {"username": username,
                    "password": password},
            "device": {
                "id": DEVICE_NAME,
                "attribute": {
                    "shared": { "uploadFrequency": uploadFrequency  },
                    "client": { "lastFirmwareVersion": 2001,
                    "timeZone": "Asia/Seoul",
                    "lastBootingTime" : 50000 }
                }
            }
        }
    }
    
    # 1. Register device with provisioning information
    logging.debug("Provisioning device with name "+DEVICE_NAME)
    device_info = provisioning.provision(AIRDEEP_HTTP_HOST, provisioning_info)

    DEVICE_ACCESS_TOKEN = device_info.get("msg").get("credentialInfo").get("credentialsId")
    AIRDEEP_MQTT_HOST = device_info.get("msg").get("connectionInfo").get("host")
    AIRDEEP_MQTT_PORT = device_info.get("msg").get("connectionInfo").get("port")
    logging.debug(DEVICE_NAME +" is registered with credentialsId "+DEVICE_ACCESS_TOKEN + " to "+AIRDEEP_MQTT_HOST+":"+str(AIRDEEP_MQTT_PORT))

    # 2. Persist device info to local or network storages
    logging.debug("Saving device info to file "+DEVICE_NAME)
    with open(DEVICE_NAME, 'w') as file:
        json.dump(device_info, file)
        logging.debug("Device info is saved successfully to file "+DEVICE_NAME)

# When device is connected to mobideep server
def on_connect(client, userdata, rc, *extra_params):
    logging.debug('Connected with result code ' + str(rc))
    
    # Subscribe to shared attribute changes on the server side
    client.subscribe(ATTRIBUTES_TOPIC)

    # Subscribe rpc command from mobideep server to device
    client.subscribe(RPC_REQUEST_TOPIC)
    
    # Upload firmware version and serial number as device attribute using 'v1/devices/me/attributes' MQTT topic
    device_client_attributes = {'firmwareVersion': 1.0, 'lastBootingTime':0}
    client.publish(ATTRIBUTES_TOPIC, json.dumps(device_client_attributes))

    # Publish request for 'appState' client attribute and two shared attributes 'uploadFrequency' and 'latestVersion'
    client.publish(ATTRIBUTES_REQUEST_TOPIC , json.dumps({"clientKeys": "firmwareVersion,lastBootingTime","sharedKeys": "uploadFrequency"}))
    logging.debug("Subscribed and published on mqtt connection")

# Execute when message is updated
def on_message(client, userdata, msg):
    logging.debug("Incoming message\nTopic: " + msg.topic + "\nMessage: " + str(msg.payload))
    global uploadFrequency

    payload = json.loads(msg.payload)
    #uploadFrequency 변경시 재설정
    if msg.topic == ATTRIBUTES_TOPIC:
        # Process attributes update notification
        if payload["uploadFrequency"] > 0:
            uploadFrequency = payload["uploadFrequency"]
        return
    
    if msg.topic == ATTRIBUTES_RESPONSE_TOPIC:
        if payload["shared"]["uploadFrequency"]  > 0:
            uploadFrequency = payload["shared"]["uploadFrequency"]
        return
    
    # Serverside RCP Controller
    if msg.topic.startswith("v1/devices/me/rpc/request/"):
        requestId = msg.topic[len("v1/devices/me/rpc/request/"):len(msg.topic)]
        
        # LED 밝기 조절 setLEDValue, getLEDValue (0~100) LED on 될때의 전체 밝기의 비율
        # 서버에서 특정값을 조회했을때 서버로 전송함
        if payload["method"] == "getLEDValue":

            #LED 값 서버로 전송
            client.publish(RPC_RESPONSE_TOPIC+requestId, json.dumps({"LEDValue": 10}))
        
        # 서버에서 디바이스에 대한 명령어를 내렸을때는 client에서 작업후 변경 정보 서버로 전송함
        if payload["method"] == "setLEDValue":
            params = payload["params"]
            
            #LED 값 변경 후 서버로 전송
            client.publish(TELEMETRY_TOPIC, json.dumps({"LEDValue": params}))

        # 공장 초기화 factoryReset 장치를 공장 생산 상태로 초기화, 저장된 설정값들 모두 지워짐
        # 서버에서 디바이스에 대한 명령어를 내렸을때는 client에서 작업후 변경 정보 서버로 전송함
        if payload["method"] == "factoryReset":

            #factoryReset 후 서버로 전송
            client.publish(TELEMETRY_TOPIC, json.dumps({"factoryReset": "true"}))

        # 리셋 reset   장치를 재부팅
        # 서버에서 디바이스에 대한 명령어를 내렸을때는 client에서 작업후 변경 정보 서버로 전송함
        if payload["method"] == "reset":
            params = payload["params"]

            #reset 후 서버로 전송
            client.publish(TELEMETRY_TOPIC, json.dumps({"reset": "true"}))

        # 알림 notify 0,1,2,3 부저에서 소리가 나도록 한다. 부저음은 차후 결정
        # 서버에서 디바이스에 대한 명령어를 내렸을때는 client에서 작업후 변경 정보 서버로 전송함
        if payload["method"] == "notify":
            params = payload["params"]

            #notify 후 서버로 전송
            client.publish(TELEMETRY_TOPIC, json.dumps({"notify": params}))


        # BT 기능 turnBT on/off 불루두스 기능을 끄고 켬
        # 서버에서 디바이스에 대한 명령어를 내렸을때는 client에서 작업후 변경 정보 서버로 전송함
        if payload["method"] == "turnBT":
            params = payload["params"]
            
            #on/off 후 서버로 전송
            client.publish(TELEMETRY_TOPIC, json.dumps({"turnBlutooth": params}))

        # Aircondition report getTelemetry 리포트 주기에 상관없이 명령을 받으면, 현재 aircondition을 report 함
        # 서버에서 특정값을 조회했을때 서버로 전송함
        if payload['method'] == 'getTelemetry':
            client.publish(TELEMETRY_TOPIC, json.dumps({"getTelemetry": {
                    'temperature': 0, 'temperature_max': 0,'temperature_unit':'C', 
                    'humidity': 0, 'humidity_max': 0, 'humidity_unit': "%",
                    'co2': 0, 'co2_max': 0, 'co2_unit': "ppm",
                    'pm10': 0, 'pm10_max': 0, 'pm10_unit': "µg/m3", 
                    'pm2.5': 0, 'pm2.5_max': 0, 'pm2.5_unit': "µg/m3", 
                    'tvoc': 0, 'tvoc_max': 0, 'tvoc_unit': "mg/m3",
                    'report_reason': 'Report Reason'
                }})
            )

        return

# Sensor data
sensor_data = {
    'ts' : 0,
    'temp': 0, 'temp_max': 0,'temp_unt':'C', 'temp_ts' : datetime.now().timestamp() * 1000,
    'hmd': 0, 'hmd_max': 0, 'hmd_unt': "%",'hmd_ts' : datetime.now().timestamp() * 1000,
    'co2': 0, 'co2_max': 0, 'co2_unt': "ppm",'co2_ts' : datetime.now().timestamp() * 1000,
    'pm10': 0, 'pm10_max': 0, 'pm10_unt': "µg/m3", 'pm10_ts' : datetime.now().timestamp() * 1000,
    'pm2.5': 0, 'pm2.5_max': 0, 'pm2.5_unt': "µg/m3", 'pm2.5_ts' : datetime.now().timestamp() * 1000,
    'tvoc': 0, 'tvoc_max': 0, 'tvoc_unt': "mg/m3",'tvoc_ts' : datetime.now().timestamp() * 1000,
    'report_rsn': 'Report Reason'
}

# Mqtt client
client = mqtt.Client()

# Set device access token
client.username_pw_set(DEVICE_ACCESS_TOKEN)

# Setting callback function on mqtt connection with mobideep server
client.on_connect = on_connect

# Setting callback function on mqtt message update
client.on_message = on_message

# Connect to mobideep server using MQTT port and 60 seconds keepalive interval
logging.debug("Connecting to  "+AIRDEEP_MQTT_HOST+":"+ str(AIRDEEP_MQTT_PORT)+" using mqtt protocal")
client.connect(AIRDEEP_MQTT_HOST, AIRDEEP_MQTT_PORT)

client.loop_start()

try:
    while True:
        # Set sensor data datetime.datetime.now().timestamp() * 1000
        timestamp_info = provisioning.getUTCTimestamp(AIRDEEP_HTTP_HOST, random.randint(0, 100), "UTC")
        ts = timestamp_info.get("msg").get("timestamp")
        sensor_data['temp'] = random.randint(0, 100)
        sensor_data['temp_ts'] = ts
        sensor_data['hmd'] = random.randint(0, 100)
        sensor_data['hmd_max'] = random.randint(0, 100)
        sensor_data['hmd_ts'] = ts
        sensor_data['co2'] = random.randint(0, 100)
        sensor_data['co2_max'] = random.randint(0, 100)
        sensor_data['co2_ts'] = ts
        sensor_data['pm10'] = random.randint(0, 100)
        sensor_data['pm10_max'] = random.randint(0, 100)
        sensor_data['pm10_ts'] = ts
        sensor_data['pm2.5'] = random.randint(0, 100)
        sensor_data['pm2.5_max'] = random.randint(0, 100)
        sensor_data['pm2.5_ts'] = ts
        sensor_data['tvoc'] = random.randint(0, 100)
        sensor_data['tvoc_max'] = random.randint(0, 100)
        sensor_data['tvoc_ts'] = ts

        # Sending humidity and temperature data to ThingsBoard
        client.publish(TELEMETRY_TOPIC, json.dumps(sensor_data), 1)
        #logging.debug("Uploaded telemetry to   "+AIRDEEP_MQTT_HOST+":"+ str(AIRDEEP_MQTT_PORT)+" using mqtt protocal with payload " + json.dumps(sensor_data))

        time.sleep(uploadFrequency) 

except KeyboardInterrupt:
    #GPIO.cleanup() 
    pass

client.loop_stop()
client.disconnect()