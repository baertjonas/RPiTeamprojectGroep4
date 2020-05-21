#!/usr/bin/python3

import time
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt

leds = [16,20,21] # GPIO 16=rood=wc-rol // 20=geel=winkelkar // 21=groen=virus
segments = [4,17,27,22,5,6,13] # GPIO A=14 // B=17 // ...
buttons = [23,24]
ID = None

def on_connect(client, userdata, flags, rc):
 print("Connected with result code " + str(rc))
 client.subscribe("RPi/Console")

def on_publish(client, userdata, mid):
 print("published")

def on_message(client, userdata, msg):
 global ID
 if((str(msg.payload)[slice(2,7)]) == "GetID"):
  print(str(msg.payload)[slice(8,9)])
  if((str(msg.payload)[slice(8,9)]) == "1" or (str(msg.payload)[slice(8,9)]) == "2" or (str(msg.payload)[slice(8,9)]) == "3"):
   ID = (str(msg.payload)[slice(8,9)])

def leftButtonPressed(channel):
 global ID
 if (ID == 0):
  ret = client.publish("RPi/Console", "ID=0; Action=UP")
 elif (ID == 1):
  ret = client.publish("RPi/Console", "ID=1; Action=UP")
 elif (ID == 2):
  ret = client.publish("RPi/Console", "ID=2; Action=LT")

def rightButtonPressed(channel):
 global ID
 if (ID == 0):
  ret = client.publish("RPi/Console", "ID=0; Action=DN")
 elif (ID == 1):
  ret = client.publish("RPi/Console", "ID=1; Action=DN")
 elif (ID == 2):
  ret = client.publish("RPi/Console", "ID=2; Action=RT")

def GetID():
 client.publish("RPi/Console", "GetID")

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

counter = 0
inputKey = "X"

def icb(channel):
  global counter
  if channel == buttons[0]:
    print("up/down")
    counter += 1 if counter < 9 else -9
    GPIO.output(segments, BCD[counter])
  if channel == buttons[1]:
    print("left/right")

for x in buttons: # interrupts activeren
  GPIO.add_event_detect(x, GPIO.FALLING, callback=icb, bouncetime=100)

client = mqtt.Client(client_id="clientId-MnYsFs07V8", clean_session=True)
client.connect("broker.mab3lly.rocks",1883)
client.on_connect = on_connect
client.on_publish = on_publish
client.on_message = on_message

#try:
#  while True:
#    pass
#except KeyboardInterrupt:
#  pass

while inputKey != "":
  inputKey = input()

for x in buttons:
  GPIO.remove_event_detect(x)
GPIO.cleanup()
