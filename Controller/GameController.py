#!/usr/bin/python3

import urllib.request
import time as t
import random as r
import paho.mqtt.client as mqtt

idToGive = 0

windowH = 600
windowW = 800
cartID = 0
virusID = 1
wcRolID = 2

virusPosX = 770
virusPosY = 260

wcRolPosX = 40
wcRolPosY = 260

cartPosX = 416
cartPosY = 0

score = 0

clientWcRol = None
clientCart = None
clientVirus = None

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
    global clientWcRol, clientVirus, clientCart, idToGive
    print(str(msg.payload))
    if str(msg.payload)[slice(2, 7)] == "GetID":
        randonId = str(msg.payload)[slice(16,24)]
        print(randonId)
        if (clientCart == None and idToGive == 0):
            #geef cart rol
            clientCart = randonId
            Rolverdeling(clientCart)
        elif (clientVirus == None and idToGive == 1):
            #geef virus rol
            clientVirus = randonId
            Rolverdeling(clientVirus)
        elif (clientWcRol == None and idToGive == 2):
            #geef wcrol rol
            clientWcRol = randonId
            Rolverdeling(clientWcRol)

    if str(msg.payload)[slice(2, 4)] == "ID":
        rolID = str(msg.payload)[slice(5, 7)]
        action = str(msg.payload)[slice(16, 18)]
        if rolID == "00":
            TerminalTestKar(action)
        elif int(rolID) % 2 == 0:
            TerminalTestWcRol(action)
        else:
            TerminalTestVirus(action)  

def Rolverdeling(clientid):
    global idToGive, clientWcRol, clientCart, clientVirus
    if idToGive < 3:
        client.publish("RPi/" + clientid, "GetID=" + str(idToGive).zfill(2))
        idToGive = idToGive + 1

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

def InitialSpawn():
    global virusID, virusPosY, virusPosX, wcRolID, wcRolPosY, wcRolPosX
    client.publish("RPi/GUI", "ID=" + str(virusID).zfill(2) + "; X=" + str(virusPosX).zfill(4) +"; Y=" + str(virusPosY).zfill(4) +";")
    client.publish("RPi/GUI", "ID=" + str(wcRolID).zfill(2) + "; X=" + str(wcRolPosX).zfill(4) +"; Y=" + str(wcRolPosY).zfill(4) +";")
    client.publish("RPi/GUI", "ID=" + str(cartID).zfill(2) + "; X=" + str(cartPosX).zfill(4) +"; Y=" + str(cartPosY).zfill(4) +";")

def AutoMoveRollen():
    global virusID, virusPosY, virusPosX, wcRolID, wcRolPosY, wcRolPosX
    wcRolPosX = wcRolPosX + 5
    virusPosX = virusPosX - 5
    client.publish("RPi/GUI", "ID=" + str(virusID).zfill(2) + "; X=" + str(virusPosX).zfill(4) +"; Y=" + str(virusPosY).zfill(4) +";")
    client.publish("RPi/GUI", "ID=" + str(wcRolID).zfill(2) + "; X=" + str(wcRolPosX).zfill(4) +"; Y=" + str(wcRolPosY).zfill(4) +";")
    client.publish("RPi/GUI", "ID=" + str(cartID).zfill(2) + "; X=" + str(cartPosX).zfill(4) +"; Y=" + str(cartPosY).zfill(4) +";")

def Respawn(id):
    global wcRolID, wcRolPosX, wcRolPosY, virusID, virusPosX, virusPosY, clientWcRol, clientVirus
    if (id == 98):
        id = 2
        wcRolID = id
    if (id == 99):
        id = 1
        virusID = id

    if (id % 2 == 0):
        #dan wc rol
        wcRolPosX = 0
        wcRolPosY = r.randint(0,520)
        wcRolID = wcRolID + 2
        client.publish("RPi/GUI", "ID=" + str(wcRolID).zfill(2) + "; X=" + str(wcRolPosX).zfill(4) +"; Y=" + str(wcRolPosY).zfill(4) +";")
        client.publish("RPi/" + clientWcRol, "Rspwn=" + (str(wcRolID - 2).zfill(2)) + "; ID=" + str(wcRolID).zfill(2))
    else:
        #dan virus
        virusPosX = 720
        virusPosY = r.randint(0,520)
        virusID = virusID + 2
        client.publish("RPi/GUI", "ID=" + str(virusID).zfill(2) + "; X=" + str(virusPosX).zfill(4) +"; Y=" + str(virusPosY).zfill(4) +";")
        client.publish("RPi/" + clientVirus, "Rspwn=" + (str(virusID - 2).zfill(2)) + "; ID=" + str(virusID).zfill(2))

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
        cartPosY = 0
        client.publish("RPi/GUI", "ID=" + str(cartID).zfill(2) + "; X=" + str(cartPosX).zfill(4) +"; Y=" + str(cartPosY).zfill(4) +";")

    if (cartPosY > 520):
        cartPosY = 520
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
client.connect("broker.mab3lly.rocks", 1883)
client.on_connect = on_connect
client.on_message = on_message
#client.on_subscribe = on_subscribe


client.loop_start()

while True:
    if (clientWcRol != None and clientCart != None and clientVirus != None):
        AutoMoveRollen()
    else:
        InitialSpawn()
    Collision()
    t.sleep(0.250)