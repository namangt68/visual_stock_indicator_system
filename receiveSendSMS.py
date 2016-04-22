#! /usr/bin python
####################################################################
# receiveSMS.py
# Received and displays the SMS
# Gopal Krishan Aggarwal
# April 22, 2016
# Contact: gopalkriagg@gmail.com
# Description: Keeps listening to new SMSes and whenever an SMS is received it
# prints it to console.
########################################################################
import sys
import serial
import re
from time import sleep
import shlex

#This function will read list of health center from a text file and 
#Store it in two different array of health center name and their assigned code.
f = open('list.txt')
hcMapping = {}  #hcMapping contains mapping from healthcentre name to its id e.g hcMapping['kam'] = 0
pinMapping = {}
hcFullNameMapping = {}
for line in f:
    line = shlex.split(line.strip()) #Strip strips up whitespaces from beg and end of string; split splits the words by default on the basis of space
    hcMapping[line[1]] = line[2]
    pinMapping[line[2]] = line[3]
    hcFullNameMapping[line[1]] = line[0]
f.close()

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
    healthcentre = msg[:3]
    print hcMapping[healthcentre]
    outSMS = 'Indicator turned '
    if msg[3] == '0':
        outSMS += 'ON for '
    else:
        outSMS += 'OFF for '
    outSMS += hcFullNameMapping[healthcentre]
    outSMS += ' healthcentre.'
    sendSMS(phoneNum, outSMS)

while True :
	sms = ser.read(10000)		#@TODO: Handle the case when only half of message is read in
	sys.stdout.write(sms)		#To print sms without newline
	sleep(1)					#Sleep time is more in order to make it more likely that full SMS is read by ser.read()
	if "CMT" in sms:
		handleSMS(sms)