import numpy as np

multiplier = 2
sigma = 200*multiplier
mu = 1024*2*multiplier
sMax = 2047*2*multiplier
size = 2048*2*multiplier
s = np.abs((np.random.normal(loc=mu, scale=sigma, size=size)).astype(int))
for i,item in enumerate(s):
    if item > sMax:
        s[i] = sMax

import matplotlib.pyplot as plt
count, bins, ignored = plt.hist(s, 2048, density=True)
plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) *np.exp( - (bins - mu)**2 / (2 * sigma**2) ),linewidth=2, color='r')
plt.ion()
plt.show()


a = s.tolist()
# a = [1,2,3,4,1,2,5,1,2,3,4,5]


n = len(a)
m = 2

#Function to accept reference string and frame size.
def accept():
    global a,n,m
    a = []
    n = eval(input("\n Enter the size of reference string : "))
    for i in range(n):
        a.append(eval(input(" Enter [%2d] : " % (i+1))))
    m = eval(input("\n Enter page frame size : "))

#First In First Out Page Replacement Algorithm
def __fifo():
    global a,n,m,printBool
    f = -1
    page_faults = 0
    page = []
    for i in range(m):
        page.append(-1)

    for i in range(n):
        flag = 0
        for j in range(m):
            if(page[j] == a[i]):
                flag = 1
                break
        if printBool: print("\n"+str(i) + "/"+str(n-1)+" ")
        if flag == 0:
            f=(f+1)%m
            page[f] = a[i]
            page_faults+=1
            if printBool: print("\n%d ->" % (a[i]), end=' ')
            for j in range(m):
                if page[j] != -1:
                    if printBool: print(page[j], end=' ')
                else:
                    if printBool: print("-", end=' ')
        else:
            if printBool: print("\n%d -> No Page Fault" % (a[i]), end=' ')
            
    print("\n Total page faults : %d." % (page_faults))



#Least Recently Used Page Replacement Algorithm
def __lru():
    global a,n,m,printBool
    x = 0
    page_faults = 0
    page = []
    for i in range(m):
        page.append(-1)

    for i in range(n):
        flag = 0
        for j in range(m):
            if(page[j] == a[i]):
                flag = 1
                break
        if printBool: print("\n"+str(i) + "/"+str(n-1)+" ")
        if flag == 0:
            if page[x] != -1:
                min = 99999
                for k in range(m):
                    flag = 0
                    j =  i
                    while j>=0:
                        j-=1
                        if(page[k] == a[j]):
                            flag = 1
                            break
                    if (flag == 1 and min > j):
                        min = j
                        x = k

            page[x] = a[i]
            x=(x+1)%m
            page_faults+=1
            if printBool: print("\n%d ->" % (a[i]), end=' ')
            for j in range(m):
                if page[j] != -1:
                    if printBool: print(page[j], end=' ')
                else:
                    if printBool: print("-", end=' ')
        else:
            if printBool: print("\n%d -> No Page Fault" % (a[i]), end=' ')
            
    print("\n Total page faults : %d." % (page_faults))

#Optimal Page Replacement Algorithm
def __optimal():
    global a,n,m,printBool
    x = 0
    page_faults = 0
    page = []
    FREE = -1
    for i in range(m):
        page.append(FREE)

    for i in range(n):
        flag = 0
        for j in range(m):
            if(page[j] == a[i]):
                flag = 1
                break
        if printBool: print("\n"+str(i) + "/"+str(n-1)+" ")
        if flag == 0:
            # look for an empty one
            faulted = False
            new_slot = FREE
            for q in range(m):
                if page[q] == FREE:
                    faulted = True
                    new_slot = q
            
            if not faulted:
                # find next use farthest in future
                max_future = 0
                max_future_q = FREE
                for q in range(m):
                    if page[q] != FREE:
                        found = False
                        for ii in range(i, n):
                            if a[ii] == page[q]:
                                found = True
                                if ii > max_future:
                                    # print "\n\tFound what will be used last: a[%d] = %d" % (ii, a[ii]),
                                    max_future = ii
                                    max_future_q = q

                                break
                        
                        if not found:
                            # print "\n\t%d isn't used again." % (page[q]),
                            max_future_q = q
                            break

                faulted = True
                new_slot = max_future_q
            
            page_faults += 1
            page[new_slot] = a[i]
            if printBool: print("\n%d ->" % (a[i]), end=' ')
            for j in range(m):
                if page[j] != FREE:
                    if printBool: print(page[j], end=' ')
                else:
                    if printBool: print("-", end=' ')
        else:
            if printBool: print("\n%d -> No Page Fault" % (a[i]), end=' ')
            
    print("\n Total page faults : %d." % (page_faults))

    


#JYGY Replacement Algorithm
class Page:
    inputCount = 0
    inputBias = 0
    frequency = 1
    timeStamp = 0
    number = 0
    base_A = 1
    base_B = 1
    A = 1
    B = 1
    def __init__( self, number, timeStamp):
        self.number = number
        self.timeStamp = timeStamp
    def incrementFrequency(self):
        self.frequency += 1
    def updateTimeStamp(self, timeStamp):
        self.timeStamp = timeStamp
    def getScore(self):
        return self.A * self.frequency + self.B * self.timeStamp


def __jygy():
    global a,n,m,printBool
    myDict = {}
    x = 0
    page_faults = 0
    page = []
    for i in range(m):
        page.append(-1)

    for i in range(n):
        flag = 0
        for j in range(m):
            if(page[j] == a[i]):
                flag = 1
                break
        if printBool: print("\n"+str(i) + "/"+str(n-1)+" ")
        if flag == 0:
            if page[x] != -1:
                min = 999999999999999
                for k in range(m):
                    if(myDict[page[k]].getScore() < min):
                        min = myDict[page[k]].getScore()
                        x = k
                # min = 999
                # for k in range(m):
                #     flag = 0
                #     j =  i
                #     while j>=0:
                #         j-=1
                #         if(page[k] == a[j]):
                #             flag = 1
                #             break
                #     if (flag == 1 and min > j):
                #         min = j

                #         x = k

            if(page[x]!= -1):
                myDict.pop(page[x])
            page[x] = a[i]
            if a[i] in myDict.keys():
                myDict[a[i]].incrementFrequency()
                myDict[a[i]].updateTimeStamp(i)
            else:
                myDict[a[i]] = Page(a[i],i)

            x=(x+1)%m
            page_faults+=1
            if printBool: print("\n%d ->" % (a[i]), end=' ')
            for j in range(m):
                if page[j] != -1:
                    if printBool: print(page[j], end=' ')
                else:
                    if printBool: print("-", end=' ')
        else:
            if a[i] in myDict.keys():
                myDict[a[i]].incrementFrequency()
                myDict[a[i]].updateTimeStamp(i)
            if printBool: print("\n%d -> No Page Fault" % (a[i]), end=' ')
            
    print("\n Total page faults : %d." % (page_faults))


#Displaying the menu and calling the functions.    
while True:
    m = eval(input("m: "))
    printBool = input("Do you want to print? Y/N: ")
    if(printBool == "Y" or printBool == "y"):
        printBool = True
    else:
        printBool = False
    print("\n SIMULATION OF PAGE REPLACEMENT ALGORITHM")
    print(" Menu:")
    print(" 0. Accept.")
    print(" 1. FIFO.")
    print(" 2. LRU.")
    print(" 3. Optimal.")
    print(" 4. JIGY.")
    print(" 5. Exit.")
    ch = eval(input(" Select : "))

    if ch == 0:
        accept()
    if ch == 1:
        __fifo()
    if ch == 2:
        __lru()
    if ch == 3:
        __optimal()
    if ch == 4:
        __jygy()
    if ch == 5:
        break

