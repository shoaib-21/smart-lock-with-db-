import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time

def readRfid():
    start = time.time()
    timeout = 1 

    while time.time()- start <= timeout:
       # GPIO.cleanup()
        #time.sleep(1)
        try:
            print("place rfid tag....")
            status,TagType = SimpleMFRC522().read_no_block()
            print(status)
            if status == None:
                print("card not found")
            elif status != 'None':
                id,text = SimpleMFRC522().read()
                print('id :', id)
                print(text.strip())
                return id,text.strip()
                
                
        finally:
            GPIO.cleanup()
    return "none" , "none"

