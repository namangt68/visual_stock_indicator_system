#! /usr/bin python
####################################################################
# receiveSMS.py
# Received and displays the SMS
# Gopal Krishan Aggarwal and Naman Gupta
# Description: Keeps listening to new SMSes and whenever an SMS is received it
# prints it to console.
########################################################################
import sys
import serial
import re
from time import sleep
import shlex
import Adafruit_BBIO.GPIO as GPIO
import os
import datetime
scriptPath = os.path.dirname(os.path.realpath(__file__))

sleep(1) #Give time to turn on the GSM Module and catch the network

#This function will read list of health center from a text file  
#Store it in dictionary of health center name and their assigned code.
f = open(scriptPath + '/list.txt')
hcMapping = {}  #hcMapping contains mapping from healthcentre name to its id e.g hcMapping['kam'] = 0
pinMapping = {}
hcFullNameMapping = {}
for line in f:
    line = shlex.split(line.strip()) #Strip strips up whitespaces from beg and end of string; split splits the words by default on the basis of space
    hcMapping[line[1]] = line[2]
    pinMapping[line[2]] = [line[3], line[4], line[5]] #RGB LEDs pin
    hcFullNameMapping[line[1]] = line[0]
    GPIO.setup(line[3], GPIO.OUT, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(line[4], GPIO.OUT, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(line[5], GPIO.OUT, pull_up_down=GPIO.PUD_UP)
f.close()
#print hcMapping
#print pinMapping
#print hcFullNameMapping
ledStatus = {}
def readOldLedStatus():
    fin = open(scriptPath + '/oldLedStatus')
    for line in fin:
        line = shlex.split(line.strip()) #Strip strips up whitespaces from beg and end of string; split splits the words by default on the basis of space
        ledStatus[line[0]] = [line[1], line[2], line[3]] #RGB LEDs pin
    f.close()
readOldLedStatus()
print ledStatus
def updateLedLights():
    for key in ledStatus:
        for i in range(0, 3):
            if ledStatus[key][i] == '1':
                GPIO.output(pinMapping[key][i], GPIO.HIGH)
            else:
                GPIO.output(pinMapping[key][i], GPIO.LOW)
updateLedLights()
sleep(10)