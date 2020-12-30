# Airdeep.DeviceEntityGroup Rest API

## 선행 조건
  - JWT Token 발급
  - deviceId 발급 

## Host Name
http://mobideep.co.kr:8080


## Device Attributes
* Shared Attributes (sharedKeys, Device 또는 Server에서 접근 또는 수정 가능 한 속성)
  - uploadFrequency

## Save Device Shared Attribute Endpoint
**http://mobideep.co.kr:8080/api/plugins/telemetry/DEVICE/{deviceId}/SHARED_SCOPE**

## Authorization
- **X-Authorization**
  
## HTTP Request Headers
```
{
  "Content-Type": "application/json",
  "Accept": "*/*",
  "X-Authorization": "Bearer [JWTtoken]"
}
```

## Request Method
POST

## Request Body

```
{
    'uploadFrequency': 2
}
```

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**deviceId** | **str**| deviceId | 
**json** | **str**| {'uploadFrequency': 1} | 

## Response body
```
{
  "result": {},
  "setOrExpired": true
}
```
## Python Example

```
import requests
import json

HOST = "http://admin.mobideep.co.kr:8080"
DEVICE_SHARED_ATTRIBUTES_ENDPOINT  = "/api/plugins/telemetry/DEVICE/{deviceId}/SHARED_SCOPE"
deviceId = "" # Device 등록후 조회된 device id

headers = {
            "content-type":"application/json"
            ,"x-authorization": "Bearer "+jwtToken
    }

# 데이터 없로드주기는 항상 uploadFrequency 에 초단위로 설정함, 향후 서버 또는 클라이언트에서 수정가능
# 추가적으로 필요한 키도 정의하여 업로드 가능함
device_shared_attributes = {
        'uploadFrequency': 1
    }

response = requests.request("POST", (http_host+DEVICE_SHARED_ATTRIBUTES_ENDPOINT).replace("{deviceId}", deviceId), data=json.dumps(device_shared_attributes), headers=headers)
print(response.json())
```




