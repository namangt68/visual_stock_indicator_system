#! /usr/bin python
####################################################################
# Naman Gupta
# Contact: namangt68@gmail.com
# Description: Test LEDs of vsis 
########################################################################
from time import sleep
import Adafruit_BBIO.GPIO as GPIO
name = input("Enter pin number: ")
name = str(name)
pin = "P8_" + name
GPIO.setup(pin, GPIO.OUT, pull_up_down=GPIO.PUD_UP)

GPIO.output(pin, GPIO.HIGH)
sleep(1)
GPIO.output(pin, GPIO.LOW)
sleep(1)
GPIO.output(pin, GPIO.HIGH)
sleep(1)

# GPIO.setup("P8_10", GPIO.OUT, pull_up_down=GPIO.PUD_UP)

# GPIO.output("P8_10", GPIO.HIGH)
# sleep(1)
# GPIO.output("P8_10", GPIO.LOW)
# sleep(1)
# GPIO.output("P8_10", GPIO.HIGH)
# sleep(1)

# GPIO.setup("P8_11", GPIO.OUT, pull_up_down=GPIO.PUD_UP)

# GPIO.output("P8_11", GPIO.HIGH)
# sleep(1)
# GPIO.output("P8_11", GPIO.LOW)
# sleep(1)
# GPIO.output("P8_11", GPIO.HIGH)
# sleep(1)


# GPIO.setup("P8_13", GPIO.OUT, pull_up_down=GPIO.PUD_UP)

# GPIO.output("P8_13", GPIO.HIGH)
# sleep(1)
# GPIO.output("P8_13", GPIO.LOW)
# sleep(1)
# GPIO.output("P8_13", GPIO.HIGH)
# sleep(1)

# GPIO.setup("P8_14", GPIO.OUT, pull_up_down=GPIO.PUD_UP)

# GPIO.output("P8_14", GPIO.HIGH)
# sleep(1)
# GPIO.output("P8_14", GPIO.LOW)
# sleep(1)
# GPIO.output("P8_14", GPIO.HIGH)
# sleep(1)


# GPIO.setup("P8_15", GPIO.OUT, pull_up_down=GPIO.PUD_UP)

# GPIO.output("P8_15", GPIO.HIGH)
# sleep(1)
# GPIO.output("P8_15", GPIO.LOW)
# sleep(1)
# GPIO.output("P8_15", GPIO.HIGH)
# sleep(1)

# GPIO.setup("P8_16", GPIO.OUT, pull_up_down=GPIO.PUD_UP)

# GPIO.output("P8_16", GPIO.HIGH)
# sleep(1)
# GPIO.output("P8_16", GPIO.LOW)
# sleep(1)
# GPIO.output("P8_16", GPIO.HIGH)
# sleep(1)

# GPIO.setup("P8_17", GPIO.OUT, pull_up_down=GPIO.PUD_UP)

# GPIO.output("P8_17", GPIO.HIGH)
# sleep(1)
# GPIO.output("P8_17", GPIO.LOW)
# sleep(1)
# GPIO.output("P8_17", GPIO.HIGH)
# sleep(1)





