 ## GITHUB VERSION
'''
This is a minimal implementation to publish to a MQTT version 3 server on aliyun

Prerequesites:
    Have access to aliyun MQTT server credentials.
    - Fill out from your credentials:
        - instanceId
        - accessKey
        - secretKey
        - groupId
    - Fill out these from your needs
        - client_id (any will work)
        - topic
'''

import hmac

import base64
from hashlib import sha1
import time
from paho.mqtt.client import MQTT_LOG_INFO, MQTT_LOG_NOTICE, MQTT_LOG_WARNING, MQTT_LOG_ERR, MQTT_LOG_DEBUG
from paho.mqtt import client as mqtt
from paho.mqtt import publish as publish

# Input
instanceId = ''# post-cn-{something}
accessKey = ''
secretKey = ''
groupId = '' #GID_{something}
client_id= groupId + '@@@' # + '{something}
topic = '' # topic to subscribe to

brokerUrl= instanceId + '.mqtt.aliyuncs.com'
userName ='Signature'+'|'+accessKey+'|'+instanceId
password = base64.b64encode(hmac.new(secretKey.encode(), client_id.encode(), sha1).digest()).decode()

message = "first message"
while message != "exit()":
    print("enter message")
    message = input()
    publish.single(topic, message, qos=1, retain=False, hostname=brokerUrl, port=1883, 
                   client_id=client_id,keepalive=60,protocol=mqtt.MQTTv311,auth = {'username': userName, 'password': password})