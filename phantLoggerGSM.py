#! /usr/bin/python
####################################################################
# phant-loggerGSM.py
# Logs data to phant from a file
# Gopal Krishan Aggarwal
# April 23, 2016 
# Contact: gopalkriagg@gmail.com
# Description: This piece of code reads data from a file 
# from nth line and tries to write this data to cloud through GSM
# module. When succesful in writing this data it increments this number 'n'
# stored in a separate file named 'lineToBeUploadedNext.txt' and tries to
# now upload the n+1th line if it exists and goes so on. 
# It also logs almost each action it takes into a file named log in the same folder.
########################################################################

import os
import urllib
import serial
import time
from bash import bash
script_dir = os.path.dirname(os.path.realpath(__file__))  #Get the directory where this script is located
log = open(script_dir + "/log", 'a', 1)

def gsmupload(privateKey, publicKey, params): 	#Tries to upload the data
	#b = str(bash("ls /dev | grep ttyUSB | head -n 1").value())
	#ser = serial.Serial('/dev/'+b,9600,timeout=1)
	ser = serial.Serial('/dev/ttyO1', 9600, timeout = 1) 
	ser.flush()
	ser.flushInput()
	ser.flushInput()
	ser.flushInput() #I feel there is need of more flushing as sometimes there is still data in buffer
	ser.flushOutput()

	time.sleep(1)
	ser.write('AT+CIPSHUT\r\n')
	time.sleep(1)
	x = ser.read(50)
	print x
	log.write(x)
	time.sleep(0.5)
	ser.flushInput()

	ser.write('AT+CSTT="airtelgprs.com","",""\r\n') #airtelgprs.com for airtel
	time.sleep(1)
	x = ser.read(50)
	print x
	log.write(x)
	ser.flushInput()


	ser.write('AT+CIICR\r\n')
	time.sleep(1)
	x = ser.read(50)
	print x
	log.write(x)
	ser.flushInput()

	time.sleep(5)

	ser.write('AT+CIFSR\r\n')
	time.sleep(0.1)
	x = ser.read(50)
	print x
	log.write(x)
	ser.flushInput()


	ser.write('AT+CIPSTART="TCP","54.86.132.254","80"\r\n') #Sparkfun data.sparkfun.com:  54.86.132.254
	time.sleep(3)  	#Sometimes it takes more time for connection (i.e. for "CONNECT OK" response)
	x = ser.read(100)
	print x
	log.write(x)
	ser.flushInput()

	ser.write('AT+CIPSEND\r\n')
	time.sleep(0.1)
	x = ser.read(50)
	print x
        log.write(x)	
	ser.flushInput()
	
	request = 'GET /input/' + publicKey + '?private_key=' + privateKey + '&' + params + ' HTTP/1.1\r\n\r\n'
	print request
        log.write(x)
	ser.write(request)
	time.sleep(1)
	x = ser.read(50)
	print x
        log.write(x)
	ser.flushInput()

	ser.write(chr(26))
	time.sleep(5) #Give time to send data
	
	x = ser.read(200)
	print x
	log.write(x)
	s = x
	
	ser.flushInput()

	time.sleep(1)
	x = ser.read(300)
	print x
        log.write(x)
	y = ser.read(300)
	print y
	z = ser.read(300)
	print z
	s = s + x + y + z
	log.write(s)
	if "1 success" in s or "200 OK" in s or "SEND OK" in s:
		response = "success"
	else:
		response = "failure"	
	ser.flushInput()

	ser.write('AT+CIPSHUT\r\n')
	x =  ser.read(50)
	print x
	log.write(x)
	ser.flushInput()
	time.sleep(20)
	ser.flushInput()
	ser.close()
	return response



#Get the line to be uploaded next. If file not found lineToBeUploadedNext will be 0. (This line to be uploaded is located in another file named weatherLocalCopy.data)
lineToBeUploadedNextFile = os.path.join(script_dir, "lineToBeUploadedNext.txt")
if os.path.isfile(lineToBeUploadedNextFile) : #True if file exists
	numberFile = open(lineToBeUploadedNextFile) #Default open mode is read
	lineToBeUploadedNext = int(numberFile.read())
	numberFile.close()
else :
	lineToBeUploadedNext = 0

print "Line to be uploaded Next: " + str(lineToBeUploadedNext)


#################
## Phant Stuff ##
#################
server = "54.86.132.254" # This is the IP of data.sparkfun.com. Using IP instead of hostname may cause trouble in future if data.sparkfun.com changes their IP
publicKey = "ZGoYlZXwRoCqpMNGON70"
privateKey = "2mMjEV69NMc9NnpboprE" 

############################################
##Read sensor data from file and upload it##
############################################
data = {}
fields = ["hc", "i", "stock", "ts"] # Weather fields
recordsFile = os.path.join(script_dir, "records")

f = open(recordsFile)
for i, line in enumerate(f):
	if i >= lineToBeUploadedNext:
		print "Value of i is: " + str(i)
		array = line.split(',')
		print array
		for j in range(0, len(fields)):
			data[fields[j]] = array[j] #In Phant all data is logged as String. Source: http://phant.io/docs/input/http/
		params = urllib.urlencode(data)
		print data
	        log.write(str(data))
		print params
	        log.write(params)
		response = gsmupload(privateKey, publicKey, params)
		print response
	        log.write(response)
		count = 0
		resetCount = 0
		while not response == "success" :
			response = gsmupload(privateKey, publicKey, params)
			count += 1
			if count > 3:
				resetGSMModule() #Simulating ejecting and reinserting the module if even after 3 times data is not uploaded
				resetCount += 1
				if (resetCount > 3):
					print "Going to restart GSM Module" #Power off and power on GSM Module if after lot of tries data is not uploaded
					restartGSMModule()
		lineToBeUploadedNext += 1
		fp = open(lineToBeUploadedNextFile, 'w', 0)	#Update the line to be uploaded next
		fp.write(str(lineToBeUploadedNext)) #Doubt as to what will happen when power goess off at this line
		fp.close()
f.close()
