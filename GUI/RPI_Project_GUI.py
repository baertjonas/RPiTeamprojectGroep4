#!/usr/bin/python3

import tkinter as tk
import paho.mqtt.client as mqtt
from threading import Thread
import time

listPlayersPos = []
listPlayersID = []
deleteImages = 0

def MQTT():

    def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        client.subscribe("RPi/GUI")

    def on_message(client, userdata, msg):
        print(str(msg.payload))
        payload = str(msg.payload)
        Slice_ID = slice(6,7)
        Slice_xpos = slice(12,15) 
        Slice_ypos = slice(20,23)
        global listPlayersPos, listPlayerID
        print(str(payload[Slice_ID]))
        print(str(payload[Slice_xpos]))
        print(str(payload[Slice_ypos]))
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

    def updateScreen():
        global listPlayersID, listPlayersPos, deleteImages
        if deleteImages == 1:
            canvas.delete("all")
        deleteImages = 1
        aantalIteraties = len(listPlayersID)
        for x in range(0, aantalIteraties):
            if listPlayersID[x] == 0:
                image = canvas.create_image(listPlayersPos[x][0], listPlayersPos[x][1], anchor=tk.N, image=imgCart)
            elif int(listPlayersID[x]) % 2 == 0:
                image = canvas.create_image(listPlayersPos[x][0], listPlayersPos[x][1], anchor=tk.N, image=imgWCrol)
            else:
                image = canvas.create_image(listPlayersPos[x][0], listPlayersPos[x][1], anchor=tk.N, image=imgVirus)
        listPlayersPos = []
        listPlayersID = []
        venster.after(1000, updateScreen)
    
    updateScreen()
    venster.mainloop()
    #image = canvas.create_image(100, 100, anchor=tk.W, image=imgWCrol)

    global listPlayersID, listPlayersPos
    aantalIteraties = len(listPlayersID)

try:
    job1 = Thread(target=GUI)
    job2 = Thread(target=MQTT)
    job1.start()
    job2.start()
except KeyboardInterrupt:
    job1.stop()
    job2.stop()
    pass
