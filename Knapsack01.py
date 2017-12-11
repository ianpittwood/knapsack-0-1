from random import *
import copy
import time

class KnapSack:
    #Declare constantas for KnapSacks
    SIZE_OF_PACK = 50

    def __init__(self):
        #Initialize all properties of the sack
        self.remainingRoom = self.SIZE_OF_PACK
        self.totalValue = 0
        self.itemList = []
    def addItem(self, item):
        #Add item to sack, increase value, decrease remaining room
        self.remainingRoom -= item[0]
        self.totalValue += item[1]
        self.itemList.append(item)

    #Getters
    def getRemainingRoom(self):
        return self.remainingRoom
    def getTotalValue(self):
        return self.totalValue
    def getItemList(self):
        return self.itemList

class ItemPool:
    #Declare constants for item pools
    LIST_SIZE = 40
    MIN_WEIGHT = 1
    MAX_WEIGHT = 50
    MIN_VALUE = 1
    MAX_VALUE = 100

    def __init__(self):
        self.items = []
        self.randomizeAvailableObjects()
        #Uncomment below for test set
        #self.items = [[20,40],[30,80],[40,90],[45,90],[50,100]]
    def randomizeAvailableObjects(self):
        for i in range(0,self.LIST_SIZE):
            self.items.append([randint(self.MIN_WEIGHT,self.MAX_WEIGHT), randint(self.MIN_VALUE,self.MAX_VALUE)])

#Pre-condition: input is an empty sack, a pre-generated item pool, and the number of items in the pool
#Post-condition: a sack containing the highest value combination of items will be returned
def dynamicAlgo(sack, xPool, n):
    #INVARIANT: n and sack.getRemainingRoom are valid integers containing the # of items remaining in the queue and the sack's remaining space
    if sack.getRemainingRoom == 0 or n == 0:
        return sack
    if xPool.items[n-1][0] > sack.getRemainingRoom():
        return dynamicAlgo(sack, xPool, n-1)
    else:
        sackCopy = copy.deepcopy(sack)
        sackCopy.addItem(xPool.items[n-1])
        sackCopy = dynamicAlgo(sackCopy, xPool, n-1)
        sack = dynamicAlgo(sack, xPool, n-1)
        if sackCopy.getTotalValue() > sack.getTotalValue():
            return sackCopy
        else:
            return sack
    #INVARIANT: Returns the best possible sack thus far, recursively

#Pre-condition: input is a pre-generated item pool
#Post-condition: highest value to weight ratio items placed into the sack
def greedyAlgo(yPool):
    greedySack = KnapSack()
    xPool = copy.deepcopy(yPool)
    for i in range(0,xPool.LIST_SIZE):
        if i != 0:
            assert(len(xPool.items[i-1]) == 3 and xPool.items[i-1][2] == xPool.items[i-1][1]/xPool.items[i-1][0]) #INVARIANT: i-1 items have value/weight ratio added
        xPool.items[i].append(xPool.items[i][1]/xPool.items[i][0])
        assert(len(xPool.items[i]) == 3 and xPool.items[i][2] == xPool.items[i][1]/xPool.items[i][0]) #INVARIANT: i items have value/weight ratio added
    xPool.items.sort(key=lambda tup: tup[2], reverse=True)
    #INVARIANT: item poool sorted by value/weight ratio in reverse order (largest ratio to smallest)
    for i in range(0,xPool.LIST_SIZE):
        if xPool.items[i][0] <= greedySack.getRemainingRoom():
            greedySack.addItem(xPool.items[i])
    return greedySack

pool = ItemPool()
dynamicSack = KnapSack()
start_time = time.time()
dynamicSack = dynamicAlgo(dynamicSack, pool, len(pool.items))
dynamicTime = time.time() - start_time
start_time = time.time()
greedySack = greedyAlgo(pool)
greedyTime = time.time() - start_time
print("Item Pool: ")
print(pool.items)
print("Value of Dynamic Algorithm Sack: " + str(dynamicSack.getTotalValue()))
print("Dynamic Algorithm Sack Contents (Weight, Value): ")
print(dynamicSack.getItemList())
print("Dynamic Time to Process: " + str(dynamicTime))
print("Value of Greedy Algorithm Sack: " + str(greedySack.getTotalValue()))
print("Greedy Algorithm Sack Contents (Weight, Value, Value/Weight): ")
print(greedySack.getItemList())
print("Greedy Time to Process: " + str(greedyTime))
