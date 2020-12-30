from __future__ import division
import paho.mqtt.client as mqtt
import random
import time
from datetime import datetime
import threading
import json

import login
import provisioning

# Host Information
MOBIDEEP_HOST = "admin.mobideep.co.kr"
MOBIDEEP_HTTP_HOST = "http://admin.mobideep.co.kr:8080"
MQTT_PORT = 1883
ATTRIBUTES_TOPIC = "v1/devices/me/attributes"
ATTRIBUTES_REQUEST_TOPIC = "v1/devices/me/attributes/request/1"
ATTRIBUTES_RESPONSE_TOPIC = ATTRIBUTES_REQUEST_TOPIC.replace("request", "response")
TELEMETRY_TOPIC ="v1/devices/me/telemetry"
RPC_REQUEST_TOPIC ="v1/devices/me/rpc/request/+"
RPC_RESPONSE_TOPIC ="v1/devices/me/rpc/response/"


# User Information
username = ""
password = ""

# Device Information
DEVICE_NAME = ""
DEVICE_ENTITY_GROUP_NAME = ""
credentialsId = ""
uploadFrequency = 1 # Data upload frequency is 1, it can be changed from server

# Get device device entity group id from user
DEVICE_ENTITY_GROUP_ID = input("Please write \033[93mdevice entity group id\033[0m: ")

# Get device name from user (Device name should be in form of AIRDEEP + wifi mac address), in case of emulator only device name provided by user is uploaded
while not DEVICE_NAME:
    DEVICE_NAME = input("Please write \033[93mdevice name\033[0m: ")

# Read local persisted device credentialsId
try:
    with open(DEVICE_NAME,'r') as file:
        for line in file:
            credentialsId = line
except:
    print("Can not read file!")

if not credentialsId:
    # Get mobideep username from user
    while not username:
        username = input("Please write \033[93mmobideep username\033[0m: ")
    
    # Get mobideep password from user
    while not password:
        password = input("Please write \033[93mmobideep password\033[0m: ")

    # 1. Login to the mobideep server using login API
    jwtToken = login.login(MOBIDEEP_HTTP_HOST, username, password)
    print("JWT Token : ", jwtToken)

    # 2. Get Device entity groups to register device under this group
    deviceEntityGroups = provisioning.getDeviceEntityGroups(MOBIDEEP_HTTP_HOST, jwtToken)
    for entityGroup in deviceEntityGroups:
        if entityGroup.get("name") == DEVICE_ENTITY_GROUP_NAME:
            DEVICE_ENTITY_GROUP_ID = entityGroup.get("id").get("id")
        elif entityGroup.get("name") == "All":
            DEVICE_ENTITY_GROUP_ID = entityGroup.get("id").get("id")  

    # 3. Register Device to the mobideep server using device register API
    deviceId = provisioning.saveDevice(MOBIDEEP_HTTP_HOST, jwtToken, DEVICE_NAME, DEVICE_ENTITY_GROUP_ID)
    print("Device ID : ", deviceId)

    # 4. Save Device shared attributes to the mobideep server using device register API
    device_shared_attributes = {
        'uploadFrequency': uploadFrequency
    }
    provisioning.saveDeviceSharedAttributes(MOBIDEEP_HTTP_HOST, jwtToken, deviceId, device_shared_attributes)

    # 5. Get Device credentials to upload device attributes and telemetry data
    credentialsId = provisioning.getDeviceCredentials(MOBIDEEP_HTTP_HOST, jwtToken, deviceId)
    print("Device Credentials : ", credentialsId)

    # 6. Persist credentialsId to local or network storages
    with open(DEVICE_NAME, 'w') as file:
        file.write(credentialsId)
        print("Saved Device Credentials to file ", DEVICE_NAME)

# When device is connected to mobideep server
def on_connect(client, userdata, rc, *extra_params):
    print('Connected with result code ' + str(rc))
    # Upload firmware version and serial number as device attribute using 'v1/devices/me/attributes' MQTT topic
    device_client_attributes = {
        'firmwareVersion': 1.0, 'lastBootingTime':datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    }
    client.publish(ATTRIBUTES_TOPIC, json.dumps(device_client_attributes))

    # Subscribe to shared attribute changes on the server side
    client.subscribe(ATTRIBUTES_TOPIC)

    # Publish request for 'appState' client attribute and two shared attributes 'uploadFrequency' and 'latestVersion'
    client.publish(ATTRIBUTES_REQUEST_TOPIC , json.dumps({"clientKeys": "firmwareVersion,lastBootingTime","sharedKeys": "uploadFrequency"}))

    # Subscribe rpc command from mobideep server to device
    client.subscribe(RPC_REQUEST_TOPIC)
    print('Subscribed and published on connection ')

# Execute when message is updated
def on_message(client, userdata, msg):
    print ('Incoming message\nTopic: ' + msg.topic + '\nMessage: ' + str(msg.payload))
    global uploadFrequency

    payload = json.loads(msg.payload)
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
    button_state = {"enabled": False}
    if msg.topic.startswith("v1/devices/me/rpc/request/"):
        requestId = msg.topic[len('v1/devices/me/rpc/request/'):len(msg.topic)]
        
        # 서버에서 특정값을 조회했을때 서버로 전송함
        if payload['method'] == 'getValue':
            print("getvalue request\n")
            client.publish(RPC_RESPONSE_TOPIC+requestId, json.dumps(button_state), 1)
        
        # 서버에서 디바이스에 대한 명령어를 내렸을때는 client에서 작업후 변경 정보 서버로 전송함
        if payload['method'] == 'setValue':
            print("setvalue request\n")
            params = payload['params']
            button_state['enabled'] = params
            #setValue(params)
            client.publish(TELEMETRY_TOPIC, json.dumps(button_state), 1)
        return

# Sensor data
sensor_data = {
    'temperature_value': 0, 'temperature_max_value': 0,'temperature_ts': 0,'temperature_unit':'C', 
    'humidity_value': 0, 'humidity_max_value': 0, 'humidity_ts': 0, 'humidity_unit': "%",
    'co2_value': 0, 'co2_max_value': 0, 'co2_ts': 0, 'co2_unit': "ppm",
    'pm10_value': 0, 'pm10_max_value': 0, 'pm10_ts': 0, 'pm10_unit': "µg/m3", 
    'pm2.5_value': 0, 'pm2.5_max_value': 0, 'pm2.5_ts': 0, 'pm2.5_unit': "µg/m3", 
    'tvoc_value': 0, 'tvoc_max_value': 0, 'tvoc_ts': 0, 'tvoc_unit': "mg/m3",
    'report_reason': 'Report Reason'
}

# Mqtt client
client = mqtt.Client()

# Set device access token
client.username_pw_set(credentialsId)

# Setting callback function on mqtt connection with mobideep server
client.on_connect = on_connect

# Setting callback function on mqtt message update
client.on_message = on_message

# Connect to mobideep server using MQTT port and 60 seconds keepalive interval
client.connect(MOBIDEEP_HOST, MQTT_PORT, 60)

client.loop_start()

try:
    while True:
        # Set sensor data
        sensor_data['temperature_value'] = random.randint(0, 100)
        sensor_data['humidity_value'] = random.randint(0, 100)
        sensor_data['humidity_max_value'] = random.randint(0, 100)
        sensor_data['co2_value'] = random.randint(0, 100)
        sensor_data['co2_max_value'] = random.randint(0, 100)
        sensor_data['pm10_value'] = random.randint(0, 100)
        sensor_data['pm10_max_value'] = random.randint(0, 100)
        sensor_data['pm2.5_value'] = random.randint(0, 100)
        sensor_data['pm2.5_max_value'] = random.randint(0, 100)
        sensor_data['tvoc_value'] = random.randint(0, 100)
        sensor_data['tvoc_max_value'] = random.randint(0, 100)

        sensor_data['temperature_ts'] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        sensor_data['humidity_ts'] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        sensor_data['co2_ts'] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        sensor_data['pm10_ts'] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        sensor_data['pm2.5_ts'] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        sensor_data['tvoc_ts'] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

        # Sending humidity and temperature data to ThingsBoard
        client.publish(TELEMETRY_TOPIC, json.dumps(sensor_data), 1)
        print(uploadFrequency)

        time.sleep(uploadFrequency) 

except KeyboardInterrupt:
    #GPIO.cleanup() 
    pass

client.loop_stop()
client.disconnect()