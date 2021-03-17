#!/usr/bin/python3
# Writes bubbling data to the www directory so I can look at it using:
# python3 -m http.server
import webcambub as wc
from time import sleep
ferm1 = 0.005

s = wc.openstream(1)

while True:
    data = s.read(wc.CHUNK)
    vol = wc.rms(data)
    if loudest > ferm1:
       with open(r'/home/pi/temperature/www/bubwww.log','a+') as f:
         f.write('ferm1|'+datetime.now().strftime(wc.sf)+'\n')
 
# stop Recording
s.stop_stream()
s.close()
wc.audio.terminate()