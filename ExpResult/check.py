import sys
f1 = open(sys.argv[1],'r')
f2 = open(sys.argv[2],'r')

S1 = set()
S2 = set()

while True:
    line = f1.readline()
    if not line:break
    if line[0]=="(":
        S1.add(line)

while True:
    line = f2.readline()
    if not line:break
    if line[0]=="(":
        S2.add(line)

print len(S2-S1)
print ""
print len(S1-S2)
