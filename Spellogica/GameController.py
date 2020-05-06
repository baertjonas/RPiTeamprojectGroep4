#!/usr/bin/python3

import urllib.request
import time as t
import random as r
import paho.mqtt.client as mqtt

id = 0

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("RPi/GUI")

def StartMQTT():
    global client
    client.loop_forever()

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: " + str(mid) + " QoS: " + str(granted_qos))

def on_message(client, userdata, msg):
    if str(msg.payload)[slice(2, 7)] == "GetID":
        Rolverdeling()
    
    if str(msg.payload)[slice(2, 4)] == "ID":
        rolID = str(msg.payload)[slice(5, 6)]
        action = str(msg.payload)[slice(15, 17)]
        if rolID == "0":
            TerminalTestWcRol(action)
        if rolID == "1":
            TerminalTestVirus(action)
        if rolID == "2":
            TerminalTestKar(action)


def Rolverdeling():
    if id < 3:
        client.publish("RPi/Console", "GetID=${id}")
        id = id + 1

def TerminalTestWcRol(action):
    if action == "UP":
        client.publish("RPi/Controller", "ID=0; Y=1")
    if action == "DN":
        client.publish("RPi/Controller", "ID=0; Y=-1")

def TerminalTestVirus(action):
    if action == "UP":
        client.publish("RPi/Controller", "ID=1; Y=1")
    if action == "DN":
        client.publish("RPi/Controller", "ID=1; Y=-1")

def TerminalTestKar(action):
    if action == "RT":
        client.publish("RPi/Controller", "ID=2; X=1")
    if action == "LT":
        client.publish("RPi/Controller", "ID=2; X=-1")

def AutoMoveRollen():
    client.publish("RPi/Controller", "ID=0; X=1")
    client.publish("RPi/Controller", "ID=1; X=-1")
    t.sleep(2)

client = mqtt.Client(client_id="clientId-x3sRNOeZi9", clean_session=True, userdata=None, protocol=mqtt.MQTTv31)
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe
client.connect("broker.mab3lly.rocks", 1883)

client.loop_start()

while True:
    pass