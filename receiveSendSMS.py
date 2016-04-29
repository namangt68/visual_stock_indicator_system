#! /usr/bin/python
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

#sleep(60) #Give time to turn on the GSM Module and catch the network

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
    fin.close()
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
def writeLedStatusToFile():
    f = open(scriptPath + '/oldLedStatus', 'w+')
    for key in ledStatus:
        f.write(key + " " + ledStatus[key][0] + " " + ledStatus[key][1] + " " + ledStatus[key][2] + "\n")
    f.close()
#This function will read list of medicine from a text file  
#Store it in a dictionary of medicine name and its assigned code.
f = open(scriptPath + '/medicine_list.txt')
mdMapping = {}  #mdMapping contains mapping from medicine code to its name e.g mdMapping['p'] = paracetamol
for line in f:
    line = shlex.split(line.strip()) #Strip strips up whitespaces from beg and end of string; split splits the words by default on the basis of space
    mdMapping[line[1]] = line[2]
f.close()
print mdMapping

ser = serial.Serial('/dev/ttyO1', 9600, timeout = 1)
ser.write('AT+CMGF=1\r\n')
sleep(0.2)
print ser.read(100)

#Deletes all SMSes to free up space
def delSMS() :
    ser.write("AT+CMGDA=\"")
    ser.write("DEL ALL\"\r\n")
    sleep(1)
    print ser.read(100)
    print ser.read(100)
    print("Deleted all SMSes")

delSMS()		#Delete any old SMSes
ser.write('AT+CNMI=2,2,0,0,0\r\n')		#blurt out contents of new SMS upon receipt to the GSM shield's serial out
print ser.read(100)

def sendSMS(phoneNum, msg) :
    ser.flushOutput()
    print("Sending SMS to "),
    print phoneNum
    ser.write("AT+CMGF=1\r\n")    #Because we want to send the SMS in text mode. Prints data to the serial port as human-readable ASCII text followed by a carriage return character (ASCII 13, or '\r') and a newline character (ASCII 10, or '\n').
    sleep(0.5)                    #On shorter delays it does not work
    ser.write("AT+CMGS=\"+91")
    sleep(0.5)
    ser.write(phoneNum)
    sleep(0.5)
    ser.write("\"\r\n")
    sleep(0.2)
    ser.write(msg)
    sleep(0.2)
    ser.write(chr(26))            #the ASCII code of the ctrl+z is 26
    sleep(0.2)                    #maybe this line may be removed
    ser.write("\r\n")
    sleep(5) 
    ser.flushOutput()

def findPhoneNum(sms) :
    try:
        found = re.search('\+91(.+?)"', sms).group(1)
    except AttributeError:
        # Pattern not found in the original string
        found = '' # apply error handling here
    return found

def findMsg(sms) :
    try:
        found = re.search('#(.*)', sms).group(1)
    except AttributeError:
        # Pattern not found in the original string
        found = '' # apply error handling here
    return found
    
def writeToFile(healthcentre, indication, stockDetails) :
    fout = open(scriptPath + '/records', 'a+')
    timestamp = str(datetime.datetime.now())
    fout.write(healthcentre + "," + indication + "," + stockDetails + "," + timestamp + "\n")
    fout.close()

def handleSMS(sms) :
    print "SMS received"
    print sms
    delSMS()
    phoneNum = findPhoneNum(sms)
    print "The phone num found is: ",
    print phoneNum
    msg = findMsg(sms)
    print "SMS msg is: "
    print msg
    outSMS = 'Indicator turned '
    if 'help' in msg:
        print "Enter SMS in form #kam0 p for switching on indicator and paracetamol required."
        outSMS = 'Enter SMS in form #kam0 p for switching on indicator and paracetamol required.'
        sendSMS(phoneNum, outSMS)
    else:
        healthcentre = msg[:3]
        if msg[3] == '1':
            outSMS += 'OFF for '
            print pinMapping[hcMapping[healthcentre]]
            ledStatus[hcMapping[healthcentre]][0] = '0'
            ledStatus[hcMapping[healthcentre]][1] = '1'
            ledStatus[hcMapping[healthcentre]][2] = '0'
            updateLedLights()
            writeLedStatusToFile()
            outSMS += hcFullNameMapping[healthcentre]
            outSMS += ' healthcentre.'
            #outSMS += 'Required:'
            #outSMS += mdMapping[medicine]
            sendSMS(phoneNum, outSMS)
            #indication = msg[3]
            #writeToFile(healthcentre, indication, stockDetails)
        else:
            medicine = msg[5]
            stockDetails = msg[4:]
            stockDetails = stockDetails.strip()
            print "Stock details are: ",
            print stockDetails
            print hcMapping[healthcentre]
            print mdMapping[medicine]
            if msg[3] == '0':
                outSMS += 'ON for '
                print pinMapping[hcMapping[healthcentre]]
                ledStatus[hcMapping[healthcentre]][0] = '1'
                ledStatus[hcMapping[healthcentre]][1] = '0'
                ledStatus[hcMapping[healthcentre]][2] = '0'
            else:
                outSMS += 'OFF for '
                print pinMapping[hcMapping[healthcentre]]
                ledStatus[hcMapping[healthcentre]][0] = '0'
                ledStatus[hcMapping[healthcentre]][1] = '1'
                ledStatus[hcMapping[healthcentre]][2] = '0'
            updateLedLights()
            writeLedStatusToFile()
            outSMS += hcFullNameMapping[healthcentre]
            outSMS += ' healthcentre.'
            outSMS += 'Required:'
            outSMS += mdMapping[medicine]
            sendSMS(phoneNum, outSMS)
            indication = msg[3]
            writeToFile(healthcentre, indication, stockDetails)

while True :
	sms = ser.read(10000)		#@TODO: Handle the case when only half of message is read in
	sys.stdout.write(sms)		#To print sms without newline
	sleep(1)					#Sleep time is more in order to make it more likely that full SMS is read by ser.read()
	if "CMT" in sms:
		handleSMS(sms)