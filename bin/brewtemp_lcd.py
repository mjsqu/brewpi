#!/usr/bin/python
import os
import time
import json
import sys
import datetime
import onewiretemp as ot
from RPLCD.gpio import CharLCD
from RPi import GPIO

os.system('/sbin/modprobe w1-gpio')
os.system('/sbin/modprobe w1-therm')

datadir = os.path.join(sys.path[0],'..','data')
wmfile = os.path.join(datadir,'wiremap.json')

lcd = CharLCD(pin_rs=22,pin_e=18,pin_rw=None,pins_data=[16,11,12,15],numbering_mode=GPIO.BOARD,backlight_enabled=True)

while True:
    strt = ''
    tmps = ot.getall()
    for i,x in enumerate(tmps):
      c = x['colour']
      t = x['datestr']
      m = x['temperature']
      # Build the string then write it
      strt += c[0]+':'+m[:4]+' '
      if i == 1:
        strt+= '\r\n'
    lcd.clear()
    lcd.write_string(strt)
    time.sleep(1)
