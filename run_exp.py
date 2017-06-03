import paho.mqtt.client as paho
import datetime
import sys
import os
import time
f = open(sys.argv[1],'r')
Tlist = list()
while True:
    line = f.readline()
    if not line:break
    line = line.replace("\n","")
    tmp = line.split(",")
    Tlist.append((tmp[1],tmp[2],tmp[0],datetime.datetime.strptime(tmp[0], "%Y/%m/%d").date()))


Tlist.sort(key=lambda tup: tup[3]) 


def on_publish(client, userdata, mid):
        print("mid: "+str(mid))

client = paho.Client()
client.connect("140.92.143.212", 1883)

cnt = 0
for x in Tlist:
    try:
        if x[0]!="" and x[1] != "" or x[2]!="":
            #os.system("python Mmqtt.py 140.92.143.212 test "+x[0]+"#"+x[1]+"#"+x[2])
            client.publish("test", x[0]+"#"+x[1]+"#"+x[2], qos=1)
	    cnt += 1
            #time.sleep(0.001)

    except:
        pass

print cnt
