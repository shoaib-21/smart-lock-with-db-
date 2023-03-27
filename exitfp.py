import adafruit_fingerprint
import serial
import time

uart = serial.Serial("/dev/ttyUSB1", baudrate=57600, timeout=1)
finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

def get_fingerprint():

    print("exit Waiting for image...")
    

    start  = time.time()
    timeout = 1
##################
    while time.time()-start < timeout:
        i = finger.get_image()
        if i == adafruit_fingerprint.OK:
            print(" exit Image taken")
            print(" exit Templating...")
            if finger.image_2_tz(1) != adafruit_fingerprint.OK:
                return "none"
            print("Searching...")
            if finger.finger_search() != adafruit_fingerprint.OK:
                return None
            return finger.finger_id
        if i == adafruit_fingerprint.NOFINGER:
            print(".", end="")
            #return "none"
    return "none"
    #################           
