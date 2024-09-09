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
    Pt = np.array(Pt)
    #print(Pt[:,0])

    # plt.savefig('img.png')
    plt.title('(SA)Total distance='+str(dist))
    plt.plot(Pt[:,0],Pt[:,1],'-o')

    for i in range(len(P)):
        plt.annotate(Pnames[i],(P[i][0],P[i][1]))
    plt.show(block=False)
    plt.pause(0.01)  # Wait for 3 seconds
    plt.cla()

# Plot(s,P,506.75,Pnames)

def swap(P,seq,dist,N1,N2,temp,nCity):
    L1,R1 = N1 - 1,N1 + 1
    if(L1 < 0):#L1 must be the last node then as the path is closed
        L1 += nCity
    if(R1 >= nCity): R1 = 0 

    L2,R2 = N2 - 1,N2 + 1
    if (L2 < 0): L2 += nCity
    if (R2 >= nCity): R2 = 0

    #we need to calculate delta E i.e. change in config between old and new states 
    delta = 0.0
    delta += distance(P[seq[L1]],P[seq[N2]])
    delta += distance(P[seq[N1]],P[seq[R2]])
    delta -= distance(P[seq[L1]],P[seq[N1]])
    delta -= distance(P[seq[N2]],P[seq[R2]])

    #other four operations are not always needed
    # if(N1 != L2 and R1 != N2 and R1 != L2 and N2 != L1 and R2 != L1):
    if R1 != L2 or R2 != L1: # 'If' N1 and N2 don't have a common neighbour
        # print("\n\nIn SWAP Special Case")
        # print( "N1=%3d N2=%3d N1L=%3d N1R=%3d N2L=%3d N2R=%3d \n" % (N1,N2, L1, R1, L2, R2))
        # print(seq)
        # print("\n nCity= %3d dist= %f temp= %f \n" % (nCity, dist, temp))

        delta += distance(P[seq[N2]], P[seq[R1]])
        delta += distance(P[seq[L2]], P[seq[N1]])
        delta -= distance(P[seq[N1]], P[seq[R1]])
        delta -= distance(P[seq[L2]], P[seq[N2]])
    
    prob = 1.0
    if (delta > 0.0):
        prob = exp(-delta/temp)

    rand = random.random()
    if(rand < prob): #accept the change
        dist += delta
        # print("New Dist is:",dist)
        seq[N1],seq[N2] = seq[N2],seq[N1]
        diff = abs(dist - totalDistance(P,seq)) #abs(delta)?
        if(diff*dist > 0.01):
            pass
            # input("...Press Enter to continue...")
        return dist,True
    else: #reject
        return dist,False

def reverse(P,seq,dist,N1,N2,temp,nCity):
    L1,R2 = N1 - 1,N2 + 1
    if L1 < 0: L1 += nCity
    if (R2 >= nCity): R2 = 0

    delta = 0.0
    if (N1 != R2) and (N2 != L1): 
        delta = distance(P[seq[N1]],P[seq[R2]])+distance(P[seq[N2]],P[seq[L1]]) \
                -distance(P[seq[N1]],P[seq[L1]])-distance(P[seq[N2]],P[seq[R2]])
    else: #N1 > N2?
        return dist,False
    
    prob = 1.0
    if(delta > 0.0):
        prob = exp(-delta/temp)

    rndm = random.random()
    if (rndm < prob):
        dist += delta
        # print("New Dist is:",dist)
        i, j = N1,N2
        while(i < j):
            seq[i], seq[j] = seq[j], seq[i]
            i+=1;j-=1

        diff = abs(dist-totalDistance(P,seq))
        if(diff*dist > 0.01):
            pass
            # print(seq)
            # print("IN Reverse\n")
            # print( "N1=%3d N2=%3d N1L=%3d N2R=%3d \n" % (N1,N2, L1, R2))
            # print("\n nCity= %3d dist= %f temp= %f \n" % (nCity, dist, temp))
            # input("...Press Enter to continue...")
        return dist,True
    else: #reject
        return dist,False


#'__name__' allows you to write code that runs only when the script is executed directly (not when imported).
if __name__ == '__main__':
    Pnames = []
    P = readcities(Pnames)
    nCity = len(P)
    print(f"Number of cities is {nCity}.")

    maxTsteps = 300 #Temp is lowered maxTsteps times
    fCool = 0.97 #Factor to multiply temp at each cooling step
    maxSwaps = 2000 #Number of swaps at constant temp

    maxAccepted = 10*nCity # Number of accepted configuration changes at constant temperature

    seq = np.arange(0,nCity,1) #start from 0 and go in increments of 1
    dist = totalDistance(P,seq)
    temp = dist * 10.0 #let us start at a high temp

    #printing the current configuration 
    print("\n\n")
    print(seq)
    print("\n nCity= %3d dist= %f temp= %f \n" % (nCity, dist, temp))
    input("...Press Enter to continue...")

    Plot(seq,P,dist,Pnames)

    prevDist, constConv = 0.0, 0

    for t in range(1,maxTsteps+1,1):
        if temp < 1.0e-6: #min temp threshold
            break
        accepted = 0
        iters = 0

        while(iters < maxSwaps):
            N1, N2 = -1, -1
            while(N1 < 0 or N1 >= nCity):
                N1 = (int((random.random()*1000)))%nCity
                # print(N1)
            while(N2 < 0 or N1==N2 or N2 >= nCity):
                N2 = (int((random.random()*1000)))%nCity
            
            if (N2 < N1):
                N1, N2 = N2, N1

            rc = random.uniform(0,1)
            #randomly choosing between swap and reverse
            #for swap, adjacent cities are not considered..
            if (rc < 0.5) and (N1+1 != N2) and (N1 != ((N2 + 1)%nCity)):
                #swap the cities
                dist, flag = swap(P, seq, dist, N1, N2, temp, nCity)
            else:
                #reverse the cities
                dist, flag = reverse(P, seq, dist, N1, N2, temp, nCity)
            #check if we accepted the new configuration
            if(flag):#?
                accepted += 1
            iters += 1

        # print("Iteration: %d temp=%f dist=%f" %(t, temp, dist))
        # print("seq = ")
        # set_printoptions(precision=3)
        # print(seq)
        # if (t%25==0): input("...Press Enter to continue...")
        # print("%c%c" % ('\n', '\n'))

        #check if we have approached the optimal solution
        if(abs(dist-prevDist) < 1.0e-4):
            constConv += 1
        else:
            constConv = 0
        
        if(constConv >= 4):
            break

        # if((t%5) == 0):
        Plot(seq,P,dist,Pnames)


        #reduce temperature...to go towards hill climbing
        temp *= fCool
        prevDist = dist

    Plot(seq,P,dist,Pnames)
        

