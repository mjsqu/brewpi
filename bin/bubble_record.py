#!/usr/bin/python
# Helper script to record a sound file and output
# a stream of numeric values that represent sound volume
# from the USB webcam
import pyaudio
import wave
import numpy as np
from datetime import datetime
 
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = r'file3.wav'

ferm1 = 8000
ferm2 = 1500

sf = "%Y%m%d:%H%M%S" 

audio = pyaudio.PyAudio()
 
# start Recording
stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK,input_device_index=2)

while True:
    data = stream.read(CHUNK)
    numpydata = np.fromstring(data, dtype=np.int16)
    loudest = numpydata.max()
    if loudest > ferm1:
       with open(r'/home/pi/temperature/data/bubble.log','a+') as f:
         f.write('ferm1|'+datetime.now().strftime(sf)+'\n')
 
# stop Recording
stream.stop_stream()
stream.close()
audio.terminate()

