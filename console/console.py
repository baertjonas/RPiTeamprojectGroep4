#!/usr/bin/python3

import time
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import random
import string

leds = [16,20,21] # GPIO 16=rood=wc-rol // 20=geel=winkelkar // 21=groen=virus
segments = [4,17,27,22,5,6,13] # GPIO A=14 // B=17 // ...
buttons = [23,24]
winkelkarID = [1]
wcrolID = [2,3,4,5]
virusID = [6,7,8,9]
ID = 0

def randomString(stringLength):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

clientID = randomString(8)

def on_connect(client, userdata, flags, rc):
  print("Connected with result code " + str(rc))
  client.subscribe("RPi/"+clientID)

def on_publish(client, userdata, mid):
  print("published")

def on_message(client, userdata, msg):
  payload = str(msg.payload)
  global ID
  if (payload[slice(2,5)] == "id="):
    ID = int(payload[slice(5,6)])
    print("Je hebt een nieuwe ID: "+str(ID))
    GPIO.output(segments, BCD[ID])
    GPIO.output(leds, 0) # alle leds uitschakelen
    if (ID in winkelkarID):
      print("Je bent nu een winkelkar.")
      GPIO.output(leds[1], 1) # gele led
    elif (ID in wcrolID):
      print ("Je bent nu een wc-rol.")
      GPIO.output(leds[0], 1) # rode led
    elif (ID in virusID):
      print("Je bent nu een virus.")
      GPIO.output(leds[2], 1) # groene led

GPIO.setmode(GPIO.BCM)
GPIO.setup(leds, GPIO.OUT) # leds activeren
GPIO.output(leds, False)
GPIO.setup(segments, GPIO.OUT) # 7-segments activeren
GPIO.output(segments, False)
GPIO.setup(buttons, GPIO.IN, pull_up_down=GPIO.PUD_UP)

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

def icb(channel):
  global ID
  if channel == buttons[0]:
    ret = client.publish("RPi/Console", "id="+str(ID)+";action=up")
    print("UP")
  if channel == buttons[1]:
    ret = client.publish("RPi/Console", "id="+str(ID)+";action=dn")
    print("DOWN")

for x in buttons: # interrupts activeren
  GPIO.add_event_detect(x, GPIO.FALLING, callback=icb, bouncetime=100)

client = mqtt.Client(client_id=clientID, clean_session=True)
client.connect("broker.mab3lly.rocks",1883)
client.on_connect = on_connect
client.on_publish = on_publish
client.on_message = on_message
client.loop_start()

# PROGRAM LOGIC
print("***COVID-19***")
print("Je bent client " + clientID)
client.publish("RPi/Auth", "client="+clientID+";hello") # publish a hello message to the controller to receive an ID
input() # when you press return, exit the program
client.publish("RPi/Auth", "client="+clientID+";goodbye") # publish a goodbye message to the controller to release the ID

for x in buttons:
  GPIO.remove_event_detect(x)
GPIO.cleanup()
