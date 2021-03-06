# Library of functions for processing webcams that listen for fermenters bubbling

# Run a bubble checker and log the process ID, time of start and other information to a file
# Periodically do a keep-alive check on the most recent process that we ran, and restart and replace the information in the file
import os
import json
import sys
from datetime import datetime as dt
import pyaudio
import wave
import struct,math

datadir = os.path.join(sys.path[0],'..','data')
psfile = os.path.join(datadir,'bubbleprocess.json')
sf = '%Y%m%d:%H%M%S'

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = RATE

sf = "%Y%m%d:%H%M%S" 

audio = pyaudio.PyAudio()

def rms( data ):
    """ Calculates RMS for sound data
    """
    count = len(data)/2
    format = "%dh"%(count)
    shorts = struct.unpack( format, data )
    sum_squares = 0.0
    for sample in shorts:
        n = sample * (1.0/32768)
        sum_squares += n*n
    return math.sqrt( sum_squares / count )

def deviceinfo():
    """ Returns all device info
    """
    d = []
    for i in range(audio.get_device_count()):
        d.append(audio.get_device_info_by_index(i))
    
    return d

def openstream(webcam_index):
    """ Returns an opened stream on the given webcam
    """
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK,input_device_index=webcam_index)
    return stream

def samplenum(webcam_index,RECORD_SECONDS):
    s = openstream(webcam_index) 
   
    frames = []
    numdata = []
 
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = s.read(CHUNK)
        numdata.append(rms(data))
        frames.append(data)

    s.stop_stream()
    s.close()
    return frames,numdata

def samplefile(webcam_index,RECORD_SECONDS,WAVE_OUTPUT_FILENAME):
    frames,numdata = samplenum(webcam_index,RECORD_SECONDS)
    waveFile = wave.open(WAVE_OUTPUT_FILENAME,'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()
