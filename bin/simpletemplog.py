#!/usr/bin/python3
import os
import time
import json
import sys
import datetime
import onewiretemp as ot
import logging


sf = '%Y%m%d:%H%M%S'
dn = datetime.datetime.now()

# Logs time and temperatures to a file
# Also writes latest temperatures to /var/www/html/index.html
os.system('/sbin/modprobe w1-gpio')
os.system('/sbin/modprobe w1-therm')

datadir = os.path.join(sys.path[0],'..','data')
wmfile = os.path.join(datadir,'wiremap.json')
logfile = os.path.join(datadir,'brewlog.txt')
b5file = os.path.join(datadir,'b5.json')
htmlout = os.path.join(r'/var/www/html/','index.html')

logging.basicConfig(filename=logfile,level=logging.INFO)

tmps = ot.getall()

# Use logger to put temperatures into a file
while True:
    time.sleep(30)
    for x in tmps:
        c = x['colour']
        t = x['datestr']
        m = x['temperature']
        
        logline = t+'|'+c+'|'+m
        logging.info(logline)
