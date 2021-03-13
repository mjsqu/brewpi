#!/usr/bin/python
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import json
import os,sys
from datetime import datetime,timedelta

sf = '%Y%m%d:%H%M%S'

datadir = os.path.join(sys.path[0],'..','data')
b5file = os.path.join(datadir,'b5.json')

with open(b5file,'r') as f:
    data = json.load(f)

# Convert element 0 to datetime
dx = []
dy = []
for d in data:
  parse_d = datetime.strptime(d[0],sf)
  if parse_d > datetime.now() - timedelta(hours=8):
      dx.append(parse_d)
      dy.append(d[2])
  
fig,ax = plt.subplots()
ax.plot(dx,dy,'g-')
ax.set_ylim(bottom=0)
ax.set_xlabel('Datetime')
ax.set_ylabel('Bubbles in previous 5 mins')
ax.set_title('Fermentation rates in past 8 hours')

ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=30))

fig.autofmt_xdate()
fig.savefig('/var/www/html/bubble_graph.png')

