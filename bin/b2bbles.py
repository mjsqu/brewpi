#!/usr/bin/python
# This script is for the business card reader webcam
# from Jaycar, it requires the volume to be set before the stream can be accurately parsed
import pyaudio
import wave
import numpy as np
import alsaaudio
from datetime import datetime
 
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000
CHUNK = 48000
RECORD_SECONDS = 5

ferm1 = 400

sf = "%Y%m%d:%H%M%S" 

# Set volume on device
m = alsaaudio.Mixer(control='Mic',cardindex=2)
m.setvolume(10,0)

audio = pyaudio.PyAudio()
 
# start Recording
stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK,input_device_index=3)
i = 0

while True:
    data = stream.read(CHUNK)
    numpydata = np.fromstring(data, dtype=np.int16)
    if i < 100:
       i+=1
    loudest = numpydata.max()
    if loudest > ferm1 and i > 4:
       with open(r'/home/pi/temperature/data/bubble2.log','a+') as f:
         f.write('ferm2|'+datetime.now().strftime(sf)+'\n')
 
# stop Recording
stream.stop_stream()
stream.close()
audio.terminate()

