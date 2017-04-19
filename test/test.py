import datetime
import sys
import os
import time
f = open(sys.argv[1],'r')
Tlist = list()
while True:
    line = f.readline()
    if not line:break
    tmp = line.split(",")
    tmp[0] = tmp[0].replace(tmp[0].split("/")[0],str(int(tmp[0].split("/")[0])+1911))
    #Time = str(int(tmp[0].split("/")[0])+1911)+"/"+tmp
    Tlist.append((tmp[5],tmp[6],tmp[0],datetime.datetime.strptime(tmp[0], "%Y/%m/%d").date()))


Tlist.sort(key=lambda tup: tup[3]) 

for x in Tlist:
    #print x[0],x[1],x[2]
    os.system("python Mmqtt.py 140.92.143.140 STevent "+x[0]+"#"+x[1]+"#"+x[2])
    time.sleep(1)
