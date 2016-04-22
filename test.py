import Adafruit_BBIO.GPIO as GPIO
from time import sleep

GPIO.setup("P9_23", GPIO.OUT, pull_up_down=GPIO.PUD_UP)
GPIO.output("P9_23", GPIO.HIGH)
sleep(10)
GPIO.cleanup()