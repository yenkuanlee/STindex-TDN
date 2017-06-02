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

for x in Tlist:
    #print x[0],x[1],x[2]
    os.system("python Mmqtt.py 140.92.143.212 STevent "+x[0]+"#"+x[1]+"#"+x[2])
    #time.sleep(1)
