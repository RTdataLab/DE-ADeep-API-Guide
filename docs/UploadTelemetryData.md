# MQTT - Airdeep.UploadTelemetryData 
# 업데이트 예정

## 선행 조건
  - 장치 등록 
  - Access Token (deviceCredentialsId) 발급

## **Protocol**
- MQTT

## Host Name


## Telemetry upload Endpoint


## HTTP Request Headers
```
 업데이트 예정
```

## Request Method
  - POST

## Request Body
```
{

    'deviceId': '[DEVICE-UUID]',
    'msgId': '[MESSAGE-UUID]',
    'msgDate': '2020-11-11T14:54:05.349+09:00',
    'msgDateFormat': 'yyyy-MM-dd HH:mm:ssZ',
    'msgType': 255
    'msg': {
        'company' : 1001,
        'preiod': 60, 'temperature_value': 0, 'temperature_max_value': 0, 'temperature_unit':'C', 
        'humidity_value': 0, 'humidity_max_value': 0,  'humidity_unit': "%",
        'co2_value': 0, 'co2_max_value': 0, 'co2_unit': "ppm",
        'pm10_value': 0, 'pm10_max_value': 0, 'pm10_unit': "µg/m3", 
        'pm2.5_value': 0, 'pm2.5_max_value': 0, 'pm2.5_unit': "µg/m3", 
        'tvoc_value': 0, 'tvoc_max_value': 0, 'tvoc_unit': "mg/m3",
        'report_reason': 'Report Reason'
    }
}
```

 * 각 파라미터 설명

      | 파라미터 | 타입 | 설명 |
      |:--------|:---------|:---------|
      |deviceId| String | 장치의 고유 UUID 값(WIFI MAC) |
      |msgId| String | 메시지 구분을 위한 ID, 응답으로 이 값을 전달한다. |
      |msgDate| Datetime | msgDateFormat 에 따른 메시지 생성 시간 |
      |msgDateFormat| String | msgDate 의 형식을 나타낸다. |
      |msgType| Integer | data 에 포함된 데이터 타입을 나타낸다. <br> ***sensor data: 255***  |
      |msg| String | 위 타입에 따른 데이터 값 |
      |ext| | 확장을 고려하여 사용 예정 |
    <br>


 * msg 값 설명

      | 파라미터 | 타입 | 설명 |
      |:--------|:---------|:---------|
      |company| Integer | company 구분 값 (alticast: 1001) |
      |preiod| Integer | 메시지의 수집 주기 |
      |*_value| Integer | 수집주기에서 마지막 수집된 값 |
      |*_max_value| Integer | 수집주기에서 최대 값 |
      |*_unit| String | value 의 단위 |
    <br>



## Response body
```
no content
```
## Python Example

```
import requests
import json
from datetime import datetime

HOST = "http://admin.mobideep.co.kr:8080"
DEVICE_TELEMETRY_ENDPOINT  = "/api/v1/{deviceCredentialsId}/telemetry"
credentialsId = ""

headers = {
            "content-type":"application/json"
        }

# 올리고 싶은 데이터를 key, value로 upload 가능함   , 기본적으로 key는 다음항목으로 사용하기 권장함 
sensor_data = {

    'deviceId': 'alticast-device-uuid-01',
    'msgId': 'alticast-msg-uuid-01',
    'msgDate': '2020-11-11T14:54:05.349+09:00',
    'msgDateFormat': 'yyyy-MM-dd HH:mm:ssZ',
    'msgType': 255
    'msg': {
        'company' : 1001,
        'preiod': 60, 'temperature_value': 0, 'temperature_max_value': 0, 'temperature_unit':'C', 
        'humidity_value': 0, 'humidity_max_value': 0,  'humidity_unit': "%",
        'co2_value': 0, 'co2_max_value': 0, 'co2_unit': "ppm",
        'pm10_value': 0, 'pm10_max_value': 0, 'pm10_unit': "µg/m3", 
        'pm2.5_value': 0, 'pm2.5_max_value': 0, 'pm2.5_unit': "µg/m3", 
        'tvoc_value': 0, 'tvoc_max_value': 0, 'tvoc_unit': "mg/m3",
        'report_reason': 'Report Reason'
    }
}

response = requests.request("POST", (http_host+DEVICE_TELEMETRY_ENDPOINT).replace("token", credentialsId), data=json.dumps(sensor_data), headers=headers)
print(response.json())
```




