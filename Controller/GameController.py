#!/usr/bin/python3

import urllib.request
import time as t
import random as r
import paho.mqtt.client as mqtt

id = 0
windowH = 600
windowW = 800
cartID = 0
virusID = 1
wcRolID = 2

virusPosX = 720
virusPosY = 260

wcRolPosX = 40
wcRolPosY = 260

cartPosX = 336
cartPosY = 0

score = 0

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("RPi/Controller")

def StartMQTT():
    global client
    client.loop_forever()

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: " + str(mid) + " QoS: " + str(granted_qos))

#ID=00; X=0100; Y=0100;
#Score=00
#0 = cart; 1 = Virus; 2 = WCrol;

def on_message(client, userdata, msg):
    if str(msg.payload)[slice(2, 7)] == "GetID":
        Rolverdeling()
    
    if str(msg.payload)[slice(2, 4)] == "ID":
        rolID = str(msg.payload)[slice(5, 6)]
        action = str(msg.payload)[slice(15, 17)]
        if rolID == "2":
            TerminalTestWcRol(action)
        if rolID == "1":
            TerminalTestVirus(action)
        if rolID == "0":
            TerminalTestKar(action)


def Rolverdeling():
    if id < 3:
        client.publish("RPi/Console", "GetID=" + id)
        id = id + 1

def TerminalTestWcRol(action):
    global wcRolID, wcRolPosY, wcRolPosX
    if action == "UP":
        wcRolPosY = wcRolPosY - 20
        client.publish("RPi/GUI", "ID=" + str(wcRolID).zfill(2) + "; X=" + str(wcRolPosX).zfill(4) +"; Y=" + str(wcRolPosY).zfill(4) +";")
        
    if action == "DN":
        wcRolPosY = wcRolPosY + 20
        client.publish("RPi/GUI", "ID=" + str(wcRolID).zfill(2) + "; X=" + str(wcRolPosX).zfill(4) +"; Y=" + str(wcRolPosY).zfill(4) +";")
        

def TerminalTestVirus(action):
    global virusID, virusPosY, virusPosX
    if action == "UP":
        virusPosY = virusPosY - 20
        client.publish("RPi/GUI", "ID=" + str(virusID).zfill(2) + "; X=" + str(virusPosX).zfill(4) +"; Y=" + str(virusPosY).zfill(4) +";")
        
    if action == "DN":
        virusPosY = virusPosY + 20
        client.publish("RPi/GUI", "ID=" + str(virusID).zfill(2) + "; X=" + str(virusPosX).zfill(4) +"; Y=" + str(virusPosY).zfill(4) +";")

def TerminalTestKar(action):
    global cartID, cartPosY, cartPosX
    if action == "UP":
        cartPosY = cartPosY - 20
        client.publish("RPi/GUI", "ID=" + str(cartID).zfill(2) + "; X=" + str(cartPosX).zfill(4) +"; Y=" + str(cartPosY).zfill(4) +";")
        
    if action == "DN":
        cartPosY = cartPosY + 20
        client.publish("RPi/GUI", "ID=" + str(cartID).zfill(2) + "; X=" + str(cartPosX).zfill(4) +"; Y=" + str(cartPosY).zfill(4) +";")

def AutoMoveRollen():
    global virusID, virusPosY, virusPosX, wcRolID, wcRolPosY, wcRolPosX
    wcRolPosX = wcRolPosX + 10
    virusPosX = virusPosX - 10
    client.publish("RPi/GUI", "ID=" + str(virusID).zfill(2) + "; X=" + str(virusPosX).zfill(4) +"; Y=" + str(virusPosY).zfill(4) +";")
    client.publish("RPi/GUI", "ID=" + str(wcRolID).zfill(2) + "; X=" + str(wcRolPosX).zfill(4) +"; Y=" + str(wcRolPosY).zfill(4) +";")

def Respawn(id):
    global wcRolID, wcRolPosX, wcRolPosY, virusID, virusPosX, virusPosY
    if (id % 2 == 0):
        #dan wc rol
        wcRolPosX = 0
        wcRolPosY = 260
        wcRolID = wcRolID + 2
        client.publish("RPi/GUI", "ID=" + str(wcRolID).zfill(2) + "; X=" + str(wcRolPosX).zfill(4) +"; Y=" + str(wcRolPosY).zfill(4) +";")
        client.publish("RPi/Console", "Rspwn=" + (str(wcRolID - 2).zfill(2)) + "; ID=" + str(wcRolID).zfill(2))
    else:
        #dan virus
        virusPosX = 720
        virusPosY = 260
        virusID = virusID + 2
        client.publish("RPi/GUI", "ID=" + str(virusID).zfill(2) + "; X=" + str(virusPosX).zfill(4) +"; Y=" + str(virusPosY).zfill(4) +";")
        client.publish("RPi/Console", "Rspwn=" + (str(virusID - 2).zfill(2)) + "; ID=" + str(virusID).zfill(2))


def Collision():
    global virusID, virusPosY, virusPosX, wcRolID, wcRolPosY, wcRolPosX, cartID, cartPosY, cartPosX, score

    #Virus Collision with map border
    if (virusPosY < 0):
        virusPosY = 0
        client.publish("RPi/GUI", "ID=" + str(virusID).zfill(2) + "; X=" + str(virusPosX).zfill(4) +"; Y=" + str(virusPosY).zfill(4) +";")

    if (virusPosY > 520):
        virusPosY = 520
        client.publish("RPi/GUI", "ID=" + str(virusID).zfill(2) + "; X=" + str(virusPosX).zfill(4) +"; Y=" + str(virusPosY).zfill(4) +";")

    if (virusPosX <= 0 ):
        Respawn(virusID)

    #WC rol Collision with map border
    if (wcRolPosY < 0):
        wcRolPosY = 0
        client.publish("RPi/GUI", "ID=" + str(wcRolID).zfill(2) + "; X=" + str(wcRolPosX).zfill(4) +"; Y=" + str(wcRolPosY).zfill(4) +";")

    if (wcRolPosY > 520):
        wcRolPosY = 520
        client.publish("RPi/GUI", "ID=" + str(wcRolID).zfill(2) + "; X=" + str(wcRolPosX).zfill(4) +"; Y=" + str(wcRolPosY).zfill(4) +";")

    if (wcRolPosX >= 720):
        Respawn(wcRolID)

    #cart Collision with map border
    if (cartPosY < 0):
        wcRolPosY = 0
        client.publish("RPi/GUI", "ID=" + str(cartID).zfill(2) + "; X=" + str(cartPosX).zfill(4) +"; Y=" + str(cartPosY).zfill(4) +";")

    if (cartPosY < 520):
        wcRolPosY = 520
        client.publish("RPi/GUI", "ID=" + str(cartID).zfill(2) + "; X=" + str(cartPosX).zfill(4) +"; Y=" + str(cartPosY).zfill(4) +";")

    #Virus and wcrol Collision
    if ((wcRolPosX + 80) > virusPosX and
        wcRolPosY < (virusPosY + 80) and 
        (wcRolPosY + 80) > virusPosY):
        Respawn(wcRolID)

    #wcrol and cart collision 
    if ((wcRolPosX + 80) > cartPosX and
        wcRolPosY < (cartPosY + 80) and 
        (wcRolPosY + 80) > cartPosY):
        Respawn(wcRolID)
        score = score + 1
        client.publish("RPi/GUI", "Score=" + str(score).zfill(2))

    #virus and cart collision
    if ((cartPosX + 88) > virusPosX and
        cartPosY < (virusPosY + 80) and 
        (cartPosY + 80) > virusPosY):
        Respawn(virusID)
        score = 0
        client.publish("RPi/GUI", "Score=" + str(score).zfill(2))

client = mqtt.Client(client_id="clientId-DLSoRvQWM3", clean_session=True, userdata=None, protocol=mqtt.MQTTv31)
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe
client.connect("broker.mab3lly.rocks", 1883)

client.loop_start()

while True:
    AutoMoveRollen()
    Collision()
    t.sleep(0.5)