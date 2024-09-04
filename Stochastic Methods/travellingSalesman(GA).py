from geopy.geocoders import Nominatim
from numpy import *
from pylab import *
import matplotlib
import matplotlib.pyplot as plt
# matplotlib.use('tkagg')
import math,random

def readcities(Pnames):
    citylist = [] #co-ordinates of cities
    j = 0 #counter
    geolocator = Nominatim(user_agent="SG_App")

    with open("./india_cities.txt") as file:
        with open('output.txt','w') as out:
            for line in file:
                city = line.rstrip("\n")
                if(city == ""):
                    break
                Pnames.insert(j,city)#insert at jth position
                city += ", India"
                pt = geolocator.geocode(city,timeout=10000)
                #  out.write("City = ",city,pt.latitude,pt.longitude)
                out.write(f"City = {city} {pt.latitude},{pt.longitude} \n")
                # out.write('/n')
                citylist.insert(j,[pt.latitude,pt.longitude])
                j += 1
    return citylist

class City:
    def __init__(self,x,y,name):
        self.x = x
        self.y = y
        self.name = name

    def __repr__(self):
        return self.name + "(" + str(self.x) + ", " + str(self.y) + ")"
    
class Fitness:
    def __init__(self,route):
        self.route = route
        self.distance = 0.0
        self.fitness = 0.0

    def routeDistance(self):
        self.distance = getTotalDistance(self.route)

    def getFitness(self):
        self.fitness = 1.0/self.distance
        return self.fitness


def distance(P1,P2):
    d = math.sqrt((P1[0]-P2[0])**2 + (P1[1]-P2[1])**2)
    return d

def getTotalDistance(P,seq):
    dist = 0.0
    N = len(seq)
    for i in range(0,N-1):
        dist += distance(P[seq[i]],P[seq[i+1]])

    dist += distance(P[0],P[seq[N-1]])
    return dist

def createRoute(citylist):
    route = random.sample(citylist,len(citylist))
    return route

def initialPopulation(popSize,citylist):
    pass
