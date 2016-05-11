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

sleep(30) #Give time to turn on the GSM Module and catch the network

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
#print ledStatus
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
#print mdMapping

ser = serial.Serial('/dev/ttyO1', 9600, timeout = 1)
ser.write('AT+CMGF=1\r\n')
sleep(0.2)
print ser.read(100)

ser.write('AT+GSMBUSY=1\r\n')   #Disables all incoming call
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
    print "Handling the following SMS:"
    print sms
    
    delSMS()        #Delete all SMSes from SIM including the one just received
    
    phoneNum = findPhoneNum(sms)    #Extract phone num from SMS
    if(phoneNum == ''):
        print "Phone number not found. Returning"
        return
    
    msg = findMsg(sms)  #Gives SMS content after #@TODO handle without # sms exception
    print "SMS content after # is: "
    print msg
    if(msg == ''):
        outSMS = 'SMS must start with a hash character like #kam0 p100 c90'
        sendSMS(phoneNum, outSMS)
        return
    
    if 'help' in msg:
        outSMS = 'Enter SMS in form #kam0 p for switching on indicator and paracetamol required.'
        sendSMS(phoneNum, outSMS)
        return
    
    outSMS = 'Indicator turned '	#Constructing the SMS that would be sent 
    
    healthcentre = msg[:3]  #Get the name of healthcentre which sent the msg
    try:
        hcMapping[healthcentre]
    except:
        print "Healthcenter not found."
        outSMS = 'Please enter correct healthcenter name'
        sendSMS(phoneNum, outSMS)
        return
    
    indication = msg[3]
    stockString = ''    #To indicate no stock required especially for the case withi indication '1'
    if indication == '1':   #Indicating that LED needs to be turned off
        outSMS += 'OFF for '
        ledStatus[hcMapping[healthcentre]][0] = '0' #Note that it is in string form
        ledStatus[hcMapping[healthcentre]][1] = '1'
        ledStatus[hcMapping[healthcentre]][2] = '0'
        outSMS += hcFullNameMapping[healthcentre]
        outSMS += ' healthcentre.'
        
    elif indication == '0':  #Indicating LED needs to be turned on
        stockString = msg[4:]
        stockTypeArray = re.findall(r'[a-zA-Z]+', stockString)
        stockQuantityArray = re.findall(r'\d+', stockString)
        #@TODO case when stock quantity for a stock type is not given

        outSMS += 'ON for '
        outSMS += hcFullNameMapping[healthcentre]
        outSMS += ' healthcentre. '
        outSMS += 'Stock Requested: '
        
        for i in range(0, len(stockTypeArray)):
            outSMS += mdMapping[stockTypeArray[i]]
            outSMS += ": "
            outSMS += stockQuantityArray[i]
            if not (i == len(stockTypeArray) - 1) :#i.e. if not last medicine stock
                outSMS += ", "

        ledStatus[hcMapping[healthcentre]][0] = '1' #Red
        ledStatus[hcMapping[healthcentre]][1] = '0' #Green
        ledStatus[hcMapping[healthcentre]][2] = '0' #Blue

    else:   #Wrong indication entered
        outSMS = 'Please enter 0 to indicate stock required ors 1 to indicate stock OK after healthcenter name. e.g. #kam0 p100 a980'
        sendSMS(phoneNum, outSMS)
        return
    
    updateLedLights()
    writeLedStatusToFile()
    writeToFile(healthcentre, indication, "".join(stockString.split()))
    sendSMS(phoneNum, outSMS)
    


while True :
	gsmRead = ser.read(10000)		#@TODO: Handle the case when only half of message is read in
	sys.stdout.write(gsmRead)		#To print sms without newline
	sleep(1)	    				#Sleep time is more in order to make it more likely that full SMS is read by ser.read()
	if "CMT" in gsmRead:            #CMT indicates that an SMS is received    
		handleSMS(gsmRead)