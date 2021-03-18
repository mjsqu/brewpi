#!/usr/bin/python3
import os
import json
from datetime import datetime

rootdir = "/home/pi/brewpi"
bubwww = os.path.join(rootdir,'www','bubwww.txt')
bubjson = os.path.join(rootdir,'www','bubwww.json')

date_format = '%Y%m%d:%H%M'

with open(bubwww,'r') as f:
    bubdat = f.readlines()

res = {}
for stat in bubdat:
    dt = stat[6:19]
    if dt not in res.keys():
       res[dt] = 0
    res[dt] += 1

with open(bubjson,'w') as f:
    json.dump(res,f)
