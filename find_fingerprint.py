import adafruit_fingerprint
import serial
import time

uart = serial.Serial("/dev/ttyUSB0", baudrate=57600, timeout=1)
finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

def get_fingerprint():

    print("Waiting for image...")
    
#    while finger.get_image() != adafruit_fingerprint.OK:
#        pass
    start  = time.time()
    timeout = 1
##################
    while time.time()-start < timeout:
        i = finger.get_image()
        if i == adafruit_fingerprint.OK:
            print("Image taken")
            print("Templating...")
            if finger.image_2_tz(1) != adafruit_fingerprint.OK:
                return "none"
            print("Searching...")
            if finger.finger_search() != adafruit_fingerprint.OK:
                return None
            
            return finger.finger_id
        if i == adafruit_fingerprint.NOFINGER:
            print(".", end="")
    return "none"
    #################           
'''    print("Templating...")
    if finger.image_2_tz(1) != adafruit_fingerprint.OK:
        return False
    print("Searching...")
    if finger.finger_search() != adafruit_fingerprint.OK:
        return False
    return finger.finger_id
'''