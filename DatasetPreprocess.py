import sys
f = open(sys.argv[1],'r')
Ddict = dict()
while True:
    line = f.readline()
    if not line:break
    line = line.replace("\n","")
    tmp = line.split(",")
    L = list()
    try:
        int(tmp[0])
        Date = tmp[1]
        Jin = tmp[6].replace("\n","")
        Wei = tmp[5]
        print Date+","+Jin+","+Wei
    except:
        continue
        # somthing error = =
        try:
            Date = tmp[1]
            line = f.readline()
            line = line.replace("\n","")
            tmp = line.split(",")
            Jin = tmp[3]
            Wei = tmp[2]
            print "KEVIN"
            print Date+","+Jin+","+Wei
        except:
            pass
