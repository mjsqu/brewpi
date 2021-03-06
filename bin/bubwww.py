#!/usr/bin/python3
# Writes bubbling data to the www directory so I can look at it using:
# python3 -m http.server
import webcambub as wc
from time import sleep
ferm1 = 0.005

s = wc.openstream(1)

while True:
    data = s.read(wc.CHUNK,exception_on_overflow=False)
    vol = wc.rms(data)
    if vol > ferm1:
       with open(r'../www/bubwww.txt','a+') as f:
         f.write('ferm1|'+wc.dt.now().strftime(wc.sf)+'\n')
 
# stop Recording
s.stop_stream()
s.close()
wc.audio.terminate()
