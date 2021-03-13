#!/bin/bash

if [ $(ps -ef | grep bubbles | grep -v grep | wc -l) -eq 0 ]
then
  echo "Restarting Bubble recorder"
  nohup /home/pi/temperature/bin/bubbles.py
fi

#if [ $(ps -ef | grep b2bbles | grep -v grep | wc -l) -eq 0 ]
#then
#  echo "Restarting B2"
#  nohup /home/pi/temperature/bin/b2bbles.py
#fi
