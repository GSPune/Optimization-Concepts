from geopy.geocoders import Nominatim
from numpy import *
from pylab import *
import math

def readcities(Pnames):
    p = [] #co-ordinates of cities
    j = 0 #counter
    geolocator = Nominatim(user_agent="SG_App")

    with open("./india_cities.txt") as file:
        with open('output.txt','w') as out:
            for line in file:
                city = line.rstrip("\n")
                if(city == ""):
                    break
                Pnames.insert(j,city)
                city += ", India"
                pt = geolocator.geocode(city,timeout=10000)
                #  out.write("City = ",city,pt.latitude,pt.longitude)
                out.write(f"City = {city} {pt.latitude},{pt.longitude} \n")
                # out.write('/n')
                p.insert(j,[pt.latitude,pt.longitude])
                j += 1
    return p

Pnames = []
P = readcities(Pnames)
print(f"Number of cities is {len(P)}.")


def distance(P1,P2):
    d = math.sqrt((P1[0]-P2[0])**2 + (P1[1]-P2[1])**2)
    return d


#d1 = distance([23.0215374,72.5800568],[31.6343083,74.8736788])
#print(d1)

def totalDistance(P,seq):
    dist = 0.0
    N = len(seq)
    for i in range(0,N-1):
        dist += distance(P[seq[i]],P[seq[i+1]])
    
    dist += distance(P[0],P[seq[N-1]])
    return dist

s = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]
#print("Total Distance::",totalDistance(P,s))

def Plot(seq,P,dist,Pnames):
    Pt = [P[seq[i]] for i in range(len(seq))]
    Pt += [P[seq[0]]]
    Pt = array(P)
    title('Total distance='+str(dist))
    plot(Pt[:,0],Pt[:,1],'-o')
    for i in range(len(P)):
    	annotate(Pnames[i],(P[i][0],P[i][1]))
    show()

Plot(s,P,506.75,Pnames)