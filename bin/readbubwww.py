#!/usr/bin/python3
import path
import json
from datetime import datetime

rootdir = "/home/pi/brewpi"
bubwww = path.join(rootdir,'www','bubwww.txt')
bubjson = path.join(rootdir,'www','bubwww.json')

date_format = '%Y%m%d:%H%M'

with open(bubwww,'r') as f:
    bubdat = f.readlines()

res = {}
for stat in bubdat:
    dt = datetime.strptime(stat[6:19],datet_format)
    res[dt] += 1

with open(bubjson,'w') as f:
    json.dump(res,f)