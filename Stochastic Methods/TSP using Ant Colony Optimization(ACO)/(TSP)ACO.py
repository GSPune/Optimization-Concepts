from geopy.geocoders import Nominatim
import operator
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
# matplotlib.use('tkagg')
import math,random
import statistics  

class Ant:
    def __init__(self,id,ph,currentCity):
        self.id = id
        self.ph = ph
        self.allowedCities = [] #list of unvisited cities
        self.distanceTravelled = 0.0
        self.currentCity = currentCity
        self.route = []

    def chooseCity(self, pheromoneMatrix,distanceMatrix):
        if len(self.allowedCities) == 0: #all cities are visited
            return None
        selection = None
        factor,highestP = 0, 0
        for city in self.allowedCities:
              if distanceMatrix.at[self.currentCity.name,city] != 0.0:
                # print(f"Check :: {self.currentCity.name} and {city}")  
                 factor += (pheromoneMatrix.at[self.currentCity.name,city]/distanceMatrix.at[self.currentCity.name,city])
        if factor == 0:
            print(f"Factor is 0! i.e. {factor}")
            return None

        #after calculating denominator we can have probablity
        for city in self.allowedCities:
                if distanceMatrix.at[self.currentCity.name,city] != 0.0:
                    p = pheromoneMatrix.at[self.currentCity.name,city]/distanceMatrix.at[self.currentCity.name,city]
                    p /= factor
                    if (p) > highestP:
                        highestP = p
                        selection = city
        return selection #gets converted to city object

    def depositPheromone(self, pheromoneMatrix, distanceMatrix,nextCity): #on path(i,j)
        if distanceMatrix.at[self.currentCity.name,nextCity.name] != 0.0:
            delta = (1/distanceMatrix.at[self.currentCity.name,nextCity.name])
            pheromoneMatrix.at[self.currentCity.name,nextCity.name] += delta
            pheromoneMatrix.at[nextCity.name,self.currentCity.name] += delta
            self.ph -= delta

    def reset(self,initialPh):
        self.ph = initialPh
        self.allowedCities = []
        self.distanceTravelled = 0.0

    def __repr__(self):
        return f"Ant ({self.id}) with pheromone {self.ph} ml at Location {self.currentCity}" 

class City:
    #instance vars are x,y and name
    def __init__(self,x,y,name):
        self.x = x
        self.y = y
        self.name = name

    def __repr__(self):
        return self.name + "(" + str(self.x) + ", " + str(self.y) + ")"

def distance(C1,C2):
    d = math.sqrt((C1.x-C2.x)**2 + (C1.y-C2.y)**2)
    return d

#Edit
def getTotalDistance(route):
    dist = 0.0
    N = len(route)
    for i in range(0,N-1):
        dist += distance(route[i],route[i+1])

    dist += distance(route[0],route[N-1])
    return dist

#Edit this function!
def Plot(route,dist,Pnames):
    Pt = [[route[i].x,route[i].y] for i in range(len(route))]
    Pt += [[route[0].x,route[0].y]]
    Pt = np.array(Pt)
    #print(Pt[:,0])

    # plt.savefig('img.png')
    plt.title('(ACO)Total distance='+str(dist))
    plt.plot(Pt[:,0],Pt[:,1],'-o')

    for i in range(len(route)):
        plt.annotate(route[i].name,(Pt[i][0],Pt[i][1]))
    plt.show(block=False)
    plt.pause(0.01)  # Wait for t seconds 0.01
    plt.cla()

def getCityObj(name,citylist):
    for city in citylist:
        # print(city.name)
        if city.name == (name):
            return city
    print(f"City with name {name} not found?")
    return None

def readcities(Pnames):
    citylist = [] #co-ordinates of cities
    j = 0 #counter
    geolocator = Nominatim(user_agent="SG_App")
    with open("./india_cities.txt") as file:
        for line in file:
            city = line.rstrip("\n")
            if(city == ""):
                break
            Pnames.insert(j,city)#insert at jth position
            modifiedN = city + ", India"
            # city += ", India"
            pt = geolocator.geocode(modifiedN,timeout=10000)
            citylist.append(City(pt.latitude,pt.longitude,city))
            j += 1
    return citylist

#create a distance matrix
def distance_matrix(citylist,cityNames):
    l = len(citylist)
    DistanceMat = np.zeros((l,l)) #using numpy
    # np.fill_diagonal(nPyDistanceMat,0)
    df = pd.DataFrame(DistanceMat,index=cityNames,columns=cityNames)
    for r in df.index:
        for c in df.columns:
            if (r != c):
                c1 = getCityObj(r,citylist)
                c2 = getCityObj(c,citylist)
                df.at[r,c] = distance(c1,c2)
                df.at[c,r] = df.at[r,c]
    # print(df)
    return df # returns a data frame

def pheromoneMatrix(citylist, cityNames):
    l = len(citylist)
    pheromoneMat = np.full((l, l), 0.10)  # Initialize with 0.1
    # Convert to DataFrame with city names as index and columns
    df = pd.DataFrame(pheromoneMat, index=cityNames, columns=cityNames)
    return df

def createAntSample(m):
    pheromones = np.random.normal(loc=10, scale=1, size=m)
    ants = []
    for i in range(m):
        ants.append(Ant(i+1,pheromones[i],getCityObj('Pune',cities)))
    return ants

def antColonyOptimization(cities, pnames, m, maxIterations,rho):
    dM = distance_matrix(cities,pnames)
    pM = pheromoneMatrix(cities,pnames)
    ants = createAntSample(m)
    iters = 0
    bestTour = None
    bestDistance = float('inf')
    while iters < maxIterations:
        
        for ant in ants:
            if iters > 1:
               ant.reset(10.0)
            ant.allowedCities = pnames.copy()
            ant.allowedCities.remove('Pune')
            ant.route.append(ant.currentCity)

            for _ in range(len(cities)-1):

                newCity = getCityObj(ant.chooseCity(pM,dM),cities) #converted to a city object
                ant.depositPheromone(pM,dM,newCity)
                ant.route.append(newCity)
                ant.allowedCities.remove(newCity.name)
                ant.distanceTravelled += distance(newCity,ant.currentCity)
                ant.currentCity = newCity

            #go back to start
            # print(f"Here is the list of univisited cities :: {ant.allowedCities}")
            ant.distanceTravelled += distance(ant.route[0],ant.route[-1])
            if(ant.distanceTravelled < bestDistance):
                bestDistance = ant.distanceTravelled
                bestTour = ant.route

        # Multiply every element in the DataFrame by the evaporation factor
        pM *= rho

        if (iters % 10 == 0):
            print(f"Best Distance so far is {bestDistance}")
            # print(bestTour)
        Plot(bestTour,bestDistance,pnames)
        # print(pM)
        iters += 1

# def pheromoneEvap(): #?
#     pass

if __name__ == '__main__':
    m = 30
    iters = 120
    rho = 0.7

    pnames = []
    cities = readcities(pnames) #list of city objects
    antColonyOptimization(cities,pnames,m,iters,rho)

