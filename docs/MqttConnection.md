# MQTT - Airdeep.RpcCommand 
# 업데이트 예정
## 선행 조건
  - 장치 등록 
  - Access Token (deviceCredentialsId) 발급

## **Protocol**
- MQTT

## **Host Name**
- **개발기 : https://dev-api-airdeep.rtdata.co.kr**
- **상용기 : https://api-airdeep.rtdata.co.kr**

## **Resource Path**
- **/v1/infos/time**

## **Query Parameter**

  Parameter | Type | Description | Notes
  :------------ | :------------- | :------------- | :-------------
  **msgId** | **str**| 메시지 구분을 위한 ID, 응답으로 이 값을 전달한다. | 
  **getTimeByZid** | **str**| Zone ID (기본으로 AirDeep 은 UTC+0 타임을 기준으로 동작한다.) | 
  
### ZONE ID 
  - 기본으로 AirDeep 은 UTC+0 타임을 기준으로 동작한다
  
  Country | Zone-ID | Description | Notes
  :------------ | :------------- | :------------- | :-------------
  **KOREA** | "Asia/Seoul"  | 한국시 | 
  **Greenwich** | "UTC" |  UTC+0 기본으로 AirDeep 은 UTC+0 타임을 기준으로 동작한다. |   
  
  ```
    Example : /v1/infos/time?msgId=msgUUID1234&getTimeByZid=UTC
  ```

## **HTTP Request Headers**
```json
  "Content-Type": "application/json",
  "Accept": "*/*"
```
## **Request Method**
```json
  GET
```

## **Request Body**

```json
  없음
```

* **Request Body 설명**
```json
  없음
```

</br>

## **Response body**
```json
{
    'msgId': '[MESSAGE-UUID]',
    'msgDate': '2020-11-11 14:54:05+0900',
    'msgDateFormat': 'yyyy-MM-dd HH:mm:ssZ',
    'msgType': 501
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
  **msgId** | **str**| 메시지 구분을 위한 ID, 응답으로 이 값을 전달한다. | 
  **msgDate** | **str**| msgDateFormat 에 따른 메시지 생성 시간 | 
  **msgDateFormat** | **str**| msgDate 의 형식을 나타낸다. | 
  **msgType** | **str**| msg 에 포함된 데이터 타입을 나타낸다. | 
  **msg** | **str**| msgType 에 따른 데이터 값. | 
  **msg.zoneId** | **str**| timestamp의 Zone ID  |  
  **msg.timestamp** | **num**| timestamp | 

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