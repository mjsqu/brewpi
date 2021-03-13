#!/usr/bin/python
import plotly.graph_objs as go
import plotly
import plotly.plotly as py
import numpy as np
import json
import os,sys
from datetime import datetime,timedelta

datadir = os.path.join(sys.path[0],'..','data')

dfile = os.path.join(datadir,'brewlog.txt')
ffile = os.path.join(datadir,'bubble.log')
cfile = os.path.join(datadir,'plotly_cfg.json')

with open(cfile,'r') as fh:
  plotly_user_config = json.load(fh)

pu = plotly_user_config["plotly_username"]
pk = plotly_user_config["plotly_api_key"]
ps = plotly_user_config["plotly_streaming_tokens"][0]

py.sign_in(pu,pk)

with open(dfile,'r') as fh:
    x = fh.readlines()
    
with open(ffile,'r') as fh:
    b = fh.readlines()
    
ferm1_start = datetime(2017,10,1,14,40)
ferm2_start = datetime(2017,10,1,17,10)

ferm1_colour = 'red'
ferm2_colour = 'green'

temps = [el.strip().split('|') for el in x[1:]]
bubb = [bl.strip().split('|') for bl in b]

redy = [x[2] for x in temps if x[1] == 'red' and datetime.strptime(x[0],'%Y%m%d:%H%M%S') >= ferm1_start]
redx = [datetime.strptime(x[0],'%Y%m%d:%H%M%S') for x in temps if x[1] == 'red'and datetime.strptime(x[0],'%Y%m%d:%H%M%S') >= ferm1_start]

greeny = [x[2] for x in temps if x[1] == 'green' and datetime.strptime(x[0],'%Y%m%d:%H%M%S') >= ferm2_start]
greenx = [datetime.strptime(x[0],'%Y%m%d:%H%M%S') for x in temps if x[1] == 'green' and datetime.strptime(x[0],'%Y%m%d:%H%M%S') >= ferm2_start]

why = [x[2] for x in temps if x[1] == 'white' and datetime.strptime(x[0],'%Y%m%d:%H%M%S') >= ferm1_start]
whx = [datetime.strptime(x[0],'%Y%m%d:%H%M%S') for x in temps if x[1] == 'white' and datetime.strptime(x[0],'%Y%m%d:%H%M%S') >= ferm1_start]


bubb_f1 = np.array([datetime.strptime(b[1],'%Y%m%d:%H%M%S') for b in bubb if b[0] == 'ferm1'])
bubb_f2 = np.array([datetime.strptime(b[1],'%Y%m%d:%H%M%S')for b in bubb if b[0] == 'ferm2'])


bfs = bubb_f1.min()
i = bfs.minute
calc = 0
while i % 5 != 0:
    i = i - 1
    calc+=1
bfs = bfs - timedelta(minutes=calc,seconds=bfs.second)

timestages = []

while bfs <= bubb_f1.max():
    bfs += timedelta(minutes=5)
    timestages.append(bfs)

b1x = []
b2x = []
b1y = []
b2y = []
    
for i,x in enumerate(timestages):
    bub_count = [b for b in bubb_f1 if b >= x and b < timestages[i+1]]
    b1y.append(len(bub_count))
    b1x.append(x)
    bub_count = [b for b in bubb_f2 if b >= x and b < timestages[i+1]]
    b2y.append(len(bub_count))
    b2x.append(x)


# In[10]:


ttr = go.Scatter(x = redx, y = redy, name = 'Ale temperatures', line=dict(color=('rgb(255,0,0)')))
ttg = go.Scatter(x = greenx, y = greeny, name = 'Lager temperatures', line=dict(color=('rgb(0,255,0)')))
tb1 = go.Scatter(x = b1x, y = b1y, name = 'Ale bubbling', line=dict(color=('rgb(125,0,0)')))
tb2 = go.Scatter(x = b2x, y = b2y, name = 'Lager bubbling', line=dict(color=('rgb(0,125,0)')))
tta = go.Scatter(x = whx, y = why, name = 'Ambient', line = dict(color=('rgb(0,0,0)')))

trace = [ttr,ttg,tb1,tb2,tta]

layout = dict(title = 'Fermentation and bubbling',
              xaxis = dict(title = 'Datetime'),
              yaxis = dict(title = 'Temperature (degrees C)/Bubbles last 5 mins'),
              )

fig = dict(data=trace, layout=layout)
py.iplot(fig, filename='ferment2')
print "Graph updated"

# In[ ]:





# In[ ]:



    
    


# In[11]:


x[1:]


# In[7]:





# In[5]:




