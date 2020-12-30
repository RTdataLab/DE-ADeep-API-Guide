# Airdeep.DeviceEntityGroup Rest API
## 선행 조건
  - JWT Token 발급
  
## Host Name
http://mobideep.co.kr:8080

## Save Device Endpoint
**http://mobideep.co.kr:8080/api/device**

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
    "name":"DEVICE_05"
}
```

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **String** |  | Device Name ( Can be replaced with mac address)

## Response body
```
{
  "id": {
    "entityType": "DEVICE",
    "id": "[DEVICE_ID]"
  },
  "createdTime": 1609224613084,
  "additionalInfo": null,
  "tenantId": {
    "entityType": "TENANT",
    "id": ""
  },
  "customerId": {
    "entityType": "CUSTOMER",
    "id": ""
  },
  "name": "DEVICE_05",
  "type": "default",
  "label": null,
  "deviceProfileId": {
    "entityType": "DEVICE_PROFILE",
    "id": ""
  },
  "deviceData": {
    "configuration": {
      "type": "DEFAULT"
    },
    "transportConfiguration": {
      "type": "DEFAULT"
    }
  },
  "ownerId": {
    "entityType": "CUSTOMER",
    "id": ""
  }
}
```

## Python Example

```
import requests
import json

HOST = "http://admin.mobideep.co.kr:8080"
DEVICE_REGISTER_ENDPOINT    = "/api/device"
entityGroupId="" # Device entity group에서 필터된 entityGroupId
deviceName="" # 등록할 device명 (고유값임)

headers = {
        "content-type":"application/json"
       ,"x-authorization": "Bearer "+jwtToken
    }

    payload = {
        "name":deviceName
    }
response = requests.request("POST", (HOST+DEVICE_REGISTER_ENDPOINT)+"?entityGroupId="+entityGroupId, data=payload.replace("device", name), headers=headers)

# 등록된 Device id
print(response.json().get("id").get("id"))
```




