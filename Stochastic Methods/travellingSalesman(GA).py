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

def geneCrossover_Parents(elitePopulation):
    nElite = len(elitePopulation)
    #Now we choose parents -- 1st Parent is the strongest and 2nd is chosen randomly
    p1 = elitePopulation[0]
    while(index < 0 or index==0 or index >= nElite):
        index = (int((random.random()*1000)))%nElite
    p2 = elitePopulation[index]
    child1 = createChild(p1,p2)
    child2 = createChild(p1,p2)
    mutation(child1);mutation(child2)
    return child1,child2

def newGeneration(elitePopulation,popSize,):
    pass

def createChild(parent1,parent2):
    # choose two indices randomly to take a subset of p2
    c1 = [None]*len(parent2)

    while (True):
        i1 = (int((random.random()*1000)))%len(parent2)
        i2 = (int((random.random()*1000)))%len(parent2)
        diff = abs(i2-i1)
        if (diff > 0 and diff < (len(parent2)//2)): break

    start = min(i1,i2)
    end = max(i1,i2)
    #genes of the weaker parent
    for i in range(start,end+1,1):
        c1[i] = parent2[i]
    #note: 'r' is a city object
    counter = 0
    for r in parent1:
        if r not in c1:
            while(c1[counter] != None):
                counter+=1
            c1[counter] = r
            counter+=1
    return c1

def mutation(child,chance=0.04):
    r = random.random()
    # chance = 0.04
    if(r > 1-chance):
        while(True):
            pos1 = (int((random.random()*1000)))%len(child)
            pos2 = (int((random.random()*1000)))%len(child)
            if pos1 != pos2: break
        #swap the cities aka genes
        child[pos1], child[pos2] = child[pos2], child[pos1]
        return child
    else:
        return child
