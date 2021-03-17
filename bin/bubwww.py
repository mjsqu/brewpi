#!/usr/bin/python3
# Writes bubbling data to the www directory so I can look at it using:
# python3 -m http.server
import webcambub as wc
from time import sleep
ferm1 = 0.00

while True:
    s = wc.openstream(1)


    # Sleep for 4 mins 30
    sleep(270)


while True:
    data = s.read(wc.CHUNK)
    vol = rms(data)
    if loudest > ferm1:
       with open(r'/home/pi/temperature/data/bubble.log','a+') as f:
         f.write('ferm1|'+datetime.now().strftime(sf)+'\n')
 
# stop Recording
stream.stop_stream()
stream.close()
audio.terminate()