import paho.mqtt.client as mqtt #import the client1
import time 
def on_log(client, userdata, level, buf):
    print("log: ",+buf)
    
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(" vs connected OK rc = ",str(rc)," flags = ",str(flags))
    else:
        print("Bad connection returned code : ",rc)
def on_disconnect(client, userdata, flags, rc=0):
    print("disconnected result code:" +str(rc))
    
def on_message(client, userdata,msg):
    topic = msg.topic
    m_decode=str(msg.payload.decode("utf-8","ignore"))
    print("msg =" ,m_decode)
broker_address= "tcp://4.tcp.ngrok.io"
#broker_address="iot.eclipse.org"
client = mqtt.Client("P6549655") #create new instance
client.on_connect = on_connect
client.on_disconnect = on_disconnect
#client.on_log = on_log
client.on_message=on_message
#print("connecting to broker ",broker_address)
client.username_pw_set("mna","mna0845")
client.connect(broker_address,17103,150)#connect to broker
client.loop_start()
messg = input('enter ur msg: ')
#while True:
client.publish("addUser",payload=messg,qos=1,retain=True)
    # time.sleep(2)
client.loop_stop()
client.disconnect()
#client.loop_forever()
