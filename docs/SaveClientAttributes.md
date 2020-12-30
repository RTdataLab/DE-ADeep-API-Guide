# Airdeep.DeviceEntityGroup Rest API

## 선행 조건
  - Access Token (deviceCredentialsId) 발급

## Host Name
http://mobideep.co.kr:8080


## Device Attributes
* Client Attributes (clientKeys,  Device 에 대한 속성, 서버에서 변경 불가함)
  - latestFirmwareVersion
  - lastBootingTime

## Save Device Client Attributes Endpoint
**http://mobideep.co.kr:8080/api/v1/{deviceCredentialsId}/attributes**

## HTTP request Headers
```
{
  "Content-Type": "application/json",
  "Accept": "*/*"
}
```

## Request Method
POST

## Request Body

```
{
    'firmwareVersion': 1.0, 
    'lastBootingTime':'2020-01-01'
}
```

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**device_token** | **str**| path parameter | 
**json payload** | **str**| {'firmwareVersion': 1.0, 'lastBootingTime':datetime.now().strftim('%Y-%m-%dT%H:%M:%S')}| 

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
DEVICE_ATTRIBUTES_ENDPOINT  = "/api/v1/{deviceCredentialsId}/attributes"
deviceCredentialsId = ""

headers = {
            "content-type":"application/json"
    }

# 기본적인 device 정보를 key, value 로 등록 또는 수정 가능하며, 다음 2개는 기본으로 등록 권장함
device_client_attributes = {
    'firmwareVersion': 1.0, 'lastBootingTime':datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
}

response = requests.request("POST", (HOST+DEVICE_ATTRIBUTES_ENDPOINT).replace("{deviceCredentialsId}", deviceCredentialsId)+"?entityGroupId="+entityGroupId, data=json.dumps(device_client_attributes), headers=headers)
print(response.json())
```




