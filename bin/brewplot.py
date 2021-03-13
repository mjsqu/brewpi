#!/usr/bin/python
import os
import time
import json
import sys
from datetime import datetime,timedelta
import numpy as np

datadir = os.path.join(sys.path[0],'..','data')
logfile = os.path.join(datadir,'brewlog.txt')

dn = datetime.now()

strf = '%Y%m%d:%H%M%S'

with open(logfile,'r') as fh:
    x = fh.readlines()
    
temps = [el.strip().split('|') for el in x[1:]]
temps = [t for t in temps if datetime.strptime(t[0],strf) > dn - timedelta(hours=1)]

tmps = []
for t in temps:
    d = {}
    d['dt'] = datetime.strptime(t[0],strf)
    d['colour'] = t[1]
    d['temp'] = t[2]
    tmps.append(d)

# Bubble data
bfile = os.path.join(datadir,'bubble.log')
with open(bfile,'r') as f:
    bdata = f.readlines()

bubb = [bl.strip().split('|') for bl in bdata]
bubb = [b for b in bubb if datetime.strptime(b[1],strf) > dn - timedelta(hours=1)]

bubb_f1 = np.array([datetime.strptime(b[1],strf) for b in bubb if b[0] == 'ferm1'])
bubb_f2 = np.array([datetime.strptime(b[1],strf) for b in bubb if b[0] == 'ferm2'])

bfs = bubb_f1.min()
print "Earliest bubble in the previous hour:"+datetime.strftime(bfs,strf)
i = bfs.minute
calc = 0
while i % 5 != 0:
    i = i - 1
    calc+=1
bfs = bfs - timedelta(minutes=calc,seconds=bfs.second)

print "Bubble start: "+datetime.strftime(bfs,strf)
print "Bubble end: "+datetime.strftime(bubb_f1.max(),strf)

timestages = []

while bfs <= bubb_f1.max():
    bfs += timedelta(minutes=5)
    timestages.append(bfs)

print "Timestages: "+str(timestages)

b1x = []
b2x = []
b1y = []
b2y = []
    
for i,x in enumerate(timestages):
    bub_count = [b for b in bubb_f1 if b >= x and b < timestages[i+1]]
    if len(bub_count) > 0:
        b1y.append(len(bub_count))
        b1x.append(x)
    bub_count = [b for b in bubb_f2 if b >= x and b < timestages[i+1]]
    if len(bub_count) > 0:
        b2y.append(len(bub_count))
        b2x.append(x)

# Extend plotly traces - replace with an hourly script that reads the logfiles and updates the plotly with the last hour's activity
import plotly.plotly as py
from plotly.graph_objs import *

with open(os.path.join(datadir,'plotly_cfg.json')) as f:
    cfg = json.load(f)

py.sign_in(cfg['plotly_username'],cfg['plotly_api_key'])

ttr = Scatter(
    x = [t['dt'] for t in tmps if t['colour'] == 'red'],
    y = [t['temp'] for t in tmps if t['colour'] == 'red']
)

ttg = Scatter(
    x = [t['dt'] for t in tmps if t['colour'] == 'green'],
    y = [t['temp'] for t in tmps if t['colour'] == 'green']
)

tta = Scatter(
    x = [t['dt'] for t in tmps if t['colour'] == 'white'],
    y = [t['temp'] for t in tmps if t['colour'] == 'white']
)

tb1 = Scatter(
    x = b1x,
    y = b1y
)  

tb2 = Scatter(
    x = b2x,
    y = b2y
)

trace = Data([ttr,ttg,tb1,tb2,tta])
# Only allows 100 plots per day, so do this every 14.4 minutes or less
py.plot(trace,filename='ferment2',fileopt='extend')
