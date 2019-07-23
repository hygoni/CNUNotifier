import json
import requests
from collections import OrderedDict

API_KEY = open('/root/api.key', 'r+').readline().rstrip()
API_URL = 'https://fcm.googleapis.com/fcm/send'

def JSONMake(token, title, body):
    file_data = OrderedDict()
    notification={"title":title, "body":body}
    file_data["to"]=token
    file_data['notification'] = notification
    return json.dumps(file_data)

def send(json):
    r = requests.post(API_URL,
                  data=json,
                  headers={'Content-Type': 'application/json', 'Authorization' : API_KEY})
    return r.text
