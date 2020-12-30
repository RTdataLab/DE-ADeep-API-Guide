# Airdeep.DeviceEntityGroup Rest API

## Host Name
http://mobideep.co.kr:8080

## Get Device Credentials Endpoint
**http://mobideep.co.kr:8080/api/device/{deviceId}**

## Authorization
- **X-Authorization**
  
## HTTP Request Headers
```
{
  "Content-Type": "application/json"
  "Accept": "*/*",
  "X-Authorization": "Bearer [JWTtoken]"
}
```

## Request Method
GET

## Request Body
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**deviceId** | **str**| path parameter |

## Response body
```
{
  "id": {
    "id": "[ID]"
  },
  "createdTime": 1609224613087,
  "deviceId": {
    "entityType": "DEVICE",
    "id": "[DEVICE_ID]"
  },
  "credentialsType": "ACCESS_TOKEN",
  "credentialsId": "[DEVICE_ACCESS_TOKEN]",
  "credentialsValue": null
}
```

## Python Example

```
import requests
import json

HOST = "http://admin.mobideep.co.kr:8080"
DEVICE_CREDENTIALS_ENDPOINT = "/api/device/{deviceId}"
deviceId ="" # Device 등록후 조회된 device uuid


headers = {
        "content-type":"application/json"
       ,"x-authorization": "Bearer "+jwtToken
    }
response = requests.request("GET", (HOST+DEVICE_CREDENTIALS_ENDPOINT).replace("{deviceId}", deviceId), headers=headers)

# Device credentialsId, 향후 데이터 없로드 또는 속성변경시 필요한 access 토큰임으로 로클저장소에 저장해서 향후 사용가능함
print("getDeviceCredentials", response.json().get("credentialsId"))
```




