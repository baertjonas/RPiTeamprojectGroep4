#!/usr/bin/python3

import tkinter as tk
import paho.mqtt.client as mqtt
from PIL import ImageTk, Image
from threading import Thread

listPlayersPos = []
listPlayersID = []
flagStartDestroy = 0

imgWCrol = ImageTK.PhotoImage(Image.open("Toilet_paper.png"))
imgWCrol = imgWCrol.resize((150,150), Image.ANTIALIAS)
imgVirus = ImageTK.PhotoImage(Image.open("virus.png"))
imgVirus = imgVirus.resize((150,150), Image.ANTIALIAS)
imgCart = ImageTK.PhotoImage(Image.open("Cart.png"))
imgCart = imgCart.resize((150,150), Image.ANTIALIAS)

venster = tk.Tk()
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
    #0 = Rol; 1 = Virus; 2 = cart;
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
    global flagStartDestroy
    if flagStartDestroy == 1:
        frame.destroy()
    frame = Frame(venster)
    flagStartDestroy = 1
    for x in (len(listPlayersID) - 1):
        if listPlayersID[x] == 0:
            Img = Label(frame, image = imgWCrol)
        elif listPlayersID[x] == 1:
            Img = Label(frame, image = imgVirus)
        elif listPlayersID[x] == 2:
            Img = Label(frame, image = imgCart)
        Img.place(x=listPlayersPos[x][0], y=listPlayersPos[x][1])



client = mqtt.Client(client_id="clientId-x3sRNOeZi9", clean_session=True, userdata=None, protocol=mqtt.MQTTv31)
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe
client.connect("broker.mab3lly.rocks", 1883)

job1= Thread(target=StartMQTT)
job1.start()


