#!/usr/bin/python
import os
import time
import json
import sys
import datetime
import onewiretemp as ot

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

tmps = ot.getall()
cssfile = os.path.join(datadir,'ferm.css')

with open(htmlout,'w') as fh:
  fh.write('<html>')
  fh.write('<head>')
  fh.write('<style>')
  with open(cssfile,'r') as fr:
    x = fr.read()
  fh.write(x)
  fh.write('</style></head>')
  fh.write('<body><table id="temps">')
  fh.write('<tr><th>Colour</th><th>Temperature (deg C)</th>')

for x in tmps:
    c = x['colour']
    t = x['datestr']
    m = x['temperature']
    with open(htmlout,'a') as fh:
        fh.write('<tr><td style="background-color:'+c+'">'+c+'</td><td>'+m+'</td></tr>')
        
    with open(logfile,'a') as fl:
        fl.write(t+'|'+c+'|'+m+'\n')

with open(htmlout,'a') as fh:
    fh.write('</table>')

# Analyse the data in data/bubble.log, get amount of bubbles in last hour, 30, 10, 5 minutes
bfile = os.path.join(datadir,'bubble.log')
b2file = os.path.join(datadir,'bubble2.log')

with open(bfile,'r') as f:
    bdata = f.readlines()

with open(b2file,'r') as f:
    bdata.extend(f.readlines())

f1=0
f2=0

for x in bdata:
    # Each line in bdata represents a bubble that has been logged on a given fermenter
    fermdata = x.split('|')
    # Each line consists of pipe delimited fermenter|datetime information
    ferm = fermdata[0]
    t = fermdata[1].strip()
    td = datetime.datetime.strptime(t,sf)
    # If the datetime of the bubble was in the last five minutes, add to our
    # bubble count statistic
    if ferm == 'ferm1' and td > dn - datetime.timedelta(minutes=5):
        f1+=1
    if ferm == 'ferm2' and td > dn - datetime.timedelta(minutes=5):
        f2+=2

# This part collects the statistic value for the matplot script
# The bubble-rate value is then used in the matplot script to produce a graph
newdata = [dn.strftime(sf),'ferm2',f1]

if os.path.isfile(b5file) and os.stat(b5file).st_size > 0:
    with open(b5file,'rb') as fh:
        b5data = json.load(fh)
else:
    b5data = []

b5data.append(newdata)

# Write b5data to the json file so that the matplot script picks it up
with open(b5file,'wb') as fh:
    json.dump(b5data,fh)
  
with open(htmlout,'a') as fh:
    fh.write('<div id="f1">Fermenter 1 has bubbled '+str(f1)+' time(s) in the last 5 minutes</div>\n')
    fh.write('<div id="f2">Fermenter 2 has bubbled '+str(f2)+' time(s) in the last 5 mins</div>\n')
    fh.write('<div id="upd">Last updated at:'+datetime.datetime.now().strftime('%H:%M %d %b')+'</div>\n')
    fh.write('<img src="bubble_graph.png"/>')
    fh.write('</body></html>')
