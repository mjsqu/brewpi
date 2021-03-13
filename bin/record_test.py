#!/usr/bin/python
import pyaudio
import datetime
import wave
import os
import numpy as np
from datetime import datetime

strf = '%Y%m%d_%H%M%S'
dst = datetime.now().strftime(strf)

p = pyaudio.PyAudio()

webcam_index = 0

for i in range(p.get_device_count()):
    devinfo = p.get_device_info_by_index(i)
    if devinfo['maxInputChannels'] > 0:
        print i# Record 10 seconds of sound to a file
        if devinfo['name'][:6] == 'Webcam':
            webcam_index = i

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 44100
RECORD_SECONDS = 20
WAVE_OUTPUT_FILENAME = r'/tmp/bub_'+dst+'.wav'

sf = "%Y%m%d:%H%M%S" 

audio = pyaudio.PyAudio()
 
# start Recording
stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK,input_device_index=webcam_index)

print 'Recording and displaying volumes'

frames = []
 
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    numpydata = np.fromstring(data, dtype=np.int16)
    loudest = numpydata.max()
    print loudest
    frames.append(data)
 
# stop Recording
stream.stop_stream()
stream.close()
audio.terminate()

waveFile = wave.open(WAVE_OUTPUT_FILENAME,'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()
