#!/usr/bin/python3

import time
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import random
import string

leds = [16,20,21] # GPIO 16=rood=wc-rol // 20=geel=winkelkar // 21=groen=virus
segments = [4,17,27,22,5,6,13] # GPIO A=14 // B=17 // ...
buttons = [23,24]
ID = None

def randomString(stringLength):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

clientID = randomString(8)
print("Je clientID is "+clientID)

def on_connect(client, userdata, flags, rc):
 print("Connected with result code " + str(rc))
 client.subscribe("RPi/" + clientID)

def on_publish(client, userdata, mid):
 print("published")

def on_message(client, userdata, msg):
 global ID
 if((str(msg.payload)[slice(2,7)]) == "GetID"):
  print(str(msg.payload)[slice(8,10)])
  ID = (str(msg.payload)[slice(8,10)])
  print("Je (nieuwe) ID is " +str(ID))
  GPIO.output(leds, 0) # alle leds uit!!!
  if (int(ID)==0):
      print("Je bent een winkelkar.")
      GPIO.output(leds[1], 1) # gele led
  elif(int(ID) % 2 == 0):
      print ("Je bent een wc-rol.")
      GPIO.output(leds[0], 1) # rode led
  elif(int(ID) % 2 != 0):
      print("Je bent een virus.")
      GPIO.output(leds[2], 1) # groene led
 elif((str(msg.payload)[slice(2,7)]) == "Rspwn"):
  currentID=(str(msg.payload)[slice(8,10)])
  newID=(str(msg.payload)[slice(15,17)])
  Respawn(currentID,newID)
 GPIO.output(segments, BCD[int(ID)])

def GetID():
 client.publish("RPi/Controller", "GetID; Client=" + clientID)

def Respawn(currentID, newID):
 global ID
 if(currentID == ID):
  ID=newID

def icb(channel):
  global ID
  if channel == buttons[0]:
    ret = client.publish("RPi/Controller", "ID=" + ID +"; Action=UP")
    print("UP")
  if channel == buttons[1]:
    ret = client.publish("RPi/Controller", "ID=" + ID +"; Action=DN")
    print("DOWN")

GPIO.setmode(GPIO.BCM)
GPIO.setup(leds, GPIO.OUT) # leds activeren
GPIO.output(leds, False)
GPIO.setup(segments, GPIO.OUT) # 7-segments activeren
GPIO.output(segments, False)
GPIO.setup(buttons, GPIO.IN, pull_up_down=GPIO.PUD_UP)

for x in buttons: # interrupts activeren
  GPIO.add_event_detect(x, GPIO.FALLING, callback=icb, bouncetime=100)

BCD = {0:(1,1,1,1,1,1,0),
    1:(0,1,1,0,0,0,0),
    2:(1,1,0,1,1,0,1),
    3:(1,1,1,1,0,0,1),
    4:(0,1,1,0,0,1,1),
    5:(1,0,1,1,0,1,1),
    6:(1,0,1,1,1,1,1),
    7:(1,1,1,0,0,0,0),
    8:(1,1,1,1,1,1,1),
    9:(1,1,1,1,0,1,1)}

client = mqtt.Client(client_id=clientID, clean_session=True)
client.connect("broker.mab3lly.rocks",1883)
client.on_connect = on_connect
client.on_publish = on_publish
client.on_message = on_message

client.loop_start()

time.sleep(2)
while ID is None:
 GetID()
 time.sleep(5)

#while True:
# print(ID)
# time.sleep(1)

print("Druk op return om de console af te sluiten...")
input()

for x in buttons:
  GPIO.remove_event_detect(x)
GPIO.cleanup()
