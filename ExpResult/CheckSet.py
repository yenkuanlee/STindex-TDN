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
    S1.add(frozenset(Sset))

while True:
    line = f2.readline()
    if not line:break
    Sset = set()
    if "set" in line:
        tmp = line.split("set([")[1].split("L])")[0].split("L, ")
        for x in tmp:
            Sset.add(x)
    S2.add(frozenset(Sset))

print (S2-S1)
print ""
print len(S1-S2)
