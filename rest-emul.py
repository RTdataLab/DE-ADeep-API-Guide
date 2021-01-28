import time
from datetime import datetime
import random

import login
import provisioning

# Host Information
MOBIDEEP_HTTP_HOST = "http://admin.mobideep.co.kr:8080"

# User Information
username = ""
password = ""

# Device Information
DEVICE_NAME = ""
DEVICE_ENTITY_GROUP_NAME = ""
credentialsId = ""
uploadFrequency = 1 # Data upload frequency is 1, it can be changed from server

# Get device device entity group id from user
DEVICE_ENTITY_GROUP_NAME = input("Please write \033[93mdevice entity group name\033[0m: ")

# Get device name from user (Device name should be in form of AIRDEEP + wifi mac address), in case of emulator only device name provided by user is uploaded
while not DEVICE_NAME:
    DEVICE_NAME = input("Please write \033[93mdevice name\033[0m: ")

# Read local persisted device credentialsId
try:
    with open(DEVICE_NAME,'r') as file:
        for line in file:
            credentialsId = line
except:
    print("Can not read file!")

if not credentialsId:
    # Get mobideep username from user
    while not username:
        username = input("Please write \033[93mmobideep username\033[0m: ")
    
    # Get mobideep password from user
    while not password:
        password = input("Please write \033[93mmobideep password\033[0m: ")

    # 1. Login to the mobideep server using login API
    jwtToken = login.login(MOBIDEEP_HTTP_HOST, username, password)
    print("JWT Token : ", jwtToken)

    # 2. Get Device entity groups to register device under this group
    deviceEntityGroups = provisioning.getDeviceEntityGroups(MOBIDEEP_HTTP_HOST, jwtToken)
    for entityGroup in deviceEntityGroups:
        
        if entityGroup.get("name") == DEVICE_ENTITY_GROUP_NAME:
            print(DEVICE_ENTITY_GROUP_NAME,"name",entityGroup.get("name"),entityGroup.get("id").get("id"))
            DEVICE_ENTITY_GROUP_ID = entityGroup.get("id").get("id")
        elif entityGroup.get("name") == "All":
            DEVICE_ENTITY_GROUP_ID = entityGroup.get("id").get("id")      

    # 3. Register Device to the mobideep server using device register API
    deviceId = provisioning.saveDevice(MOBIDEEP_HTTP_HOST, jwtToken, DEVICE_NAME, DEVICE_ENTITY_GROUP_ID)
    
    # 4. Save Device shared attributes to the mobideep server using device register API
    device_shared_attributes = {
        'uploadFrequency': uploadFrequency
    }
    provisioning.saveDeviceSharedAttributes(MOBIDEEP_HTTP_HOST, jwtToken, deviceId, device_shared_attributes)

    # 5. Get Device credentials to upload device attributes and telemetry data
    credentialsId = provisioning.getDeviceCredentials(MOBIDEEP_HTTP_HOST, jwtToken, deviceId)
    print("Device Credentials : ", credentialsId)

    # 6. Persist credentialsId to local or network storages
    with open(DEVICE_NAME, 'w') as file:
        file.write(credentialsId)
        print("Saved Device Credentials to file ", DEVICE_NAME)

device_client_attributes = {
    'firmwareVersion': 1.0, 'lastBootingTime':datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
}

# 7. Save Device client attributes to the mobideep server using device attributes API
provisioning.saveDeviceAttributes(MOBIDEEP_HTTP_HOST, credentialsId, device_client_attributes)

sensor_data = {
    'ts' : 0,
    'temp': 0, 'temp_max': 0,'temp_unt':'C', 'temp_ts' : datetime.now().timestamp(),
    'hmd': 0, 'hmd_max': 0, 'hmd_unt': "%",'hmd_ts' : datetime.now().timestamp(),
    'co2': 0, 'co2_max': 0, 'co2_unt': "ppm",'co2_ts' : datetime.now().timestamp(),
    'pm10': 0, 'pm10_max': 0, 'pm10_unt': "µg/m3", 'pm10_ts' : datetime.now().timestamp(),
    'pm2.5': 0, 'pm2.5_max': 0, 'pm2.5_unt': "µg/m3", 'pm2.5_ts' : datetime.now().timestamp(),
    'tvoc': 0, 'tvoc_max': 0, 'tvoc_unt': "mg/m3",'tvoc_ts' : datetime.now().timestamp(),
    'report_rsn': 'Report Reason'
}

while True:
    # 8. Get Device attributes to upload device telemetry data
    sharedKeys = "sharedKeys=uploadFrequency"
    attributes = provisioning.getDeviceAttributes(MOBIDEEP_HTTP_HOST, credentialsId, sharedKeys)
    
    if attributes and attributes.get("shared"):
        if attributes.get("shared").get("uploadFrequency"):
            uploadFrequency = attributes.get("shared").get("uploadFrequency")

    # Set sensor data
    timestamp_info = provisioning.getUTCTimestamp(AIRDEEP_HTTP_HOST, random.randint(0, 100), "UTC")
    ts = timestamp_info.get("msg").get("timestamp")
    sensor_data['temp'] = random.randint(0, 100)
    sensor_data['temp_ts'] = ts
    sensor_data['hmd'] = random.randint(0, 100)
    sensor_data['hmd_max'] = random.randint(0, 100)
    sensor_data['hmd_ts'] = ts
    sensor_data['co2'] = random.randint(0, 100)
    sensor_data['co2_max'] = random.randint(0, 100)
    sensor_data['co2_ts'] = ts
    sensor_data['pm10'] = random.randint(0, 100)
    sensor_data['pm10_max'] = random.randint(0, 100)
    sensor_data['pm10_ts'] = ts
    sensor_data['pm2.5'] = random.randint(0, 100)
    sensor_data['pm2.5_max'] = random.randint(0, 100)
    sensor_data['pm2.5_ts'] = ts
    sensor_data['tvoc'] = random.randint(0, 100)
    sensor_data['tvoc_max'] = random.randint(0, 100)
    sensor_data['tvoc_ts'] = ts

    # 9. Upload Device telemetry data to mobideep server using device telemetry API
    provisioning.uploadDeviceTelemetry(MOBIDEEP_HTTP_HOST, credentialsId, sensor_data)

    # Sleep for given time
    time.sleep(uploadFrequency)