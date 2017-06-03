import sys
f1 = open(sys.argv[1],'r')
f2 = open(sys.argv[2],'r')

S1 = set()
S2 = set()

while True:
    line = f1.readline()
    if not line:break
    Sset = set()
    if "set" in line:
        tmp = line.split("set([")[1].split("L])")[0].split("L, ")
        for x in tmp:
            Sset.add(x)
    Max = 0
    for x in Sset:
        if int(x) > Max:
            Max = int(x)
    S1.add(Max)

while True:
    line = f2.readline()
    if not line:break
    Sset = set()
    if "set" in line:
        tmp = line.split("set([")[1].split("L])")[0].split("L, ")
        for x in tmp:
            Sset.add(x)
    Max = 0
    for x in Sset:
        if int(x) > Max:
            Max = int(x)
    S2.add(Max)

if S1!=S2:
    print (S2-S1)
    print ""
    print (S1-S2)
else:
    print S1
