# MQTT - Airdeep.ALL-Collaboration

## **목적**
  - 서버의 제어 명령어를 디바이스이 처리하고, 처리 결과를 서버에 전달한다.


## 선행 조건
  - 장치 등록 
  - AIRDEEP_MQTT_HOST, AIRDEEP_MQTT_PORT # 디바이스 등록시 받은 mqtt host 및 port
  - Access Token (deviceCredentialsId/DEVICE_ACCESS_TOKEN) 발급

## **Protocol**
- MQTT

## **Host Name**
- **개발기 : 장치등록 과정에서 내려온 mqtt host 및 port**

## **Topic**
```
ATTRIBUTES_TOPIC = "v1/devices/me/attributes"
ATTRIBUTES_REQUEST_TOPIC = "v1/devices/me/attributes/request/1"
ATTRIBUTES_RESPONSE_TOPIC = ATTRIBUTES_REQUEST_TOPIC.replace("request", "response")
TELEMETRY_TOPIC ="v1/devices/me/telemetry"
RPC_REQUEST_TOPIC ="v1/devices/me/rpc/request/+"
RPC_RESPONSE_TOPIC ="v1/devices/me/rpc/response/"
```

## Sensor data
```
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
```
## **시퀀스 다이어그램**
 
   ```plantuml
   @startuml
     participant "AirDeep[AQS]" order 1
     participant "AirDeep[MQTT Server]" order 2
     hide footbox
      group 1. MQTT - Connection
      "AirDeep[AQS]" -> "AirDeep[MQTT Server]" : MQTT Connection(AIRDEEP_HTTP_HOST, AIRDEEP_MQTT_PORT, DEVICE_ACCESS_TOKEN)
      "AirDeep[AQS]" <--> "AirDeep[MQTT Server]"  : Ack
     end
     == MQTT Session Established ==
     group 2. MQTT - on_connect
       "AirDeep[AQS]" -> "AirDeep[MQTT Server]" : subscribe(ATTRIBUTES_TOPIC)
       "AirDeep[AQS]" -> "AirDeep[MQTT Server]" : subscribe(RPC_REQUEST_TOPIC) 
       "AirDeep[AQS]" -> "AirDeep[MQTT Server]" : publish(ATTRIBUTES_TOPIC, {'firmwareVersion': 1.0, 'lastBootingTime':0})
       "AirDeep[AQS]" -> "AirDeep[MQTT Server]" : publish(ATTRIBUTES_REQUEST_TOPIC, {"clientKeys": "firmwareVersion,lastBootingTime","sharedKeys": "uploadFrequency"})
     end

     group 3. MQTT - on_message
       "AirDeep[AQS]" <- "AirDeep[MQTT Server]" : publish(msg.topic=ATTRIBUTES_TOPIC, msg.payload)
       "AirDeep[AQS]" <- "AirDeep[AQS]" : [if msg.topic == ATTRIBUTES_TOPIC && payload["uploadFrequency"] > 0] Update local uploadFrequency 
       "AirDeep[AQS]" <- "AirDeep[MQTT Server]" : publish(msg.topic=ATTRIBUTES_RESPONSE_TOPIC, msg.payload)
       "AirDeep[AQS]" <- "AirDeep[AQS]" : [if msg.topic == ATTRIBUTES_RESPONSE_TOPIC && payload["shared"]["uploadFrequency"]  > 0] Update local uploadFrequency 
       "AirDeep[AQS]" <- "AirDeep[MQTT Server]" : publish(msg.topic=RPC_REQUEST_TOPIC", msg.payload)
       "AirDeep[AQS]" -> "AirDeep[MQTT Server]" : [if msg.topic.startswith("v1/devices/me/rpc/request/") && payload["method"] == "getLEDValue"] publish(RPC_RESPONSE_TOPIC+${id}, {"LEDValue": 10})
       "AirDeep[AQS]" <- "AirDeep[AQS]" :  [if msg.topic.startswith("v1/devices/me/rpc/request/") && payload["method"] == "setLEDValue"] Change Device LED with  payload["params"]
       "AirDeep[AQS]" -> "AirDeep[MQTT Server]" : publish(TELEMETRY_TOPIC, {"LEDValue": 10})
       "AirDeep[AQS]" -> "AirDeep[MQTT Server]" : [if msg.topic.startswith("v1/devices/me/rpc/request/") && payload["method"] == "factoryReset"] publish(TELEMETRY_TOPIC, {"factoryReset": "true"})
       "AirDeep[AQS]" <- "AirDeep[AQS]" : refactorDevice (mqtt connection will be terminated)
       "AirDeep[AQS]" -> "AirDeep[MQTT Server]" : [if msg.topic.startswith("v1/devices/me/rpc/request/") && payload["method"] == "reset"] publish(TELEMETRY_TOPIC, {"reset": "true"})
       "AirDeep[AQS]" <- "AirDeep[AQS]" : reset device (mqtt connection will be terminated)
       "AirDeep[AQS]" <- "AirDeep[AQS]" : [if msg.topic.startswith("v1/devices/me/rpc/request/") && payload["method"] == "notify"] notify device 
       "AirDeep[AQS]" -> "AirDeep[MQTT Server]" :  publish(TELEMETRY_TOPIC, {"notify": payload["params"])
       "AirDeep[AQS]" <- "AirDeep[AQS]" : [if msg.topic.startswith("v1/devices/me/rpc/request/") && payload["method"] == "turnBT"] set bluetooth on/off 
       "AirDeep[AQS]" -> "AirDeep[MQTT Server]" :  publish(TELEMETRY_TOPIC, {"turnBlutooth": payload["params"])
       "AirDeep[AQS]" <- "AirDeep[AQS]" : [if msg.topic.startswith("v1/devices/me/rpc/request/") && payload["method"] == "checkUpdate"] TBD
       "AirDeep[AQS]" -> "AirDeep[MQTT Server]" :  [if msg.topic.startswith("v1/devices/me/rpc/request/") && payload["method"] == "getTelemetry"] publish(TELEMETRY_TOPIC, {"getTelemetry": {sensor_data})
     end

     group 4. MQTT - Upload Telemetry Data (with time interval of uploadFrequency)
       "AirDeep[AQS]" -> "AirDeep[MQTT Server]" : Publish Data - (TELEMETRY_TOPIC,{sensor_data}) 
       "AirDeep[AQS]" <- "AirDeep[MQTT Server]" : Ack
     end
     == MQTT Session Established ==
   @enduml
   ```

## **mqtt connect**
- **Python mqtt connection example**
  ```python
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
    AIRDEEP_HTTP_HOST = "https://api-airdeep.rtdata.co.kr"
    AIRDEEP_MQTT_HOST = "mqtt-airdeep.rtdata.co.kr"
    AIRDEEP_MQTT_PORT = 1883

    # Mqtt client
    client = mqtt.Client()

    # Set device access token
    client.username_pw_set(DEVICE_ACCESS_TOKEN)

    # Setting callback function on mqtt connection with airdeep server
    client.on_connect = on_connect

    # Setting callback function on mqtt message update
    client.on_message = on_message

    # Connect to airdeep server using MQTT port and 60 seconds keepalive interval
    logging.debug("Connecting to  "+AIRDEEP_MQTT_HOST+":"+ str(AIRDEEP_MQTT_PORT)+" using mqtt protocal")
    client.connect(AIRDEEP_MQTT_HOST, AIRDEEP_MQTT_PORT)
  ```
## **on_connect**
- **Subscription Topic**
```
ATTRIBUTES_TOPIC = "v1/devices/me/attributes"
RPC_REQUEST_TOPIC ="v1/devices/me/rpc/request/+"
```
- **Publishing Topic**
```
ATTRIBUTES_TOPIC = "v1/devices/me/attributes"
ATTRIBUTES_REQUEST_TOPIC = "v1/devices/me/attributes/request/1"
```
## **Python mqtt on_connect example**
```python
import requests
import json
from datetime import datetime

ATTRIBUTES_TOPIC = "v1/devices/me/attributes"
RPC_REQUEST_TOPIC ="v1/devices/me/rpc/request/+"

ATTRIBUTES_TOPIC = "v1/devices/me/attributes"
ATTRIBUTES_REQUEST_TOPIC = "v1/devices/me/attributes/request/1"

# When device is connected to mobideep server
def on_connect(client, userdata, rc, *extra_params):
    logging.debug('Connected with result code ' + str(rc))
    
    # Subscribe to shared attribute changes on the server side
    client.subscribe(ATTRIBUTES_TOPIC)

    # Subscribe rpc command from mobideep server to device
    client.subscribe(RPC_REQUEST_TOPIC)
    logging.debug("Subscribed to attribute topic "+ATTRIBUTES_TOPIC " and rpc command topic "+ RPC_REQUEST_TOPIC")

    # Upload firmware version and serial number as device attribute using 'v1/devices/me/attributes' MQTT topic
    device_client_attributes = {
        'firmwareVersion': 1.0, 'lastBootingTime':datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "timeZone": "Asia/Seoul"
    }
    client.publish(ATTRIBUTES_TOPIC, json.dumps(device_client_attributes))
    logging.debug("Published client attribute to topic "+ATTRIBUTES_TOPIC)

    # Publish request for 'firmwareVersion' and 'latestVersion' client attribute and shared attributes 'uploadFrequency' 
    client.publish(ATTRIBUTES_REQUEST_TOPIC , json.dumps({"clientKeys": "firmwareVersion,timeZone,lastBootingTime","sharedKeys": "uploadFrequency"}))
  
```
## **on_message**
```
MQTT Message : msg
Topic key : msg.topic  
Topic payload key: msg.payload (string으로 변환하여 사용)
msg.topic 및 msg.payload의 method 및 params 값에 따라서 디바이스에서 작업하여 서버로 변경 값 또는 데이터 publish 해야 함
```  
  명령 | Topic(msg.topic) | Payload(msg.payload) | Description | Notes
  :------------ | :------------ | :------------- | :------------- | :-------------
   Device에서 client, shared 속성 변경시 | **v1/devices/me/attributes/response/1** | **str**| **b'{"client":{"lastBootingTime":"01/27/2021, 00:28:31","firmwareVersion":1.0},"shared":{"uploadFrequency":1}}'** | device의 upload주기 값 재설정: uploadFrequency = msg.payload.shared.uploadFrequency 
   서버에서 shared 속성 변경시 | **v1/devices/me/attributes** | **str**| **b'{"uploadFrequency":2}'** | device의 upload주기 값 재설정: uploadFrequency = msg.payload.uploadFrequency
   LED 발기 조절 정보요청 | **v1/devices/me/rpc/request/${id}** | **str**| **b'{"method":"getLEDValue"}'** | 
   LED 발기 조절 명령 | **v1/devices/me/rpc/request/${id}** | **str**| **b'{"method":"setLEDValue","params":71}'** |
   공장초기화 | **v1/devices/me/rpc/request/${id}** | **str**| **b'{"method":"factoryReset","params":"{}"}'** | 
   리셋 | **v1/devices/me/rpc/request/${id}** | **str**| **b'{"method":"reset","params":"{}"}'** | 
   알람 | **v1/devices/me/rpc/request/${id}** | **str**| **b'{"method":"notify","params":"{1}"}'** | 
   BT 기능 | **v1/devices/me/rpc/request/${id}** | **str**| **b'{"method":"turnBT","params":true}'** | 
   Check update| **v1/devices/me/rpc/request/${id}** | **str**| **b'{"method":"checkUpdate","params":"{}"}'** | 
   Aircondition report | **v1/devices/me/rpc/request/${id}** | **str**| **b'{"method":"getTelemetry","params":"{}"}'** | 

## **Python mqtt on_message example**
```python
import requests
import json
from datetime import datetime

ATTRIBUTES_TOPIC = "v1/devices/me/attributes"
ATTRIBUTES_RESPONSE_TOPIC = "v1/devices/me/attributes/response/1"
RPC_REQUEST_TOPIC ="v1/devices/me/rpc/request/+"
uploadFrequency = 1

# Execute when message is updated
def on_message(client, userdata, msg):
    logging.debug("Incoming message\nTopic: " + msg.topic + "\nMessage: " + str(msg.payload))
    global uploadFrequency

    payload = json.loads(msg.payload)
    # 서버에서 변경했을때
    if msg.topic == ATTRIBUTES_TOPIC:
        # Process attributes update notification
        if payload["uploadFrequency"] > 0:
            uploadFrequency = payload["uploadFrequency"]
        return
    
    if msg.topic == ATTRIBUTES_RESPONSE_TOPIC:
        if payload["shared"]["uploadFrequency"]  > 0:
            uploadFrequency = payload["shared"]["uploadFrequency"]
        return

    # Client에서 변경했을때
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
  ```