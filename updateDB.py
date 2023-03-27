import faceRecog
import RRead
import time
import lock
import userdb
import find_fingerprint
import exitfp
import lcd_display as lcd


path = '/home/pi/facial-recognition-main/db/user-login-register-firebase.json'
db = userdb.initializeDB(path)

while True:
#    lock.doorlock()
    authorizeduser =''
    authname = ''
    num = 0
    if num == 0:
                    #############  EXIT FP CODE    ###########
        exitempid= exitfp.get_fingerprint()

        if exitempid == None:
            lcd.display_msg('USER NOT FOUND ','   ACCESS DENIED!!  ')
            time.sleep(1.5)
            pass
        elif exitempid == 'none':
            pass
        else :
            st = time.time()
            username=userdb.get_empname(db,exitempid)
            exit = userdb.logout_entry(db,username)
            if exit == True:
                lock.doorunlock()
                print(time.time()-st)
                time.sleep(4)
            else:
                print('unable to open the door')
        num = 1

    ####################    EXIT CODE END     ###################
    
    rfid,rfid_username = RRead.readRfid()
    lcd.display_msg('USE RFID TAG OR ','    BIOMETRIC   ')
    if rfid_username != 'none' :
        print(rfid_username)
        if userdb.login_check(db,rfid_username):
                lcd.display_msg('  user already  ','   inside    ')
                continue
        user_auth = userdb.get_rfid(db,rfid)
        if user_auth == rfid_username:
            print('please look in the camera')
            lcd.display_msg('PLEASE LOOK IN  ','   THE CAMERA')
            time.sleep(1.5)
            try:
                (authorizeduser,authname) = faceRecog.Face(user_auth)
                print(authname)
                num = 0
            except TypeError:
                num = 0
                continue
        else:
            lcd.display_msg('  INVALID RFID  ','   ACCESS DENIED!!  ')
            time.sleep(1.5)
            #print(authorizeduser)
            num = 0
            
    else:    
        empid= find_fingerprint.get_fingerprint()

        if empid == None:
            lcd.display_msg('USER NOT FOUND ','   ACCESS DENIED!!  ')
            time.sleep(1.5)
            num = 0
            continue
        elif empid == 'none':
            num = 0
            continue
        else :
            
            username=userdb.get_empname(db,empid)
            if userdb.login_check(db,username):
                lcd.display_msg('  user already  ','   inside    ')
                continue
            print(username)
            num = 0
            if username == None:
                num = 0
                continue
            try:
                lcd.display_msg('PLEASE LOOK IN  ','   THE CAMERA')
                authorizeduser,authname = faceRecog.Face(username)
                print(authname)
                num = 0
            except TypeError:
                num = 0
                continue
            

        
        
    if authorizeduser == False:
            print("Face not match!! Access denied")
            lcd.display_msg('FACE NOT MATCHED ','  ACCESS DENIED!')
            time.sleep(1.5)
            
    
#     elif authorizeduser == '':
#         print('empty ')
#         time.sleep(2)
    else:    
        print('Access granted')
        #time.sleep(2)
        #print("string ",authorizeduser)
        #print(authname)
        #time.sleep(2)
        lcd.display_msg('FACE MATCHED ',' ACCESS GRANTED! ')
        st = time.time()
        imgUrl=userdb.uploadImage(authname,authname,authorizeduser)
        print(imgUrl)
        userdb.login_entry(db,authname,imgUrl)
        print('time to upload on db: ', time.time()-st)
        #print("door unlocks...")
        
        lock.doorunlock()

