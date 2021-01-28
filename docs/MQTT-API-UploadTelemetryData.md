# MQTT API - Airdeep.RPC Command

## **요약 설명**
  - 단말은 서버로부터 수신된 'uploadFrequency' 를 기준으로 TelemetryData 를 업로드 한다.

## **선행 조건**
  - 장치 등록 
  - 디바이스 등록 과정에서 수신받은 MQTT 호스트 정보
  - Access Token (deviceCredentialsId)

</br>

## **Protocol**
- MQTT

</br>

## **Host Name**
- [디바이스 등록 과정](./HTTP-API-DeviceRegister.md)에서 수신받은 MQTT 호스트 정보

</br>

## **MQTT TOPIC**
NO | TOPIC    | Publish | Subscribe | Description
:------: | :------ | :---------: | :----------: | :----------
1  | v1/devices/me/telemetry  | O | X | **Publish** </br> 서버에 telemetry data 를 전달한다.
2 | v1/devices/me/attributes/request/1 | O | X | **Publish**</br> 서버에 저장된 Attribute(Client, Shard) 값을 요청한다. 
3  | v1/devices/me/attributes/response/1  | X | X | 2번 요청의 응답 값</br> on_message 콜백으로 응답 값이 수신된다. 

</br>

## **Payload**
NO | TOPIC    | Send(Publish) | Recv(on_message)
:------: | :------ | :--------- | :----------
1  | v1/devices/me/telemetry  | O [(Sensor Telemetry)](#Sensor-Telemetry) | X }
2  | v1/devices/me/attributes/response/1  | X | { "firmwareVersion": 5.0,"lastBootingTime": timestamp(sec) },"shared":{"uploadFrequency": 1} }
3  | v1/devices/me/attributes/response/1  | X | { "firmwareVersion": 5.0,"lastBootingTime": timestamp(sec) },"shared":{"uploadFrequency": 1} }
</br>

## Sensor Telemetry
```json
{
    'ts' : 0,
    'temp': 0, 'temp_max': 0,'temp_unt':'C', 'temp_ts' : datetime.now().timestamp()       1000,
    'hmd': 0, 'hmd_max': 0, 'hmd_unt': "%",'hmd_ts' : datetime.now().timestamp() * 000,
    'co2': 0, 'co2_max': 0, 'co2_unt': "ppm",'co2_ts' : datetime.now().timestamp()       1000,
    'pm10': 0, 'pm10_max': 0, 'pm10_unt': "µg/m3", 'pm10_ts' : datetime.now().imestamp     () *     1000,
    'pm2.5': 0, 'pm2.5_max': 0, 'pm2.5_unt': "µg/m3", 'pm2.5_ts' : datetime.now()     timestamp    () * 1000,
    'tvoc': 0, 'tvoc_max': 0, 'tvoc_unt': "mg/m3",'tvoc_ts' : datetime.now().imestamp()      *     1000,
    'report_rsn': 'Report Reason'
}
```


## **Payload 설명**
Key        |  Value | Description 
:----------|:-----------------|:------------------
ts| Unix timestamp(Sec) | json 을 구성하여 데이터를 전달한 시간 
xxxx_ts| Unix timestamp(Sec) | 센서를 수집한 시간
xxxx_unit| mg/m3 | 센서 값 단위 
report_rsn| Report Reason | 전송 이유(주기적 수집, 요청에 의한 OneShot 수집 전달 | 없음


</br>

## **시퀀스 다이어그램**

1. TelemetryData 업로드
    - 장비 업데이트 후 펌웨어 값 전달
   ```plantuml
   @startuml
     participant "AirDeep[AQS]" order 1
     participant "AirDeep[MQTT Server]" order 2
     hide footbox

     group 1. MQTT - Connection
      "AirDeep[AQS]" -> "AirDeep[MQTT Server]" : MQTT Connection(MQTT_HOST, MQTT_PORT, ACCESS_TOKEN(deviceCredentialsId))
      "AirDeep[AQS]" <- "AirDeep[MQTT Server]"  : Ack(Connected)
     end

     == MQTT Session Established ==
     group 2. MQTT - 서버의 uploadFrequency Attribute 값 설정 
     "AirDeep[AQS]" -> "AirDeep[MQTT Server]" : 1.1) Publish - ATTRIBUTES_REQUEST_TOPIC(서버에 저장된 Attribute(Client, Shard) 값 요청)
     "AirDeep[AQS]" <- "AirDeep[MQTT Server]" : 1.2) ATTRIBUTES_RESPONSE_TOPIC( Receive Attribute (Client(firmwareVersion, lastBootingTime), Shard(uploadFrequency)) )
     "AirDeep[AQS]" <- "AirDeep[AQS]" : 1.3 on_message
     note left: uploadFrequency 설정
     end

     group 3. MQTT - Upload Telemetry Data
       "AirDeep[AQS]" -> "AirDeep[MQTT Server]" : 2.1) Publish Data - (TELEMETRY_TOPIC) 
     end
     
     == MQTT Session Established ==
   @enduml
   ```
</br></br>



## Python Example

```python
import paho.mqtt.client as mqtt
import random
import time
from datetime import datetime
import threading
import logging
import json

AIRDEEP_MQTT_HOST="" # 디바이스 등록시 받은 host
AIRDEEP_MQTT_PORT="" # 디바이스 등록시 받은 port
DEVICE_ACCESS_TOKEN="" # 디바이스 등록시 받은 credentialsId

# Publishing topic
TELEMETRY_TOPIC ="v1/devices/me/telemetry"
ATTRIBUTES_REQUEST_TOPIC = "v1/devices/me/attributes/request/1"
ATTRIBUTES_RESPONSE_TOPIC = "v1/devices/me/attributes/response/1"

# Sensor data
sensor_data = {
    'ts':0,
    'temperature': 0, 'temperature_max': 0,'temperature_unit':'C', 'temperature_ts': 0, 
    'humidity': 0, 'humidity_max': 0, 'humidity_unit': "%", 'humidity_ts': 0, 
    'co2': 0, 'co2_max': 0, 'co2_unit': "ppm", 'co2_ts': 0, 
    'pm10': 0, 'pm10_max': 0, 'pm10_unit': "µg/m3", 'pm10_ts': 0, 
    'pm2.5': 0, 'pm2.5_max': 0, 'pm2.5_unit': "µg/m3", 'pm2.5_ts': 0, 
    'tvoc': 0, 'tvoc_max': 0, 'tvoc_unit': "mg/m3", 'tvoc_ts': 0, 
    'report_reason': 'Report Reason'
}

# Mqtt client
client = mqtt.Client()

# Set device access token
client.username_pw_set(DEVICE_ACCESS_TOKEN)

# Connect to airdeep server using MQTT port and 60 seconds keepalive interval
logging.debug("Connecting to  "+AIRDEEP_MQTT_HOST+":"+ str(AIRDEEP_MQTT_PORT)+" using mqtt protocal")
client.connect(AIRDEEP_MQTT_HOST, AIRDEEP_MQTT_PORT)

client.loop_start()

try:
    while True:
        # Set sensor data
        sensor_data['temperature'] = random.randint(0, 100)
        sensor_data['humidity'] = random.randint(0, 100)
        sensor_data['humidity_max'] = random.randint(0, 100)
        sensor_data['co2'] = random.randint(0, 100)
        sensor_data['co2_max'] = random.randint(0, 100)
        sensor_data['pm10'] = random.randint(0, 100)
        sensor_data['pm10_max'] = random.randint(0, 100)
        sensor_data['pm2.5'] = random.randint(0, 100)
        sensor_data['pm2.5_max'] = random.randint(0, 100)
        sensor_data['tvoc'] = random.randint(0, 100)
        sensor_data['tvoc_max'] = random.randint(0, 100)

        # Sending sensor data to airdeep
        client.publish(TELEMETRY_TOPIC, json.dumps(sensor_data), 1)
        
        time.sleep(uploadFrequency) 

except KeyboardInterrupt:
    #GPIO.cleanup() 
    pass

client.loop_stop()
client.disconnect()
```
 
## **Python Example**
```python
import requests
import json
from datetime import datetime

uploadFrequency = 1

ATTRIBUTES_TOPIC = "v1/devices/me/attributes"
ATTRIBUTES_REQUEST_TOPIC = "v1/devices/me/attributes/request/1"
ATTRIBUTES_RESPONSE_TOPIC = "v1/devices/me/attributes/response/1"

# When device is connected to AirDeep server
def on_connect(client, userdata, rc, *extra_params):

    # 1.1) Attribute(Client, Shared) 값 요청한다.
    client.publish(ATTRIBUTES_REQUEST_TOPIC , json.dumps({"clientKeys": "firmwareVersion,lastBootingTime","sharedKeys": "uploadFrequency"}))

    # 2.1) 서버에서 Device의 Shared Attribute 변경 시, 변경된 값을 받기 위하여 Subscribe 요청.
    client.subscribe(ATTRIBUTES_TOPIC)


def on_message(client, userdata, msg):
    global uploadFrequency

    payload = json.loads(msg.payload)

    # 1.2) 서버로 부터 요청한 Attribute(Client, Shard) 값을 수신한다.
    if msg.topic == ATTRIBUTES_RESPONSE_TOPIC:
        if payload["shared"]["uploadFrequency"]  > 0:
            uploadFrequency = payload["shared"]["uploadFrequency"]
        return

    # 2.2) 서버에서 Shard Attribute 변경 시 수신된다.
    if msg.topic == ATTRIBUTES_TOPIC:
        if payload["uploadFrequency"] > 0:
            uploadFrequency = payload["uploadFrequency"]
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
  ```


