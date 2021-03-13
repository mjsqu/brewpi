#!/usr/bin/python
import pyaudio
import wave
import numpy as np
from datetime import datetime
 
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 44100

ferm1 = 17000

sf = "%Y%m%d:%H%M%S" 

audio = pyaudio.PyAudio()

for i in range(audio.get_device_count()):
    devinfo = audio.get_device_info_by_index(i)
    if devinfo['maxInputChannels'] > 0 and devinfo['name'][:6] == 'Webcam':
            webcam_index = i
 
stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK,input_device_index=webcam_index)

# Continuously record data and log when sounds above threshold heard
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
