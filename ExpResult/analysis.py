import sys
f = open(sys.argv[1],'r')
f2 = open(sys.argv[2],'r')
Elist = list()
while True:
        line = f.readline()
        if not line:break
        if "Time : " in line:
                Elist.append(float(line.split("Time : ")[1].split("\n")[0]))

Elist2 = list()
while True:
        line = f2.readline()
        if not line:break
        if "Time : " in line:
                Elist2.append(float(line.split("Time : ")[1].split("\n")[0]))

Mlen = len(Elist)
if len(Elist2) > len(Elist):
        Mlen = len(Elist2)
		
for i in range(Mlen):
        Y1 = ""
        Y2 = ""
        try:
                Y1 = str(Elist[i]-Elist[0])
        except:
                pass
        try:
                Y2 = str(Elist2[i]-Elist2[0])
        except:
                pass
        print str(i)+"\t"+str(Y1)+"\t"+str(Y2)