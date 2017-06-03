import paho.mqtt.client as mqtt
import time
import datetime
import math
import os
from math import radians, cos, sin, asin, sqrt


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
    client.subscribe("test")
    client.subscribe("STevent")



def WriteOut(text):
	os.system("echo '"+text+"' >> OutputDmqtt.txt")

		
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	if msg.topic=='test':
		
		if "##" in str(msg.payload):
			time.sleep(5)
		WriteOut(str(msg.payload))
		
		#client.Tlist.append(str(msg.payload))
		#client.Tlist.append(str(msg.payload))
		#	WriteOut(str(msg.payload))

	
	if msg.topic=='STevent':
		print client._out_messages



client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.Tlist = list()

client.max_inflight_messages_set(200000)

client.connect("localhost", 1883, 60000)
client.loop_forever()
'''
client.loop_start()
while True:
	time.sleep(5)
	print client._in_messages
'''
