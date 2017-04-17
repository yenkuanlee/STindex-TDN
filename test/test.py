from geopy.distance import great_circle
newport_ri = (25,121)
cleveland_oh = (26, 121)
#print(great_circle(newport_ri, cleveland_oh).meters)
for i in range(1000000):
    a = great_circle(newport_ri, cleveland_oh).meters
