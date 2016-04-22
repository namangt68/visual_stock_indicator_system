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
from time import sleep

#Deletes all SMSes to free up space
def delSMS() :
  ser.write("AT+CMGDA=\"")
  ser.write("DEL ALL\"\r\n")
  sleep(1)
  print ser.read(100)
  print ser.read(100)
  print("Deleted all SMSes")

def handleSMS(sms) :
	print "SMS received"
	print sms
	delSMS()

ser = serial.Serial('/dev/ttyO1', 9600, timeout = 1)
ser.write('AT+CMGF=1\r\n')
sleep(0.2)
print ser.read(100)

delSMS()		#Delete any old SMSes
ser.write('AT+CNMI=2,2,0,0,0\r\n')		#blurt out contents of new SMS upon receipt to the GSM shield's serial out
print ser.read(100)

while True :
	sms = ser.read(10000)		#@TODO: Handle the case when only half of message is read in
	sys.stdout.write(sms)		#To print sms without newline
	sleep(1)					#Sleep time is more in order to make it more likely that full SMS is read by ser.read()
	if "CMT" in sms:
		handleSMS(sms)