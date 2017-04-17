import paho.mqtt.client as mqtt
import time

EventDict = dict()

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
		RedIndex = set()
		BlackIndex = set()
		Neighber = set()
		tmp = str(msg.payload).split("#")
		Lon = tmp[0]
		Lat = tmp[1]
		Time = tmp[2]

		# Generate Red, Black and Neighber
		for x in EventDict:
			Tdiff = Time - EventDict[x]["Time"]
			if Tdiff <= 1 :
				RedIndex.add(x)
			elif Tdiff <= 2 and Tdiff > 1 :
				BlackIndex.add(x)
			else :
				EventDict.pop(x,None)
				continue
			if distance(Lon,Lat,EventDict[x]["Lon"],EventDict[x]["Lat"]) <= (2*D) :
				Neighber.add(x)
		
		# Get L2
		L2 = set()
		for x in Neighber:
			for y in Neighber:
				if x > y : 
					if y in EventDict[x]["Neighber"]:
						L2.add((x,y))
					
				

		# Add To EventDict
		Eid = long(str(time.time()).replace(".",""))
		EventDict[Eid] = dict()
		EventDict[Eid]["Lon"] = Lon
		EventDict[Eid]["Lat"] = Lat
		EventDict[Eid]["Time"] = Time
		EventDict[Eid]["Neighber"] = Neighber

		print EventDict

		



client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, 60)
client.loop_forever()
