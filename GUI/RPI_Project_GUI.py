#!/usr/bin/python3

import tkinter as tk
import paho.mqtt.client as mqtt
from threading import Thread
import time

listPlayersPos = []
listPlayersID = []
flagStartDestroy = 0
ID = 0
Xpos= 100
Ypos= 100
listPlayersID.append(ID)
listPlayersPos.append([Xpos, Ypos])

def MQTT():

    def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        client.subscribe("RPi/GUI")

    def on_message(client, userdata, msg):
        print("Message received: " + str(msg.payload))
        payload = str(msg.payload)
        Slice_ID = slice(4,5)
        Slice_xpos = slice(10,13) 
        Slice_ypos = slice(18,21)
        global listPlayersPos, listPlayerID
        listPlayersID.append(payload[Slice_ID])
        listPlayersPos.append([payload[Slice_xpos], payload[Slice_ypos]])
        #ID=00; X=0100; Y=0100;
        #0 = Cart; 1 = Virus; 2 = WCrol;

    def on_subscribe(client, userdata, mid, granted_qos):
        print("Subscribed: " + str(mid) + " QoS: " + str(granted_qos))

    client = mqtt.Client(client_id="clientId-x3sRNOeZi9", clean_session=True, userdata=None, protocol=mqtt.MQTTv31)
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_subscribe = on_subscribe
    client.connect("broker.mab3lly.rocks", 1883)
    client.loop_forever()

def GUI():
    venster = tk.Tk()

    imgWCrol = tk.PhotoImage(file="Toilet_paper.png")

    imgVirus = tk.PhotoImage(file="virus.png")

    imgCart = tk.PhotoImage(file="Cart.png")

    venster.title('RPi Groep 4')
    canvas = tk.Canvas(venster, width=800, height=600)
    canvas.pack()

    global listPlayersID, listPlayersPos
    aantalIteraties = len(listPlayersID)

    for x in range(0, aantalIteraties):
        if listPlayersID[x] == 0:
            image = canvas.create_image(listPlayersPos[x][0], listPlayersPos[x][1], anchor=tk.N, image=imgCart)
        if listPlayersID[x] % 2:
            image = canvas.create_image(listPlayersPos[x][0], listPlayersPos[x][1], anchor=tk.E, image=imgVirus)
        else:
            image = canvas.create_image(listPlayersPos[x][0], listPlayersPos[x][1], anchor=tk.W, image=imgWCrol)
    
    venster.mainloop()
    #image = canvas.create_image(100, 100, anchor=tk.W, image=imgWCrol)
    
    



job1 = Thread(target=GUI)
job2 = Thread(target=MQTT)
job1.start()
job2.start()
