import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(7, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(15, GPIO.OUT, initial=GPIO.LOW)

def flash_led(channel):
    for i in range(5):
        GPIO.output(channel, GPIO.HIGH)
        sleep(.5)
        GPIO.output(channel, GPIO.LOW)
        sleep(.25)
