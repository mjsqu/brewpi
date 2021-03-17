#!/usr/bin/python
import pyaudio
import datetime
import wave
import os
import struct,math
from datetime import datetime

def rms( data ):
    count = len(data)/2
    format = "%dh"%(count)
    shorts = struct.unpack( format, data )
    sum_squares = 0.0
    for sample in shorts:
        n = sample * (1.0/32768)
        sum_squares += n*n
    return math.sqrt( sum_squares / count )

strf = '%Y%m%d_%H%M%S'

dst = datetime.now().strftime(strf)

p = pyaudio.PyAudio()

webcam_index = 0

for i in range(p.get_device_count()):
    devinfo = p.get_device_info_by_index(i)
    if devinfo['maxInputChannels'] > 0:
        print(i) # Record 10 seconds of sound to a file
        if devinfo['name'][:7] == 'USB Cam':
            webcam_index = i
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000 
CHUNK = RATE 
RECORD_SECONDS = 20
WAVE_OUTPUT_FILENAME = r'/tmp/bub_'+dst+'.wav'

sf = "%Y%m%d:%H%M%S" 

audio = pyaudio.PyAudio()
 
# start Recording
stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK,input_device_index=webcam_index)

print('Recording and displaying volumes')

frames = []
 
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    print(rms(data))
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
