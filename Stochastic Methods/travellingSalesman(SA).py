from geopy.geocoders import Nominatim
from numpy import *
from pylab import *
import matplotlib
import matplotlib.pyplot as plt
# matplotlib.use('tkagg')
import math,random

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
                Pnames.insert(j,city)#insert at jth position
                city += ", India"
                pt = geolocator.geocode(city,timeout=10000)
                #  out.write("City = ",city,pt.latitude,pt.longitude)
                out.write(f"City = {city} {pt.latitude},{pt.longitude} \n")
                # out.write('/n')
                p.insert(j,[pt.latitude,pt.longitude])
                j += 1
    return p

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
    Pt = np.array(P)
    #print(Pt[:,0])

    # plt.savefig('img.png')
    plt.title('Total distance='+str(dist))
    plt.plot(Pt[:,0],Pt[:,1],'-o')

    for i in range(len(P)):
        plt.annotate(Pnames[i],(P[i][0],P[i][1]))
    plt.show()

# Plot(s,P,506.75,Pnames)

#'__name__' allows you to write code that runs only when the script is executed directly (not when imported).
if __name__ == '__main__':
    Pnames = []
    P = readcities(Pnames)
    nCity = len(P)
    print(f"Number of cities is {nCity}.")

    maxTsteps = 300 #Temp is lowered maxTsteps times
    fCool = 0.92 #Factor to multiply temp at each cooling step
    maxSwaps = 2000 #Number of swaps at constant temp

    maxAccepted = 10*nCity # Number of accepted configuration changes at constant temperature

    seq = np.arange(0,nCity,1) #start from 0 and go till in increment of 1
    dist = totalDistance(P,seq)
    temp = dist * 10.0 #let us start at a high temp

    #printing the current configuration 
    print("\n\n")
    print(seq)
    print("\n nCity= %3d dist= %f temp= %f \n" % (nCity, dist, temp))

    input("...Press Enter to continue...")

    Plot(seq,P,dist,Pnames)

    prevDist, countC = 0.0, 0

    for t in range(1,maxTsteps+1,1):
        if temp < 1.0e-6: #min temp threshold
            break
        accepted = 0
        iters = 0

        while(iters < maxSwaps):
            N1, N2 = -1, -1
            while(N1 < 0 or N1 >= nCity):
                N1 = (int((random.random()*1000)))%nCity
                print(N1)
            while(N2 < 0 or N1==N2):
                N2 = (int((random.random()*1000)))%nCity
                print(N2)
            
            if (N2 < N1):
                N1, N2 = N2, N1

            rc = random.uniform(0,1)
            #randomly choosing between swap and reverse
            #for swap, adjacent cities are not considered..
            if (rc < 0.5) and (N1+1 != N2) and (N1 != ((N2 + 1)%nCity)):
                #swap the cities
                pass
            else:
                #reverse the cities
                pass
            #check if we accepted the new configuration
            if():#?
                accepted += 1
            iters += 1


