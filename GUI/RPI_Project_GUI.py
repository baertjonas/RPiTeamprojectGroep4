#!/usr/bin/python3

import tkinter as tk
import paho.mqtt.client as mqtt
from threading import Thread
import time

listPlayersPos = []
listPlayersID = []
flagStartDestroy = 0

venster = tk.Tk()

imgWCrol = tk.PhotoImage( file = "Toilet_paper.png" )

imgVirus = tk.PhotoImage( file = "virus.png")

imgCart = tk.PhotoImage( file = "Cart.png" )

venster.title('RPi Groep 4')
venster.geometry("1600x900")

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("RPi/GUI")

def on_message(client, userdata, msg):
    print("Message received: " + str(msg.payload))
    payload = str(msg.payload)
    global listPlayersPos
    #ID=0; X=0100; Y=0100;
    #0 = Cart; 1 = Virus; 2 = WCrol;
    #TODO: Scrape payload from ID, X and Y
    ID = 0
    Xpos= 100
    Ypos= 100
    listPlayersID.append(ID)
    listPlayersPos.append([Xpos, Ypos])

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: " + str(mid) + " QoS: " + str(granted_qos))

def StartMQTT():
    global client
    client.loop_forever()

def GUI():
    frame = tk.Frame(venster)
    global listPlayersID, listPlayersPos
    aantalIteraties = len(listPlayersID) - 1
    for x in range(0, aantalIteraties):
        if listPlayersID[x] == 0:
            Img = tk.Label(frame, image = imgCart)
        elif listPlayersID[x] % 2:
            Img = tk.Label(frame, image = imgVirus)
        else:
            Img = tk.Label(frame, image = imgWCrol)
        Img.pack()
        Img.place(x=listPlayersPos[x][0], y=listPlayersPos[x][1])
    frame.destroy()

client = mqtt.Client(client_id="clientId-x3sRNOeZi9", clean_session=True, userdata=None, protocol=mqtt.MQTTv31)
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe
client.connect("broker.mab3lly.rocks", 1883)

job1= Thread(target=StartMQTT)
job1.start()
time.sleep(3)
job2 = Thread(target=GUI)
job2.start()

