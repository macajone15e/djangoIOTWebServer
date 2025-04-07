import json
import requests
import sys
import time
import datetime
import paho.mqtt.client as mqtt
from django.conf import settings
from datetime import date
from django.utils import timezone
from django.core.management.base import BaseCommand

from ...models import Devices, Temperatures, Pressures, Altitudes

DEBUG = True  
connected = False

client = mqtt.Client()

def on_connect(mqtt_client, userdata, flags, rc):
    global connected
    if rc == 0:
        if not connected:
            print('MQTT: Connected successfully')
        connected = True
        mqtt_client.subscribe('Sensors')
    else:
        print('MQTT: Connexion échouée, code:', rc)



def on_disconnect(mqtt_client, userdata, rc):
    global connected
    if connected:
        print("MQTT: Déconnecté, code:", rc)
    connected = False



def on_message(mqtt_client, userdata, msg):
    #print(f'Received message on topic: {msg.topic} with payload: {msg.payload}')
    data = json.loads(msg.payload)
    uid = data['id']
    if DEBUG:
        print("Payload brut reçu:", msg.payload)
        print("Data JSON:", data)
        print("UID reçu:", uid)
    #print("UID: " + uid)
    try:
        device = Devices.objects.get(uid=uid)
        #print("Device:" + device)
        device.lastSeenAt = timezone.now()
        device.save()
        #print("Device updated")
    except Exception as err:
        #print(f"An error occurred: {err}")
        device = Devices()
        device.uid = uid
        device.name = uid
        device.createdAt = timezone.now()
        device.lastSeenAt = timezone.now()
        device.save()
        #print("Device created: " + uid)
    if 'temperature' in data:
        temp = Temperatures()
        temp.device = device
        temp.value = data['temperature']
        temp.save()
        if DEBUG:
            print("Température enregistrée:", temp.value)
    if 'pressure' in data:
        press = Pressures()
        press.device = device
        press.value = data['pressure']
        press.save()
        if DEBUG:
            print("Pression enregistrée:", press.value)
    if 'altitude' in data:
        alt = Altitudes()
        alt.device = device
        alt.value = data['altitude']
        alt.save()
        if DEBUG:
            print("Altitude enregistrée:", alt.value)



def doConnect():
    try:
        client.connect(
            host=settings.MQTT_SERVER,
            port=settings.MQTT_PORT,
            keepalive=settings.MQTT_KEEPALIVE
        )
    except:
        print("MQTT: could not connect")


client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect
client.username_pw_set(settings.MQTT_USER, settings.MQTT_PASSWORD)
doConnect()
client.loop_start()

class Command(BaseCommand):
    help = 'Lance le client MQTT pour écouter les capteurs'

    def handle(self, *args, **kwargs):
        doConnect()
        client.loop_forever()