# Mobideep System Integration Document
## 작성 이력
##  작성 이력
| 날짜 | 내용 | 작성자 |
|:--------|:---------|:-------|
|2020-12-30| 최초 작성     | 유수던</br>이창주 |
|          |             |      |
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
  |테스트 서버|https://admin.mobideep.co.kr:8080| 테스트 서버의 URL | 
  |상용 서버| 추후 기술 예정 | 상용 서버의 URL | 
</br>

### 2.2 속성 설정 정보
  | 설정키 | 목적 | 공용(서버/장비) | 장비 | 
  |:-----|:----|:----:|:----:|
  | uploadFrequency | 데이터 업로드 주기를 설정한다.| O | O |
  | lastFirmwareVersion | 장비의 현재 펌웨어 버전을 기록한다. | X | O |
  | lastBootingTime | 마지막 구동 시간을 기록한다. | X | O |
</br>

****
</br>

## 3.  서비스 연동
### 3.1 서비스 연동 콜 플로우
1. 다바이스 등록 과정
   - [**login**](./docs/Login.md) : 발급된 계정으로 JWT Token 을 발급 받아야 한다.
   - [**deviceEntityGroups**](./docs/DeviceEntityGroup.md) : 디바이스를 등록할 디바이스 그룹정보 조회한다.
   - [**saveDevice**](./docs/SaveDevice.md) : 서버에 디바이스를 등록한다.
   - [**saveDeviceSharedAttribute**](./docs/SaveDeviceSharedAttribute.md) : 장비 및 서버 사용하고자 하는 속성 등록을 등록한다.
   - [**deviceCredentials**](./docs/DeviceCredentials.md) : 등록된 디바이스의 Access Token(deviceCredentialsId) 을 발급받는다. 

2. 디바이스 설정 정보 등록 및 조회
   - [**saveDeviceAttributes**](./docs/SaveClientAttributes.md) : 장비의 속성 정보를 서버에 등록한다.
   - [**getDeviceAttributes**](./docs/DeviceAttributes.md) : 서버에 등록된 장비의 속성 정보를 조회한다.

3. 센서 데이터 전달
   - [**uploadTelemetryData**](./docs/UploadTelemetryData.md) : 서버에 센서 데이터를 전달한다.

4. 하드웨어 제어
   - 추후 추가 예정이며 연동 프로토콜은 **MQTT** 를 사용한다.

5. 시퀀스 다이어그램

   <img src="./docs/Device provisioning and data upload sequence diagram (REST Example).png" height="80%" width="80%" alt="System Integration Flow"/>
</br>


### 3.2  서비스 연동 API

- [**REST API**](#3.2.1-rest-api)
  - 목적 : 디바이스 등록 과정 및 센서 데이터 전달
- [**MQTT API**](#3.2.2-mqtt-api)
  - 목적 : 센서 데이터 전달 및 장비 제어 

</br>

### 3.2.1 REST API
  | Name | HTTP Method | Request URI | Description |
  |:--------- | :--------- | :--------- | :--------- |
  | [**login**](./docs/Login.md) | **POST** | /api/auth/login | 디비이스 등록하기 위해서 mobideep 서버의 customer 계정으로 로그인 하여 jwt 토큰을 조회한다. |
  | [**deviceEntityGroups**](./docs/DeviceEntityGroup.md) | **GET** | /api/entityGroups/DEVICE | 디바이스를 등록할 디바이스 그룹 정보를 조회한다. |
  | [**saveDevice**](./docs/SaveDevice.md) | **POST** | /api/device | AIRDEEP + MAC ADDRESS 형식으로 디이바스 등록한다. |
  | [**saveDeviceSharedAttribute**](./docs/SaveDeviceSharedAttribute.md) | **POST** | /api/plugins/telemetry/DEVICE/{deviceId}/SHARED_SCOPE | 장비 및 서버에서 수정할수 있는 속성을 등록한다. </br> ___- 필수 속성___ </br> 　uploadFrequency : 데이터 업로드 주기 |
  | [**deviceCredentials**](./docs/DeviceCredentials.md) | **GET** | /api/device/{deviceId} | 등록된 장비의 Access Token(deviceCredentialsId) 조회</br> ___- 권장 사항___ </br> 　로컬에 저장하여 사용하도록 한다. |
  | [**saveDeviceAttributes**](./docs/SaveClientAttributes.md) | **POST** | /api/v1/{deviceCredentialsId}/attributes | 장비의 상태를 등록한다. </br> ___- 필수 속성___ </br> 　firmwareFrequency, lastBootingTime |
  | [**getDeviceAttributes**](./docs/DeviceAttributes.md) | **GET** | /api/v1/{deviceCredentialsId}/attributes | 등록된 장비의 속성정보를 조회한다. |
  | [**uploadTelemetryData**](./docs/UploadTelemetryData.md) | **POST** | /api/v1/{deviceCredentialsId}/telemetry | 속성정보기준으로 데이터 업로드한다. |
</br></br>

### 3.2.2 MQTT API
 - MQTT API 를 사용하기 위해서는 반드시 **디바이스 등록과정**이 선행이 되어야 한다.
 - 시퀀스 다이어그램

    <img src="./docs/Device data upload sequence diagram (MQTT Example).png" height="80%" width="80%"/>

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

# *Appendix A. Sample 소스*
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

## HOST 정보
```
MOBIDEEP_HOST = "mobideep.rtdata.co.kr"
MOBIDEEP_HTTP_HOST = "http://mobideep.rtdata.co.kr:8080"
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
