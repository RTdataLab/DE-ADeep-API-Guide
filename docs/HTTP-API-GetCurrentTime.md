# Rest API - Airdeep.GetCurrentTime 

## **선행 조건**
  - 없음
## **Protocol**
- HTTP / TLS
## **Host Name**
- **개발기 : https://dev-api-airdeep.rtdata.co.kr**
- **상용기 : https://api-airdeep.rtdata.co.kr**

## **Request Method**
```json
  GET
```
## **HTTP Request Headers**
```json
  "Content-Type": "application/json",
```

## **Resource Path**
```json
  /v1/infos/time
```

## **Query Parameter**

  Parameter | Type | Description | Notes
  :------------ | :------------- | :------------- | :-------------
  **msgId** | **String**| 메시지 구분을 위한 ID, 응답으로 이 값을 전달한다. | 
  **getTimeByZid** | **String**| Zone ID (기본으로 AirDeep 은 UTC+0 타임을 기준으로 동작한다.) | 
</br>

## ZONE ID 
  - 기본으로 AirDeep 은 UTC+0 타임을 기준으로 동작한다
  
  Country | Zone-ID | Description | Notes
  :------------ | :------------- | :------------- | :-------------
  **KOREA** | "Asia/Seoul"  | 한국시 | 
  **Greenwich** | "UTC" |  UTC+0 기본으로 AirDeep 은 UTC+0 타임을 기준으로 동작한다. |   
</br>


## **Request Body**
```json
  없음
```

* **Request Body 설명**
```json
  없음
```

</br>

## **CURL 예시**
  ```
    curl --location --request GET 'https://dev-api-airdeep.rtdata.co.kr/v1/infos/time?msgId=msgUUID1234&getTimeByZid=UTC' \
--header 'Content-Type: application/json'
  ```

## **Response body**
```json
{
    'msgId': '[MESSAGE-UUID]',
    'msgDate': '2020-11-11 14:54:05+0900',
    'msgDateFormat': 'yyyy-MM-dd HH:mm:ssZ',
    'msgType': 1050
    'msg': {
       'zoneId': "UTC",
       'timestamp': 1610604928
    }
}
```
</br>

* **Response body 설명**
  Name | Type | Description | Notes
  ------------ | ------------- | ------------- | -------------
  **msgId** | **String**| 메시지 구분을 위한 ID, 응답으로 이 값을 전달한다. 
  **msgDate** | **String**| msgDateFormat 에 따른 메시지 생성 시간 
  **msgDateFormat** | **String**| msgDate 의 형식을 나타낸다. 
  **msgType** | **Number**| msg 에 포함된 데이터 타입을 나타낸다. 
  **msg** | **String**| msgType 에 따른 데이터 값. 
  **msg.zoneId** | **String**| timestamp의 Zone ID 
  **msg.timestamp** | **Number**| timestamp (Second)
</br>

* **msgType 설명**
  - json 의 msg 필드가 어떠한 형식의 값인지 나타낸다.

     msgType | Type | Description
     ------------ | ------------- | -------------
     **1050** | **Number**| (Response)time 요청이 정상처리 되어 서버의 time 값을 나타낸다.
     **400** | **Number**| (Rquest) 파라미터 유효성 검사 중 에러
     **404** | **Number**| (Rquest) 서버 로그인 실패
     **500** | **Number**| (Rquest) 서버 내부 로직등의 예외적인 에러
<br/>

## **Python Example(업데이트 예정)**
```python
import requests
import json
from datetime import datetime

HOST = "https://api-airdeep.rtdata.co.kr/v1/infos/time"
credentialsId = ""
sharedKeys = "msgId=msgUUID1234&getTimeByZid=UTC" 

headers = {
            "content-type":"application/json"
        }
response = requests.request("GET", ... , headers=headers)
print(response.json())
```

</br>

## *Appendix. json contens 도식화*

* Request Contents
  ```json
    없음
  ```

* Response Contents
  ```plantuml
  @startjson
  {
    "msgId": "{msg-uuid}",
    "msgDate": "{msgDate}",
    "msgDateFormat": "{msgDateFormat}",
    "msgType": "{msgTypeId}",
    "msg": {
      "zoneId": "{Zone-ID}",
      "timestamp": "{timestamp}"
    }
  }
  @endjson 
  ```