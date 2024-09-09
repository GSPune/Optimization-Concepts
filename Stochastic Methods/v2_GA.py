from geopy.geocoders import Nominatim
import operator
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
# matplotlib.use('tkagg')
import math,random
import statistics  

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

def Plot(route,dist,Pnames):
    Pt = [[route[i].x,route[i].y] for i in range(len(route))]
    Pt += [[route[0].x,route[0].y]]
    Pt = np.array(Pt)
    #print(Pt[:,0])

    # plt.savefig('img.png')
    plt.title('(GA)Total distance='+str(dist))
    plt.plot(Pt[:,0],Pt[:,1],'-o')

    for i in range(len(route)):
        plt.annotate(route[i].name,(Pt[i][0],Pt[i][1]))
    plt.show(block=False)
    plt.pause(0.01)  # Wait for t seconds
    plt.cla()

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
                # citylist.insert(j,[pt.latitude,pt.longitude])
                citylist.append(City(pt.latitude,pt.longitude,city))
                j += 1
    return citylist

def createRoute(citylist):
    route = random.sample(citylist,len(citylist))
    return route

def initialPopulation(popSize,citylist):
    population = []
    for i in range(0,popSize):
        population.append(createRoute(citylist))
    return population

def rankRoutes(population):
    fitnessResult = {} #set ~ dict?
    for i in range(0,len(population)):
        fitnessResult[i] = Fitness(population[i]).getFitness()
    return sorted(fitnessResult.items(),key = operator.itemgetter(1),reverse=True)

#fittest is a list of tuples sorted in descending order
def createFittestPopulation(fittest,population,popRetention,popSize):
    eliteP = []
    retention = round(popRetention*popSize)
    subset = fittest[:retention]
    # print(subset)
    # print(f"Len of retained pop is {len(subset)}")
    for item in subset:
        eliteP.append(population[item[0]])
    return eliteP

# for cityR in topPop:
#     print(getTotalDistance(cityR), end=", ")
# print()

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

def mutation(child,chance):
    r = random.random()
    # chance = 0.04
    if(r > 1-chance):
        while(True):
            pos1 = (int((random.random()*1000)))%len(child)
            pos2 = (int((random.random()*1000)))%len(child)
            if pos1 != pos2: break
        #swap the cities aka genes
        child[pos1], child[pos2] = child[pos2], child[pos1]
        # print("mutation occured for child...with r = ", r)
        return child
    else:
        return child

def geneCrossover_Parents(elitePopulation,mutProb):
    nElite = len(elitePopulation)
    #Now we choose parents -- 1st Parent is the strongest and 2nd is chosen randomly
    p1 = elitePopulation[0]
    index = -1
    while(index < 0 or index==0 or index >= nElite):
        index = (int((random.random()*1000)))%nElite
    p2 = elitePopulation[index]
    child1 = createChild(p1,p2)
    child2 = createChild(p1,p2)
    #mutation by chance
    child1=mutation(child1,mutProb);child2=mutation(child2,mutProb)
    return [child1,child2]

def newGeneration(elitePopulation,popSize,popRetention,mutProb):
    maxChildren = round(0.3*popSize)
    childrenN = []
    #children are born
    for k in range(0,maxChildren):
        childrenN.extend(geneCrossover_Parents(elitePopulation,mutProb))    
    # print(f"The number of routes of all the children born is {len(childrenN)}")
    percentageChildren = ((1-popRetention)*100)/(2*maxChildren)
    elite_Children = createFittestPopulation(rankRoutes(childrenN),childrenN,percentageChildren,len(childrenN))
    # print(f"The number of routes in the fittest population is {len(elitePopulation)} and no. of routes in fittest children is {len(elite_Children)}\n\n")
    # print(len(elitePopulation+elite_Children))
    return elitePopulation+elite_Children #joining the 2 lists

def averageFittness(population):
    fitnessResult=[]
    for i in range(0,len(population)):
        fitnessResult.append(Fitness(population[i]).getFitness())
    fm = statistics.fmean(fitnessResult) 
    return fm   

def geneticAlgorithm(maxPopSize,mutProb,popRetention,maxPairs,maxGen):
    #read cities
    #gen init pop
    #create fittest subset and choose parents for mating
    #create 0.3popSize children and choose x% of them to make new gen
    #repeat procedure with new gen
    #termination condition
    #modify plotting func and animation
    #test out the code
    threshold = 1.0e-7
    Names,fittnessTrack = [],[]
    cities = readcities(Names)

    intialPop = initialPopulation(maxPopSize,cities)
    currentPopulation = intialPop
    fittnessTrack.append(averageFittness(currentPopulation))
    bestRoute = currentPopulation[0]
    bestDistAchieved = getTotalDistance(currentPopulation[0])
    print(f"Initial Dist is now {bestDistAchieved}")
    Plot(bestRoute,bestDistAchieved,Names)
    iters,retentC = 0,0
    while(True):
        
        fittestRanked = rankRoutes(currentPopulation)
        topPop = createFittestPopulation(fittestRanked,currentPopulation,popRetention,maxPopSize)

        new_population = newGeneration(topPop,maxPopSize,popRetention,mutProb)
        fittnessTrack.append(averageFittness(new_population))
        currentPopulation = new_population

        bestRoute = currentPopulation[0]
        bestDistAchieved = getTotalDistance(currentPopulation[0])
        
        Plot(bestRoute,bestDistAchieved,Names)
        iters+=1
        # print(iters)
        if(iters % 10 == 0):
            print(f"Fitness is now {fittnessTrack[iters]} for the {iters} iteration")
            print(f"Dist is now {bestDistAchieved}")
        relativeP = (fittnessTrack[iters]-fittnessTrack[iters-1])/(fittnessTrack[iters-1])
        if(abs(relativeP) < threshold):
            retentC+=1
        else: retentC = 0
        if retentC >= 4: 
            # print(relativeP)
            break
        if iters > maxGen: break

    print("\nFitness (final) is now: ",fittnessTrack[iters])
    print("Best distance achieved is ",bestDistAchieved)
    plt.close()
    input("...Press Enter to continue...View the fittness the graph")
    
    plt.plot(fittnessTrack)
    plt.xlabel('Generations')
    plt.ylabel('Average Fittness')
    plt.title('Increase in Fittness(GA)')
    plt.show()
    plt.pause(1)  # Wait for t seconds
    plt.cla()
   

if __name__ == '__main__':
    maxPopSize = 100
    mutProb = 0.05
    popRetention = 0.85
    maxPairs = 25
    maxGen = 100
    geneticAlgorithm(maxPopSize,mutProb,popRetention,maxPairs,maxGen)
