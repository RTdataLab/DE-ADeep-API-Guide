# Airdeep.DeviceEntityGroup Rest API

## Host Name
http://mobideep.co.kr:8080

## Get Device Attributes Endpoint
**http://mobideep.co.kr:8080/api/v1/{deviceCredentialsId}/attributes**


## Device Attributes
* Client Attributes (clientKeys,  Device 에 대한 속성, 서버에서 변경 불가함)
  - latestFirmwareVersion
  - lastBootingTime
  
* Shared Attributes (sharedKeys, Device 또는 Server에서 접근 또는 수정 가능 한 속성)
  - uploadFrequency

* Server Attributes (serverKeys, Device 에서 접근 불가한 속성 정보, 서버에서만 관리 가능)
  - 필요시 추가
  - 
## HTTP Request Headers
```
{
  "Content-Type": "application/json",
  "Accept": "*/*"
}
```
## Request Method
GET

## Request Body

```
{
    'shared': {'firmwareVersion': 1.0}
}
```

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**device_token** | **str**| path parameter | 
**client_keys** | **str**| clientKeys | [optional] 
**shared_keys** | **str**| sharedKeys | [optional] 



## Response body
Device Attribute List

## Python Example
```
import requests
import json
from datetime import datetime

HOST = "http://admin.mobideep.co.kr:8080"
DEVICE_ATTRIBUTES_ENDPOINT = "/api/v1/{deviceCredentialsId}/attributes"
credentialsId = ""
sharedKeys = "sharedKeys=uploadFrequency" # shared 또는 client 필요한 속성을 조회 함, 여기서는 uploadFrequency 만 조회 함

headers = {
            "content-type":"application/json"
        }
response = requests.request("GET", (HOST+DEVICE_ATTRIBUTES_ENDPOINT).replace("{deviceCredentialsId}", credentialsId) + "?"+sharedKeys, headers=headers)
print(response.json())
```




