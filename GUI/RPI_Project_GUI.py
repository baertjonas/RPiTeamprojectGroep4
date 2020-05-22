#!/usr/bin/python3

import tkinter as tk
import paho.mqtt.client as mqtt
from threading import Thread
import time

listPlayersPos = []
listPlayersID = []
score = "00"
deleteImages = 0

def MQTT():

    def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        client.subscribe("RPi/GUI")

    def on_message(client, userdata, msg):
        print(str(msg.payload))
        payload = str(msg.payload)
        Slice_Type = slice(2,4)
        Slice_ID = slice(5,7)
        Slice_Score = slice(8,10)
        Slice_xpos = slice(12,15) 
        Slice_ypos = slice(20,23)
        global listPlayersPos, listPlayersID, score
        print(str(payload[Slice_Type]))
        print(str(payload[Slice_ID]))
        print(str(payload[Slice_xpos]))
        print(str(payload[Slice_ypos]))
        if str(payload[Slice_Type]) == "Sc":
            score = payload[Slice_Score]
            print("Score: " + str(score))
        else:
            listPlayersID.append(payload[Slice_ID])
            listPlayersPos.append([payload[Slice_xpos], payload[Slice_ypos]])
        #ID=00; X=0100; Y=0100;
        #Score=00
        #0 = Cart; 1 = Virus; 2 = WCrol;

    def on_subscribe(client, userdata, mid, granted_qos):
        print("Subscribed: " + str(mid) + " QoS: " + str(granted_qos))

    client = mqtt.Client(client_id="clientId-x3sRNOeZi9", clean_session=True, userdata=None, protocol=mqtt.MQTTv31)
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_subscribe = on_subscribe
    client.connect("broker.mab3lly.rocks", 1883)
    client.loop_start()

def GUI():
    venster = tk.Tk()
    imgWCrol = tk.PhotoImage(file="Toilet_paper.png")
    imgVirus = tk.PhotoImage(file="virus.png")
    imgCart = tk.PhotoImage(file="Cart.png")
    venster.title('RPi Groep 4')
    canvas = tk.Canvas(venster,bg="#b394e3", width=800, height=600)

    canvas.pack()

    def updateScreen():
        #Show score on screen
        global listPlayersID, listPlayersPos, deleteImages, score
        if deleteImages == 1:
            canvas.delete("all")
        deleteImages = 1
        aantalIteraties = len(listPlayersID)
        for x in range(0, aantalIteraties):
            if str(listPlayersID[x]) == "00":
                image = canvas.create_image(listPlayersPos[x][0], listPlayersPos[x][1], anchor=tk.N, image=imgCart)
                canvas.create_text(listPlayersPos[x][0], listPlayersPos[x][1], text=str(listPlayersID[x]))
            elif int(listPlayersID[x]) % 2 == 0:
                image = canvas.create_image(listPlayersPos[x][0], listPlayersPos[x][1], anchor=tk.N, image=imgWCrol)
                canvas.create_text(listPlayersPos[x][0], listPlayersPos[x][1], text=str(listPlayersID[x]))
            else:
                image = canvas.create_image(listPlayersPos[x][0], listPlayersPos[x][1], anchor=tk.N, image=imgVirus)
                canvas.create_text(listPlayersPos[x][0], listPlayersPos[x][1], text=str(listPlayersID[x]))
        canvas.create_text(760,20, text="Score: " + str(score))
        listPlayersPos = []
        listPlayersID = []
        venster.after(250, updateScreen)
    
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
