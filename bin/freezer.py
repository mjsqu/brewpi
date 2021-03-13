#!/usr/bin/python
import os
import time
import json
import sys
import datetime

sf = '%Y%m%d:%H%M%S'

# Logs time and temperatures to a file for the red probe in the freezer
# Also writes latest temperatures to /var/www/html/frz.html
os.system('/sbin/modprobe w1-gpio')
os.system('/sbin/modprobe w1-therm')

datadir = os.path.join(sys.path[0],'..','data')
wmfile = os.path.join(datadir,'wiremap.json')
logfile = os.path.join(datadir,'frzlog.txt')
b5file = os.path.join(datadir,'b5.json')

w1path = '/sys/bus/w1/devices/'

with open(wmfile,'r') as f:
    sensors = json.load(f)

htmlout = '/var/www/html/frz.txt'
cssfile = os.path.join(datadir,'ferm.css')

dn = datetime.datetime.now()

wire_id = [k for k,v in sensors.items() if v == 'red'][0]

dn_fmt = dn.strftime(sf)

# Read the file and append the data straight onto frz.txt
with open(os.path.join(w1path,k,'w1_slave'),'r') as f:
    data = f.read()

dl = data.split('\n')
if dl[0][-3:] == 'YES':
    tempst = dl[1].index('t=')
    temperature = str(float(dl[1][tempst+2:])/1000)
else:
    temperature = 'ERROR'

with open(htmlout,'a') as fh:
    fh.write(dn_fmt+'|'+temperature+'\n')
