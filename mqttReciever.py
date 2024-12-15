## GITHUB VERSION
'''
This is a minimal implementation of subscribing to a MQTT version 3 server on aliyun

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

# Credentials
instanceId = ''# post-cn-{something}
accessKey = ''
secretKey = ''
groupId = '' #GID_{something}

# Fill as needed
client_id= groupId + '@@@' # + '{something}
topic = '' # topic to subscribe to

brokerUrl= instanceId + '.mqtt.aliyuncs.com'
userName ='Signature'+'|'+accessKey+'|'+instanceId
password = base64.b64encode(hmac.new(secretKey.encode(), client_id.encode(), sha1).digest()).decode()
# You can find the expected password on aliyun site


def on_log(client, userdata, level, buf):
    if level == MQTT_LOG_INFO:
        head = "INFO"
    elif level == MQTT_LOG_NOTICE:
        head = 'NOTICE'
    elif level == MQTT_LOG_WARNING:
        head = 'WARNING'
    elif level == MQTT_LOG_ERR:
        head = "ERR"
    elif level == MQTT_LOG_DEBUG:
        head = 'DEBUG'
    else:
        head = level
        print(head, ": ", buf)

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print('unexpected disconnection ', rc)

def on_connect(client, userdata, flags, rc):
    print('Connected with result code ', rc)
    client.subscribe(topic, 0)

def on_message(client, userdata, msg):
    print(msg.topic, ' ', str(msg.payload))

client = mqtt.Client(client_id, protocol= mqtt.MQTTv311, clean_session=True)
client.on_log = on_log
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect
client.username_pw_set(userName, password)


# port=8883 if SSL needed:
# client.tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS, ciphers=None)

# port 1883 otherwise
client.connect(brokerUrl, 1883, 60)
client.loop_forever()
