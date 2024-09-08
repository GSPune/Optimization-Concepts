from geopy.geocoders import Nominatim
from numpy import *
from pylab import *
import operator
import matplotlib
import matplotlib.pyplot as plt
# matplotlib.use('tkagg')
import math,random

class City:
    #instance vars are x,y and name
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
        self.routeDistance()
        self.fitness = 1.0/self.distance
        return self.fitness


def distance(C1,C2):
    d = math.sqrt((C1.x-C2.x)**2 + (C1.y-C2.y)**2)
    return d

def getTotalDistance(route):
    dist = 0.0
    N = len(route)
    for i in range(0,N-1):
        dist += distance(route[i],route[i+1])

    dist += distance(route[0],route[N-1])
    return dist

def readcities():
    citylist = [] #co-ordinates of cities
    j = 0 #counter
    geolocator = Nominatim(user_agent="SG_App")

    with open("./india_cities.txt") as file:
        with open('output.txt','w') as out:
            for line in file:
                city = line.rstrip("\n")
                if(city == ""):
                    break
                # Pnames.insert(j,city)#insert at jth position
                city += ", India"
                pt = geolocator.geocode(city,timeout=10000)
                #  out.write("City = ",city,pt.latitude,pt.longitude)
                out.write(f"City = {city} {pt.latitude},{pt.longitude} \n")
                # out.write('/n')
                # citylist.insert(j,[pt.latitude,pt.longitude])
                citylist.append(City(pt.latitude,pt.longitude,city))
                j += 1
    return citylist

cities = readcities()

def createRoute(citylist):
    route = random.sample(citylist,len(citylist))
    return route

def initialPopulation(popSize,citylist):
    population = []
    for i in range(0,popSize):
        population.append(createRoute(citylist))
    return population

pop = initialPopulation(10,cities)

def rankRoutes(population):
    fitnessResult = {} #set ~ dict?
    for i in range(0,len(population)):
        fitnessResult[i] = Fitness(population[i]).getFitness()
    return sorted(fitnessResult.items(),key = operator.itemgetter(1),reverse=True)

#fittest is a list of tuples sorted in descending order
def createFittestPopulation(fittest,population,popRetention,popSize):
    eliteP = []
    retention = int(popRetention*popSize)
    subset = fittest[:retention]
    for item in subset:
        eliteP.append(population[item[0]])
    return eliteP

# fitt = rankRoutes(pop)
# topPop = createFittestPopulation(fitt,pop,0.85,10)
# for cityR in topPop:
#     print(getTotalDistance(cityR), end=", ")
# print()

def geneCrossover(elitePopulation):
    nElite = len(elitePopulation)
    #Now we choose parents -- 1st Parent is the strongest and 2nd is chosen randomly
    p1 = elitePopulation[0]
    while(index < 0 or index==0 or index >= nElite):
        index = (int((random.random()*1000)))%nElite
    p2 = elitePopulation[index]
    # choose two indices randomly to take a subset of p2
    while (True):
        i1 = (int((random.random()*1000)))%len(p2)
        i2 = (int((random.random()*1000)))%len(p2)
        diff = abs(i2-i1)
        if (diff > 0 and diff < (len(p2)//2)): break

    start = min(i1,i2)
    end = max(i1,i2)