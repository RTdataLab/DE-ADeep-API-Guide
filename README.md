# AirDeep System Integration Document
##  작성 이력
| 날짜 | 내용 | 작성자 |
|:--------|:---------|:-------|
|2020-12-30| - 최초 작성     | 유수던</br>이창주 |
|2021-01-14| - 다이어그램 수정</br> - Device 등록 Wrapper API 추가</br> - Server URL 변경</br>- Time API 추가   | 유수던</br>이창주 |

</br>

## 1. 소개
### 1.1 목적
    본 문서의 내용은 AQS 서비스 연동 엔터페이스를 제공하기 위한 규격이다. 

### 1.2 적용 범위 
     본 문서의 내용은 AQS 서비스 제공 계획의 변경 및 관련 표준 규격의 갱신등에 다라 추후 보완 및 변경 될 수 있다.
     본 문서에서 기술되지 않은 부분에 대한 기능 구현 시 반드시 협의하여 구현하여야 한다.

### 1.3 프로토콜
      - HTTP/1.1
      - TLS 1.2
      - MQTT

### 1.4 용어 정의 및 약어
      - API : Application Program Interface
      - AQS : Air Quality Services
      - REST : Representational State Transfer

****
</br>

## 2. 기본 정보
### 2.1 서버 정보
  | 서버 | URL |   설명 |
  |:-----|:----|:-------|
  |테스트 서버|https://dev-api-airdeep.rtdata.co.kr| 테스트 서버 |
  |상용 서버| https://api-airdeep.rtdata.co.kr | 상용 서버 | 
</br>

****
</br>

## 3.  서비스 연동
### 3.1 서비스 연동 콜 플로우
* 시퀀스 다이어그램
  ```plantuml
  @startuml
   participant "AirDeep[AQS]" order 1
   participant "AirDeep[REST Server]" order 2
   participant "AirDeep[MQTT Server]" order 3
   hide footbox
   group 1. HTTP - 디바이스 등록
     "AirDeep[AQS]" -> "AirDeep[REST Server]" : Device Register
     "AirDeep[AQS]" <- "AirDeep[REST Server]"  : Response( Token, MQTT Host )
   end

   group 2. HTTP - 현재 시간 가져오기
       "AirDeep[AQS]" -> "AirDeep[REST Server]" : Get Current Time
       "AirDeep[AQS]" <- "AirDeep[REST Server]" : Response(time)
       "AirDeep[AQS]" <- "AirDeep[AQS]" : Set Time
   end

   group 3. MQTT - Session Establish, Upload Telemetry Data, RPC
     group 3.1 MQTT - Session
       "AirDeep[AQS]" -> "AirDeep[MQTT Server]" : MQTT Connection
       "AirDeep[AQS]" <- "AirDeep[MQTT Server]" : Ack
     end
     == MQTT Session Established ==
     group 3.2 MQTT - Upload Telemetry Data
       "AirDeep[AQS]" -> "AirDeep[MQTT Server]" : Upload Telemetry Data
       "AirDeep[AQS]" <- "AirDeep[MQTT Server]" : Ack
     end

     group 3.3 MQTT - ATTRIBUTE CHANGED (RPC Command)
       "AirDeep[AQS]" -> "AirDeep[MQTT Server]" : Subscribe - ATTRIBUTE_TOPIC
       "AirDeep[AQS]" <- "AirDeep[MQTT Server]" : Publish Data - CHANGED ATTRIBUTE VALUE
       "AirDeep[AQS]" <- "AirDeep[AQS]" : Update Device Attribute 
     end
     
     == MQTT Session Established ==
   end
  @enduml
  ```

#### [**3.1.2 디바이스 등록**](./docs/DeviceRegister.md)
   - 목적 : 디바이스는 최초 구동시 디바이스 등록 과정을 하여 Access Token 및 MQTT Host 정보를 가져온다.
  
  </br>
#### [**3.1.2 현재 시간 가져오기**](./docs/GetCurrentTime.md)
   - 목적 : 디바이스는 서버 시간 정보를 가져온 후 디바이스에 시간 정보를 셋팅한다.
  
  </br>
#### [**3.1.3 MQTT Connect**](./docs/MqttConnection.md)
   - 목적 : [3.1 디바이스 등록] 과정에서의 얻은 MQTT Host 정보를 바탕으로 MQTT Session 을 수립한다.

  </br>
#### [**3.1.4 Upload Telemetry Data**](./docs/UploadTelemetryData.md)
   - 목적 : 장비는 MQTT Session 수립 후 Telemetry Data 를 서버에 전달한다.

  </br>
#### [**3.1.5 ATTRIBUTE CHANGED (RPC Command)**](./docs/RpcCommand.md)
   - 목적 : 서버는 MQTT Session 으로 장비 제어 메시지를 전달하여, 장비 제어를 한다. 
  
  </br>
### 3.2  서비스 연동 API
- 디바이스는 최초 구동시 디바이스 등록 과정을 하여 Access Token 및 MQTT Host 정보를 가져온다.
- 디바이스는 서버 시간 정보를 가져온 후 디바이스에 시간 정보를 셋팅한다.
- 시퀀스 다이어그램
  ```plantuml
  @startuml
   participant "AirDeep[AQS]" order 1
   participant "AirDeep[REST Server]" order 2
   hide footbox
   group 1. HTTP - 디바이스 등록
     "AirDeep[AQS]" -> "AirDeep[REST Server]" : Device Register
     "AirDeep[AQS]" <- "AirDeep[REST Server]"  : Response( token, mqtt host info )
   end
   group 2. HTTP - 현재 시간 가져오기
       "AirDeep[AQS]" -> "AirDeep[REST Server]" : Get Current Time
       "AirDeep[AQS]" <- "AirDeep[REST Server]" : Response(time)
       "AirDeep[AQS]" <- "AirDeep[AQS]" : Set Time
   end
  @enduml
  ```

  #### 3.2.1 REST API
    | Name | HTTP Method | Request URI | Description |
    |:--------- | :--------- | :--------- | :--------- |
    | [**register**](./docs/DeviceRegister.md) | **POST** | /v1/devices/register | 디비이스   등록하기 위해서 mobideep 서버의 customer 계정으로 로그인 하여 access token, mqtt host 를 조회한다. |
    | [**getCurrentTime**](./docs/GetCurrentTime.md) | **GET** | /v1/infos/time | mobideep   서버의 시간 정보를 가져온다. |
  
</br></br>

### 3.2.2 MQTT API
 - MQTT API 를 사용하기 위해서는 반드시 **디바이스 등록과정** 이 선행 되어야 한다.
 - AQS 디바이스는 **디바이스 등록과정** 을 통해 얻어진 MQTT Host 정보로 MQTT Host 와 MQTT Session Establish 되어야 한다.
 - RPC Command 는 [**공용 ATTRIBUTE**](./docs/DeviceRegister.md) 로 디바이스에 전달된다. 
 - 시퀀스 다이어그램
   ```plantuml
   @startuml
     participant "AirDeep[AQS]" order 1
     participant "AirDeep[MQTT Server]" order 2
     hide footbox
      group 1. MQTT - Connection
      "AirDeep[AQS]" -> "AirDeep[MQTT Server]" : MQTT Connection
      "AirDeep[AQS]" <--> "AirDeep[MQTT Server]"  : Ack
     end
     == MQTT Session Established ==
     group 2. MQTT - Upload Telemetry Data
       "AirDeep[AQS]" -> "AirDeep[MQTT Server]" : Publish Data - TELEMETRY_TOPIC
       "AirDeep[AQS]" <- "AirDeep[MQTT Server]" : Ack
     end
   
     group 3. MQTT - ATTRIBUTE CHANGED (RPC Command)
       "AirDeep[AQS]" -> "AirDeep[MQTT Server]" : Subscribe - ATTRIBUTE_TOPIC
       "AirDeep[AQS]" <- "AirDeep[MQTT Server]" : Publish Data - CHANGED ATTRIBUTE VALUE
       "AirDeep[AQS]" <- "AirDeep[AQS]" : Update Device Attribute 
     end
     == MQTT Session Established ==
   @enduml
   ```

 - MQTT API 리스트 ___(지원 command는 추후 논의 후 기술 예정)___
    | Method | Topic | Description |
    |:------------- |:------------- |:-------------|
    | **Publish to client ATTRIBUTES_TOPIC** | **v1/devices/me/attributes** | client에 대한 속성정보 서버로 전송함 |
    | **Subscribe to ATTRIBUTES_TOPIC** | **v1/devices/me/attributes** | 변경 된 설정 정보를 조회함 |
    | **Publish to ATTRIBUTES_REQUEST_TOPIC** | **v1/devices/me/attributes/request/1** | client에 대한 속성정보 서버로 전송함 |
    | **Subscribe to ATTRIBUTES_REQUEST_TOPIC** | **v1/devices/me/attributes/request/1** |  변경 된 설정 정보를 조회함 |
    | **Publish to RPC_RESPONSE_TOPIC** | **v1/devices/me/rpc/response/{id}** | rpc 명령어 서버로 전송 |
    | **Subscribe to RPC_REQUEST_TOPIC** | **v1/devices/me/rpc/request/+** | 서버로부터 들어오는 rpc 명령어 |
    | **Publish to TELEMETRY_TOPIC** | **v1/devices/me/telemetry** | 서버로 센서 데이터를 전송함 |
</br></br>

***

# *Appendix A. Sample 소스(업데이트 예정)*
- [**Python Sample 소스**](#python-sample-소스)
  - [**필요한 lib**](#필요한-lib)
  - [**소스 파일**](#소스-파일)
  - [**HOST 정보**](#host-정보)
  - [**MQTT Sample 실행 방법**](#mqtt-sample-실행-방법)
  - [**REST Sample 실행 방법**](#rest-sample-실행-방법)

</br>

## Python Sample 소스
## 필요한 lib
  - python 설치 후 필요한 lib 설치해야함

    | Lib | Description |
    | :--- | :--------- |
    | `time` | 해당 thread를 지연하기 위한 |
    | `datetime` | 센서정보 측정된 timestamp |
    | `random` | random 데이터 사용함  |
    | `json` | josn으로 변경 또는 string으로 변경시 사용|
    | `paho.mqtt.client` | mqtt 연동시 사용 |
    | `threading` | threading |

</br>

## 소스 파일
  - Sample 소스로 아래 파일들이 제공된다.
    | File | Description  |
    | :--- | :----------- |
    | `login.py` | username & password으로 mobideep 서버에 로그인하는 모듈 |
    | `provisioning.py` | 디바이스 및 telemetry 데이터 관리 API 모듈 |
    | `mqtt-emul.py` | 디바이스 등록 및 MQTT 연동 후  데이터 전송  |
    | `rest-emul.py` | 디바이스 등록 및 데이터 전송|

## HOST 정보 (**HOST 정보 변경 예정**)
```json
MOBIDEEP_HOST = "mqtt-airdeep.rtdata.co.kr"  
MOBIDEEP_HTTP_HOST = "http://mqtt-airdeep.rtdata.co.kr"
MQTT_PORT= 1883
username = ""# Mobideep 에서 제공한 사용자 아이디
password =""# Mobideep 에서 제공한 사용자 아이디
```

## MQTT Sample 실행 방법

```
python mqtt-emul.py 
```
명령어가 나오는대로 파라미터 입력: username, password, deviceName, entityGroupName

## REST Sample 실행 방법
```
python rest-emul.py 
```
명령어가 나오는대로 파라미터 입력: username, password, deviceName, entityGroupName
