import RPi.GPIO as GPIO
from time import sleep


def doorunlock():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)
    GPIO.output(18, 0)
    sleep(3)
    GPIO.output(18, 1)
    GPIO.cleanup()
    
    
def doorlock():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)
    sleep(0.5)
    GPIO.cleanup()
