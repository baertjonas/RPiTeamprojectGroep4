#!/usr/bin/python3

import RPi.GPIO as GPIO

leds = [16,20,21] # GPIO 16=rood=wc-rol // 20=geel=winkelkar // 21=groen=virus
segments = [4,17,27,22,5,6,13] # GPIO A=14 // B=17 // ...
buttons = [23,24]

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
