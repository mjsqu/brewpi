#!/usr/bin/python
import onewiretemp
import datetime
import os
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

frztemp = onewiretemp.gettemp('red')
sf = '%Y%m%d:%H%M%S'

dn = datetime.datetime.now()
dn_fmt = dn.strftime(sf)

entry = [dn_fmt,frztemp]

datadir = onewiretemp.datadir
frzfile = os.path.join(datadir,'frz.json')

frzdata = []

# Load existing JSON
if os.path.isfile(frzfile) == True:
    with open(frzfile,'r') as f:
        frzdata = json.load(f)

# Append data
frzdata.append(entry)

# Re-dump JSON
with open(frzfile,'w') as f:
    json.dump(frzdata,f)

# Plot data in JSON
from datetime import datetime,timedelta

dx = []
dy = []
for d in frzdata:
  parse_d = datetime.strptime(d[0],sf)
  if parse_d > datetime.now() - timedelta(hours=8):
      dx.append(parse_d)
      dy.append(float(d[1]))
  
fig,ax = plt.subplots()
# g- means green line solid
dy_mean = [sum(dy)/len(dy) for point in dy]
ax.plot(dx,dy,'g-')
ax.plot(dx,dy_mean,'r-')
ax.set_xlabel('Datetime')
ax.set_ylabel('Temperature')
ax.set_title('Freezer stats in past 8 hours')

ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=30))

fig.autofmt_xdate()
fig.savefig('/var/www/html/frz.png')

