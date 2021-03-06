import paho.mqtt.client as mqtt
import time
import datetime
import math
import os
from math import radians, cos, sin, asin, sqrt

EventDict = dict()
DistanceDict = dict()

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
    client.subscribe("test")
    client.subscribe("STevent")

def on_publish(client, userdata, mid):
    print("mid: "+str(mid))

def distance(lon1, lat1, lon2, lat2):
	"""
	Calculate the great circle distance between two points 
	on the earth (specified in decimal degrees)
	"""
	# convert decimal degrees to radians 
	lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
	# haversine formula 
	dlon = lon2 - lon1 
	dlat = lat2 - lat1 
	a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
	c = 2 * asin(sqrt(a)) 
	m = 6367 * c * 1000
	return m


def TimeDifference(TimeA,TimeB):
	tmpA = datetime.datetime.strptime(TimeA, "%Y/%m/%d").date()
	tmpB = datetime.datetime.strptime(TimeB, "%Y/%m/%d").date()
	DateDelta = ( tmpA - tmpB ).days
	if DateDelta < 0:
		DateDelta = (-1) * DateDelta
	return DateDelta
	

def CheckPointInMcc(p,Mcc):
	global DistanceDict
	for x in Mcc:
		if (x,p) not in DistanceDict:
			return False
	if len(Mcc) == 2:
		if DistanceDict[(Mcc[0],p)] > DistanceDict[(Mcc[0],Mcc[1])] or DistanceDict[(Mcc[1],p)] > DistanceDict[(Mcc[0],Mcc[1])] :
			return False
		if DistanceDict[(Mcc[0],p)]**2 + DistanceDict[(Mcc[1],p)]**2 > DistanceDict[(Mcc[0],Mcc[1])]**2:
			return False
		return True
	elif len(Mcc) == 3:
		# ABC vs P
		a = DistanceDict[(p,Mcc[0])] # PA
		b = DistanceDict[(p,Mcc[1])] # PB
		c = DistanceDict[(p,Mcc[2])] # PC
		Pmin = a
		Pmax = (b,c)
		brother = Mcc[0]
		Bmax = (DistanceDict[(Mcc[0],Mcc[1])],DistanceDict[(Mcc[0],Mcc[2])])
		Base = DistanceDict[(Mcc[1],Mcc[2])]
		
		if b < Pmin:
			Pmin = b
			Pmax = (a,c)
			brother = Mcc[1]
			Bmax = (DistanceDict[(Mcc[0],Mcc[1])],DistanceDict[(Mcc[1],Mcc[2])])
			Base = DistanceDict[(Mcc[0],Mcc[2])]
		if c < Pmin:
			Pmin = c
			Pmax = (a,b)
			brother = Mcc[2]
			Bmax = (DistanceDict[(Mcc[0],Mcc[2])],DistanceDict[(Mcc[1],Mcc[2])])
			Base = DistanceDict[(Mcc[0],Mcc[1])]

		if Pmax[0]**2 + Pmax[1]**2 <= Base**2:	# degree more than 90
			return True

		CosP = (Pmax[0]**2 + Pmax[1]**2 - Base**2) / (2*Pmax[0]*Pmax[1])
		CosB = (Bmax[0]**2 + Bmax[1]**2 - Base**2) / (2*Bmax[0]*Bmax[1])
		if CosP <= CosB :
			return True
		return False

'''
def GetNewMcc(p,OldMcc):
	global DistanceDict
	if len(Mcc) == 2:
		if DistanceDict[(Mcc[0],p)]**2 + DistanceDict[(Mcc[1],p)]**2 <= DistanceDict[(Mcc[0],Mcc[1])]**2:
			return OldMcc
		else:
'''

def WriteOut(text):
	os.system("echo '"+text+"' >> OutputDmqtt.txt")

EEid = 0		
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	global EEid
	if msg.topic=='test':
		#print str(msg.payload)
		WriteOut(str(msg.payload))
	elif msg.topic=='STevent':
		#print time.time()
		WriteOut("Time : "+str(time.time()))
		# Rule
		T = 30
		D = 100
		N = 10

		# Initial
		global EventDict
		global DistanceDict
		RedIndex = set()
		BlackIndex = set()
		Neighber = set()
		tmp = str(msg.payload).split("#")
                try:
		    Lon = float(tmp[0])
		    Lat = float(tmp[1])
		    Time = tmp[2]
                except:
                    return

		#Eid = long(str(time.time()).replace(".",""))
		Eid = long(EEid)
		EEid += 1

		# Generate Red, Black and Neighber
		PopList = list()
		for x in EventDict:
			Rflag = False
			Bflag = False
			Tdiff = TimeDifference(Time,EventDict[x]["Time"]) #######################
			if Tdiff <= 1*T :
				#RedIndex.add(x)
				Rflag = True
			elif Tdiff <= 2*T and Tdiff > 1*T :
				#BlackIndex.add(x)
				Bflag = True
			else :
				#EventDict.pop(x,None)
				#print "KEVIN OLD POINT : "+str(x)
				PopList.append(x)
				continue

			
			DistanceTmp = distance(Lon,Lat,EventDict[x]["Lon"],EventDict[x]["Lat"])
			#print "KEVIN DISTANCE : "+str(DistanceTmp)
			if DistanceTmp <= (2*D) :
				if Rflag:
					RedIndex.add(x)
				if Bflag:
					BlackIndex.add(x)
				Neighber.add(x)
				DistanceDict[(x,Eid)] = DistanceTmp	# from small to large
				DistanceDict[(Eid,x)] = DistanceTmp	# from large to small

		RedIndex.add(Eid)
		Dpop = set()
		for x in PopList:
			del EventDict[x]
			for y in DistanceDict:
				if x in y:
					Dpop.add(y)
		for x in Dpop:
			del DistanceDict[x]

		# Get Mcc about Eid (2-point and 3-point)
		Mcc = dict()

		for x in Neighber:
			Mcc[(x,Eid)] = set([x,Eid])	# 2-point Mcc
			for y in EventDict[x]["Neighber"]: # Eid > x > y
				if y not in Neighber or y not in EventDict:
					continue
				a = DistanceDict[(x,Eid)]
				b = DistanceDict[(y,Eid)]
				c = DistanceDict[(y,x)]
				Emax = a
				Emin = (b,c)
				diameter = (x,Eid)
				if b > Emax:
					Emax = b
					Emin = (a,c)
					diameter = (y,Eid)
				if c > Emax:
					Emax = c
					Emin = (a,c)
					diameter = (y,x)

				if Emin[0]**2 + Emin[1]**2 <= Emax**2:
					Mcc[diameter] = set([y,x,Eid])	# 3 point in 2-point Mcc
				else:
					S = (a+b+c)/2
                                        try:
					    R = a*b*c/(4*math.sqrt(S*(S-a)*(S-b)*(S-c)))
                                        except:
                                            continue
					if R > D:
						continue
					Mcc[(y,x,Eid)] = set([y,x,Eid])	# 3-point Mcc

		###print "KEVIN Eid : "+str(Eid)
		#print "KEVIN DistanceDict : "
		#print DistanceDict
		#print "KEVIN NEIGHBER : "
		#print Neighber
		
		for p in Neighber:
			for mcc in Mcc:
				if CheckPointInMcc(p,mcc):
					Mcc[mcc].add(p)
		
		# Get Score of Mcc about Eid
		for mcc in Mcc:
			Pnumber = len(Mcc[mcc])
			RedNumber = len(Mcc[mcc]&RedIndex)
			BlackNumber = Pnumber - RedNumber
			if BlackNumber == 0 :
				###WriteOut(str(mcc))
				###WriteOut(str(Mcc[mcc]))
				#print mcc
				#print Mcc[mcc]
				continue
			if RedNumber / BlackNumber >= N:
				WriteOut(str(mcc))
				WriteOut(str(Mcc[mcc]))
				#print mcc
				#print Mcc[mcc]

		# Get Score of Mcc about Eid's Neighber
		MccPop = set()
		for x in Neighber:
			for mcc in EventDict[x]["Mcc"]:
				if mcc[0] not in RedIndex and mcc[0] not in BlackIndex :
					#EventDict[x]["Mcc"].pop(mcc,None)
					MccPop.add((x,mcc))
					continue
				if CheckPointInMcc(Eid,mcc):
					EventDict[x]["Mcc"][mcc].add(Eid)
				else:
					continue
				Pnumber = len(EventDict[x]["Mcc"][mcc])
				RedNumber = len(EventDict[x]["Mcc"][mcc]&RedIndex)
				BlackNumber = len(EventDict[x]["Mcc"][mcc]&BlackIndex)
				if BlackNumber == 0:
					###WriteOut(str(mcc))
					###WriteOut(str(EventDict[x]["Mcc"][mcc]))
					#print mcc
					#print EventDict[x]["Mcc"][mcc]
					continue
				if RedNumber / BlackNumber >= N:
					WriteOut(str(mcc))
					WriteOut(str(EventDict[x]["Mcc"][mcc]))
					#print mcc
					#print EventDict[x]["Mcc"][mcc]
				
		for x in MccPop:
			EventDict[x[0]]["Mcc"].pop(x[1],None)

		'''
		# Get L2
		L2 = list()
		for x in Neighber:
			for y in EventDict[x]["Neighber"]:
				if y in Neighber :
					# (EventSet,MCC)
					L2.append(list([y,x]),(y,x))	# from small to large
		results[0] = L2
		# Get Ln
		for x in Neighber:
			 for i in range(len(EventDict[x]["results"])):
				for y in EventDict[x]["results"][i]:	# (EventSet,MCC)
					Ltmp = list()
					Lflag = False
					for z in y[0]:
						if z in Neighber:
							Ltmp.append(z)
						else:
							Lflag = True
							break
					if Lflag : continue
					Ltmp.append(x)
					if i+1 not in results:
						results[i+1] = list()
					# Get MCC of Ltmp !!!
					OldMcc = y[1]
					NewMcc = GetMcc(x,OldMcc)	############################
					results[i+1].append(Ltmp,NewMcc)
		'''


		# Add To EventDict

		EventDict[Eid] = dict()
		EventDict[Eid]["Lon"] = Lon
		EventDict[Eid]["Lat"] = Lat
		EventDict[Eid]["Time"] = Time
		EventDict[Eid]["Neighber"] = Neighber
		EventDict[Eid]["Mcc"] = Mcc



client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, 0)
client.loop_forever()
