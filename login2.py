import requests
import json

LOGIN_ENDPOINT = "/api/auth/login"

def login(http_host, username, password):
    headers = {"content-type":"application/json"}
    payload = {
        "username":username,
        "password":password
    }
    
    response = requests.request("POST", http_host+LOGIN_ENDPOINT, data=json.dumps(payload), headers=headers)
    return response.json().get("token")