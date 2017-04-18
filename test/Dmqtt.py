import paho.mqtt.client as mqtt
import time
import math

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

'''
def CheckPointInMcc(p,Mcc):
	global DistanceDict
	if len(Mcc) == 2:
		if DistanceDict[(Mcc[0],p)]**2 + DistanceDict[(Mcc[1],p)]**2 > DistanceDict[(Mcc[0],Mcc[1])]**2:
			return False
		else return True
	elif len(Mcc) == 3:
	else return "ERROR"

def GetNewMcc(p,OldMcc):
	global DistanceDict
	if len(Mcc) == 2:
		if DistanceDict[(Mcc[0],p)]**2 + DistanceDict[(Mcc[1],p)]**2 <= DistanceDict[(Mcc[0],Mcc[1])]**2:
			return OldMcc
		else:
'''
			
		
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	if msg.topic=='test':
		print str(msg.payload)
	elif msg.topic=='STevent':
		# Rule
		T = 1
		D = 100
		N = 2

		# Initial
		global EventDict
		global DistanceDict
		RedIndex = set()
		BlackIndex = set()
		Neighber = set()
		tmp = str(msg.payload).split("#")
		Lon = tmp[0]
		Lat = tmp[1]
		Time = tmp[2]

		Eid = long(str(time.time()).replace(".",""))

		# Generate Red, Black and Neighber
		for x in EventDict:
			Tdiff = Time - EventDict[x]["Time"]	############################
			if Tdiff <= 1 :
				RedIndex.add(x)
			elif Tdiff <= 2 and Tdiff > 1 :
				BlackIndex.add(x)
			else :
				EventDict.pop(x,None)
				continue
			DistanceTmp = distance(Lon,Lat,EventDict[x]["Lon"],EventDict[x]["Lat"]) <= (2*D)
			if DistanceTmp <= (2*D) :
				Neighber.add(x)
				DistanceDict[(x,Eid)] = DistanceTmp	# from small to large
		
		results = dict()


		# Get L2 and L3
		L2 = list()
		L3 = list()
		for x in Neighber:
			L2.append(set([x,Eid]),(x,Eid))
			for y in EventDict[x]["Neighber"]: # Eid > x > y
				if y not in Neighber:
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
					L3.append(set(y,x,Eid),diameter,Emax/2)
				else:
					S = (a+b+c)/2
					R = a*b*c/(4*math.sqrt(S*(S-a)*(S-b)*(S-c)))
					if R > 2*D:
						continue
					L3.append(set(y,x,Eid),(y,x,Eid),R)

		#results[0] = L2
		#results[1] = L3
		
		# L3 to Ln


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
		EventDict[Eid]["results"] = results

		print EventDict

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, 60)
client.loop_forever()
