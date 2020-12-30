# Airdeep.Login Rest API

## 선행 조건
  - 없음

## Host Name
http://mobideep.co.kr:8080

## Login Endpoint
**http://mobideep.co.kr:8080/api/auth/login**

## HTTP Request Headers
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
{'username': 'username', 'password': 'password'}
```

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**username** | **String** |  | [optional] 
**password** | **Integer** |  | [optional]

## Response body
```
{'token': '[JWT_TOKEN]', 'refreshToken': '[REFRESH_TOKEN]'}
```

## Python Example
```
import requests
import json

HOST = "http://admin.mobideep.co.kr:8080"
LOGIN_ENDPOINT = "/api/auth/login"
username =""
password =""

headers = {"content-type":"application/json"}
payload = {
        "username":username,
        "password":password
    }
response = requests.request("POST", (HOST+LOGIN_ENDPOINT), data=payload, headers=headers)

# jwtToken
print(response.json().get("token"))
```




