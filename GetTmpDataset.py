# -*- coding: utf-8 -*-
import csv
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
f = open(sys.argv[1], 'r')
while True:
    line = f.readline()
    if not line:break
    line = line.replace("\n","")
    line = line.replace("\r","")
    X = ""
    for x in line:
        try:
            int(x)
            X += x
        except:
            if x=="/" or x=="." or x==",":
                X += x
    print X
