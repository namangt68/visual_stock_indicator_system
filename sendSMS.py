#! /usr/bin python
####################################################################
# sendSMS.py
# Send the SMS 
# Gopal Krishan Aggarwal
# April 22, 2016
# Contact: gopalkriagg@gmail.com
# Description: Keeps listening to new SMSes and whenever an SMS is received it
# prints it to console.
########################################################################
import serial
from time import sleep

ser = serial.Serial('/dev/ttyO1', 9600, timeout = 1)
def sendSMS(phoneNum, msg) :
  ser.flushOutput()
  print("Sending SMS to "),
  print phoneNum
  ser.write("AT+CMGF=1\r\n")    #Because we want to send the SMS in text mode. Prints data to the serial port as human-readable ASCII text followed by a carriage return character (ASCII 13, or '\r') and a newline character (ASCII 10, or '\n').
  sleep(0.5)                    #On shorter delays it does not work
  ser.write("AT+CMGS=\"")
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

sendSMS("+919816923467", "Hey there!")