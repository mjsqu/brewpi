import os
import json
import sys
from datetime import datetime as dt

datadir = os.path.join(sys.path[0],'..','data')
wmfile = os.path.join(datadir,'wiremap.json')
sf = '%Y%m%d:%H%M%S'

def gettemp(colour):
    """ Gets the temperature of the specified wire colour
    """ 
    # Check the colour of wire is valid before proceeding to probe the wires
    sensors = sensormap()
   
    sensor = [k for k,v in sensors.items() if v == colour]
    if len(sensor) == 0:
        raise Exception('Wire does not exist')
    wire_id = sensor[0]

    os.system('/sbin/modprobe w1-gpio')
    os.system('/sbin/modprobe w1-therm')

    w1path = '/sys/bus/w1/devices/'
    try:
        with open(os.path.join(w1path,wire_id,'w1_slave'),'r') as f:
            data = f.read()
    except:
        data = 'SENSOR ERROR'

    dl = data.split('\n')
    if dl[0][-3:] == 'YES':
        tempst = dl[1].index('t=')
        temperature = str(float(dl[1][tempst+2:])/1000)
    else:
        temperature = 'ERROR'

    return temperature

def sensormap():
    """ Returns the sensor map from the json
    """
    with open(wmfile,'r') as f:
        return json.load(f)

def getall():
    """ Returns a dict containing all temperature colours and values
    """
    sensors = sensormap()
    allsensors = []
    dn = dt.now()
    dnstr = dt.strftime(dn,sf)
    for k,v in sensors.items():
        d = {}
        d['id'] = k
        d['colour'] = v
        d['temperature'] = gettemp(v)
        d['datetime'] = dn
        d['datestr'] = dnstr
        allsensors.append(d)
    return allsensors
