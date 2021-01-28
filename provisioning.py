import requests
import json

DEVICE_ENTITY_GROUPS        = "/api/entityGroups/DEVICE"
DEVICE_REGISTER_ENDPOINT    = "/api/device"
DEVICE_CREDENTIALS_ENDPOINT = "/api/device"
DEVICE_SHARED_ATTRIBUTES_ENDPOINT  = "/api/plugins/telemetry/DEVICE/{deviceId}/SHARED_SCOPE"
DEVICE_ATTRIBUTES_ENDPOINT  = "/api/v1/token/attributes"
DEVICE_TELEMETRY_ENDPOINT   = "/api/v1/token/telemetry"
ONE_STEP_DEVICE_PROVISIONING_API = "/v1/devices/register"
TIMESTAMP_ENDPOINT = "/v1/infos/time"

#Get current UTC timestamp
def getUTCTimestamp(HTTP_HOST, msgId, timeZone):
    headers = {
        "content-type":"application/json"
    }
    response = requests.request("GET", (HTTP_HOST+TIMESTAMP_ENDPOINT+"?msgId="+str(msgId)+"&getTimeByZid="+timeZone), headers=headers)
    return response.json()

#Device provisioning
def provision(HTTP_HOST, payload):
    headers = {
        "content-type":"application/json"
    }

    response = requests.request("POST", HTTP_HOST+ONE_STEP_DEVICE_PROVISIONING_API, data=json.dumps(payload), headers=headers)
    return response.json()

# Get device entity groups
def getDeviceEntityGroups(http_host, token):
    headers = {
        "content-type":"application/json",
        "x-authorization": "Bearer "+token
    }

    response = requests.request("GET", (http_host+DEVICE_ENTITY_GROUPS), headers=headers)
    return response.json()

# Save device with device name
def saveDevice(http_host, jwtToken, name, entityGroupId):
    headers = {
        "content-type":"application/json"
       ,"x-authorization": "Bearer "+jwtToken
    }

    payload = {
        "name":name
    }
    
    response = requests.request("POST", (http_host+DEVICE_REGISTER_ENDPOINT+"?entityGroupId="+entityGroupId), data=json.dumps(payload), headers=headers)
    
    if response.status_code == 200:
        return response.json().get("id").get("id")
    else:
        return ""

# Save device shared attributes with device id (scope:SHARED_SCOPE)
def saveDeviceSharedAttributes(http_host, jwtToken, deviceId, payload):
    headers = {
            "content-type":"application/json"
            ,"x-authorization": "Bearer "+jwtToken
    }

    response = requests.request("POST", (http_host+DEVICE_SHARED_ATTRIBUTES_ENDPOINT).replace("{deviceId}", deviceId), data=json.dumps(payload), headers=headers)
    return response.status_code

# Get device attributes for mqtt connection or http connection to send and get data or command to or from airdeep server
def getDeviceCredentials(http_host, jwtToken, deviceId):
    
    headers = {
        "content-type":"application/json"
       ,"x-authorization": "Bearer "+jwtToken
    }

    response = requests.request("GET", (http_host+DEVICE_CREDENTIALS_ENDPOINT+"/"+deviceId+"/credentials"), headers=headers)
    if response.status_code == 200:
        return response.json().get("credentialsId")
    else:
        return ""

# Save device attributes with device id (scope: CLIENT_SCOPE, SHARED_SCOPE)
def saveDeviceAttributes(http_host, credentialsId, payload):
    headers = {
            "content-type":"application/json"
    }

    response = requests.request("POST", (http_host+DEVICE_ATTRIBUTES_ENDPOINT).replace("token", credentialsId), data=json.dumps(payload), headers=headers)
    return response.status_code

# Get device attributes
def getDeviceAttributes(http_host, credentialsId, key):
    headers = {
            "content-type":"application/json"
        }

    response = requests.request("GET", (http_host+DEVICE_ATTRIBUTES_ENDPOINT).replace("token", credentialsId)+"?"+key, headers=headers)
    return response.json()

# Upload telemetry data to mobideep server
def uploadDeviceTelemetry(http_host, credentialsId, payload):
    headers = {
            "content-type":"application/json"
        }
    
    response = requests.request("POST", (http_host+DEVICE_TELEMETRY_ENDPOINT).replace("token", credentialsId), data=json.dumps(payload), headers=headers)
    return response.status_code

# Subscribe rpc 
def subscribeRPC(http_host, credentialsId, timeOut):
    headers = {
            "content-type":"application/json"
        }
    response = requests.request("GET", (http_host+"/api/v1/token/rpc?timeout="+timeOut).replace("token", credentialsId), headers=headers)
    if response.status_code == 200:
        return response.json().get("id")
    else:
        return ""

# Publish Reply to rpc
def publishResponseToRPCRequest(http_host, credentialsId, id):
    headers = {
            "content-type":"application/json"
        }
    response = requests.request("POST", (http_host+"/api/v1/token/rpc/"+id).replace("token", credentialsId), headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return ""

# Publish Reply to rpc
def postClientSideRPCRequest(http_host, credentialsId):
    headers = {
            "content-type":"application/json"
        }
    
    payload = {
        "method": "method",
        "params":{}
    }

    response = requests.request("POST", (http_host+"/api/v1/token/rpc").replace("token", credentialsId), data=json.dumps(payload), headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return ""