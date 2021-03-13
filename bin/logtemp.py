#!/usr/bin/python3
import datetime,csv
from subprocess import Popen,PIPE
from sense_hat import SenseHat
s=SenseHat()

ftime='%Y.%m.%d %H:%M:%S'
with open('/home/pi/temperature/data/templog2.txt','a') as f:
  output = Popen(['/opt/vc/bin/vcgencmd','measure_temp'],stdout=PIPE)
  cpu = str(output.stdout.read())
  cpupos = cpu.index('temp')+5
  cpuf = float(cpu[cpupos:cpupos+4])
  # Correction
  tempf = float(s.get_temperature())
  corrtemp = tempf - ((cpuf-tempf)/1.5)
  sp=csv.writer(f,delimiter=',')
  line = [datetime.datetime.now().strftime(ftime),corrtemp]
  sp.writerow(line)
