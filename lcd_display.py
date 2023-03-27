from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD
import time
lcd = LCD()
def safe_exit(signum, frame):
    exit(1)
def display_msg(msg1,msg2):

        lcd.clear()
        signal(SIGTERM, safe_exit)
        signal(SIGHUP, safe_exit)
        lcd.text(msg1,1)
        lcd.text(msg2,2)
        time.sleep(0.5)
    #except KeyboardInterrupt:
     #   pass
    #finally:
        #lcd.clear()