# Airdeep.DeviceEntityGroup Rest API

## 선행 조건
  - JWT Token 발급

## Host Name
http://mobideep.co.kr:8080

## Get Device Entity Groups Endpoint
**http://mobideep.co.kr:8080/api/entityGroups/DEVICE**

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
GET

## Request Body
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------

## Response body
```
[
  {
    "id": {
      "entityType": "ENTITY_GROUP",
      "id": "[DEVICE_ENTITYGROUP_ID]"
    },
    "createdTime": 1608703846432,
    "type": "DEVICE",
    "name": "All",
    "ownerId": {
      "entityType": "CUSTOMER",
      "id": ""
    },
    "additionalInfo": null,
    "configuration": {
      "columns": [
        {
          "type": "ENTITY_FIELD",
          "key": "created_time",
          "sortOrder": "DESC"
        },
        {
          "type": "ENTITY_FIELD",
          "key": "name",
          "sortOrder": "NONE"
        },
        {
          "type": "ENTITY_FIELD",
          "key": "device_profile",
          "sortOrder": "NONE"
        },
        {
          "type": "ENTITY_FIELD",
          "key": "label",
          "sortOrder": "NONE"
        }
      ],
      "settings": {},
      "actions": {}
    },
    "ownerIds": [
      {
        "entityType": "CUSTOMER",
        "id": ""
      },
      {
        "entityType": "TENANT",
        "id": ""
      }
    ],
    "groupAll": true
  },
  {
    "id": {
      "entityType": "ENTITY_GROUP",
      "id": ""
    },
    "createdTime": 1608704802292,
    "type": "DEVICE",
    "name": "DEVICE_GROUP_NAME",
    "ownerId": {
      "entityType": "TENANT",
      "id": ""
    },
    "additionalInfo": {
      "description": ""
    },
    "configuration": {
      "columns": [
        {
          "type": "ENTITY_FIELD",
          "key": "created_time",
          "sortOrder": "DESC"
        },
        {
          "type": "ENTITY_FIELD",
          "key": "name",
          "sortOrder": "NONE"
        },
        {
          "type": "ENTITY_FIELD",
          "key": "device_profile",
          "sortOrder": "NONE"
        },
        {
          "type": "ENTITY_FIELD",
          "key": "label",
          "sortOrder": "NONE"
        }
      ],
      "settings": {},
      "actions": {}
    },
    "ownerIds": [
      {
        "entityType": "TENANT",
        "id": ""
      }
    ],
    "groupAll": false
  }
]
```

## Python Example
```
import requests
import json

HOST = "http://admin.mobideep.co.kr:8080"
DEVICE_ENTITY_GROUPS        = "/api/entityGroups/DEVICE"
jwtToken ="" # 로그인 후 응답으로 받은 토큰값
DEVICE_ENTITY_GROUP_NAME =""# Device 등록할 entity group 명

headers = {
        "content-type":"application/json",
        "x-authorization": "Bearer "+jwtToken
    }
response = requests.request("GET", (HOST+DEVICE_ENTITY_GROUPS), headers=headers)

# DEVICE_ENTITY_GROUP_NAME 없는 경우 All에다 등록
for entityGroup in response.json():
        if entityGroup.get("name") == DEVICE_ENTITY_GROUP_NAME:
            DEVICE_ENTITY_GROUP_ID = entityGroup.get("id").get("id")
        elif entityGroup.get("name") == "All":
            DEVICE_ENTITY_GROUP_ID = entityGroup.get("id").get("id")   
print(response.json())
```




