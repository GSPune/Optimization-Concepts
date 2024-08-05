from geopy.geocoders import Nominatim
# from numpy import *
import math

def readcities():
    p = [] #co-ordinates of cities
    j = 0 #counter
    geolocator = Nominatim(user_agent="SG_App")

    with open("./india_cities.txt") as file:
        with open('output.txt','w') as out:
            for line in file:
                city = line.rstrip("\n")
                if(city == ""):
                    break
                city += ", India"
                pt = geolocator.geocode(city,timeout=10000)
                #  out.write("City = ",city,pt.latitude,pt.longitude)
                out.write(f"City = {city} {pt.latitude},{pt.longitude} \n")
                # out.write('/n')
                p.insert(j,[pt.latitude,pt.longitude])
                j += 1
    return p

# P = readcities()
# print(f"Number of cities is {len(P)}.")


def distance(P1,P2):
    d = math.sqrt((P1[0]-P2[0])**2 + (P1[1]-P2[1])**2)
    return d


d1 = distance([23.0215374,72.5800568],[31.6343083,74.8736788])
print(d1)

def totalDistance(P,seq):
    dist = 0.0
    N = len(seq)
    for i in range(0,N-1):
        dist += distance(P[seq[i]],P[seq[i+1]])
    
    dist += distance(P[0],P[seq[N-1]])
    return dist

def plot():
    pass

