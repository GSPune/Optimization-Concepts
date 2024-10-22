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
    def __init__(self,ph,id):
        self.id = id
        self.ph = ph

    def __repr__(self):
        return "Ant" + "(" + self.id + ")"

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
    plt.pause(0.01)  # Wait for t seconds
    plt.cla()

def getCityObj(name,citylist):
    for city in citylist:
        # print(city.name)
        if city.name == (name+", India"):
            return city
    print(f"City with name {name} not found?")
    return None

def readcities(Pnames):
    citylist = [] #co-ordinates of cities
    j = 0 #counter
    geolocator = Nominatim(user_agent="SG_App")

    with open("./india_cities.txt") as file:
        # with open('output.txt','w') as out:
        for line in file:
            city = line.rstrip("\n")
            if(city == ""):
                break
            Pnames.insert(j,city)#insert at jth position
            city += ", India"
            pt = geolocator.geocode(city,timeout=10000)
            #  out.write("City = ",city,pt.latitude,pt.longitude)
            # out.write(f"City = {city} {pt.latitude},{pt.longitude} \n")
            # out.write('/n')
            # citylist.insert(j,[pt.latitude,pt.longitude])
            citylist.append(City(pt.latitude,pt.longitude,city))
            j += 1
    return citylist

pnames = []
cities = readcities(pnames)
print(pnames)
print()

def distance_matrix(citylist,cityNames):
    l = len(citylist)
    nPyDistanceMat = np.zeros((l,l))
    # np.fill_diagonal(nPyDistanceMat,0)
    df = pd.DataFrame(nPyDistanceMat,index=cityNames,columns=cityNames)
    for r in df.index:
        for c in df.columns:
            if (r != c):
                c1 = getCityObj(r,citylist)
                c2 = getCityObj(c,citylist)
                df.at[r,c] = distance(c1,c2)
                df.at[c,r] = df.at[r,c]
    print(df)

distance_matrix(cities,pnames)