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
    'temperature_value': 0, 'temperature_max_value': 0,'temperature_ts': 0,'temperature_unit':'C', 
    'humidity_value': 0, 'humidity_max_value': 0, 'humidity_ts': 0, 'humidity_unit': "%",
    'co2_value': 0, 'co2_max_value': 0, 'co2_ts': 0, 'co2_unit': "ppm",
    'pm10_value': 0, 'pm10_max_value': 0, 'pm10_ts': 0, 'pm10_unit': "µg/m3", 
    'pm2.5_value': 0, 'pm2.5_max_value': 0, 'pm2.5_ts': 0, 'pm2.5_unit': "µg/m3", 
    'tvoc_value': 0, 'tvoc_max_value': 0, 'tvoc_ts': 0, 'tvoc_unit': "mg/m3",
    'report_reason': 'Report Reason'
}

while True:
    # 8. Get Device attributes to upload device telemetry data
    sharedKeys = "sharedKeys=uploadFrequency"
    attributes = provisioning.getDeviceAttributes(MOBIDEEP_HTTP_HOST, credentialsId, sharedKeys)
    
    if attributes and attributes.get("shared"):
        if attributes.get("shared").get("uploadFrequency"):
            uploadFrequency = attributes.get("shared").get("uploadFrequency")

    # Set sensor data
    sensor_data['temperature_value'] = random.randint(0, 100)
    sensor_data['humidity_value'] = random.randint(0, 100)
    sensor_data['humidity_max_value'] = random.randint(0, 100)
    sensor_data['co2_value'] = random.randint(0, 100)
    sensor_data['co2_max_value'] = random.randint(0, 100)
    sensor_data['pm10_value'] = random.randint(0, 100)
    sensor_data['pm10_max_value'] = random.randint(0, 100)
    sensor_data['pm2.5_value'] = random.randint(0, 100)
    sensor_data['pm2.5_max_value'] = random.randint(0, 100)
    sensor_data['tvoc_value'] = random.randint(0, 100)
    sensor_data['tvoc_max_value'] = random.randint(0, 100)

    sensor_data['temperature_ts'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    sensor_data['humidity_ts'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    sensor_data['co2_ts'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    sensor_data['pm10_ts'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    sensor_data['pm2.5_ts'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    sensor_data['tvoc_ts'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

    # 9. Upload Device telemetry data to mobideep server using device telemetry API
    provisioning.uploadDeviceTelemetry(MOBIDEEP_HTTP_HOST, credentialsId, sensor_data)

    # Sleep for given time
    time.sleep(uploadFrequency)