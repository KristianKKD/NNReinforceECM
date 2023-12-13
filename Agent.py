import Neural
import math
import numpy

def CalculateDistance(x2, x1, y2, y1):
    xTerm = (int(x2) - int(x1))
    yTerm = int(y2) - int(y1)
    return math.sqrt(abs(xTerm + yTerm))

class Agent:
    #neural stats
    net = None #neural net, assigned in __init__
    score = 0

    #agent stats
    timeTravelled = 0
    currentWeight = 0
    currentProfit = 0

    #calculation stats
    minVelocity = 0
    maxVelocity = 0
    maxWeight = 0

    #city related stats
    currentDestination = None
    destinations = []
    visited = []
    itemsCollected = []

    #calculate the highest vals and the max vals so we can scale them from -1 to 1 for the net
    highestDistance = 1
    highestProfit = 1
    highestWeight = 1
    #^^
    totalDistance = 1
    totalProfit = 1
    totalWeight = 1

    def __init__(self, inputNodes, hiddenLayers, hiddenNodes, outputNodes, targetDestinations, minVelocity, maxVelocity, maxWeight, highestDistance, highestProfit, highestWeight, totalDistance, totalProfit, totalWeight):
        #we reset a lot of the stats in Travel

        #net
        self.net = Neural.NeuralNet(inputNodes, hiddenLayers, hiddenNodes, outputNodes)

        #collect data
        self.destinations = targetDestinations

        #velocities
        self.minVelocity = minVelocity
        self.maxVelocity = maxVelocity

        #weights
        self.maxWeight = maxWeight

        #scaling vars
        self.highestDistance = highestDistance
        self.highestProfit = highestProfit
        self.highestWeight = highestWeight

        #scaling vars 2
        self.totalDistance = totalDistance
        self.totalProfit = totalProfit
        self.totalWeight = totalWeight

    def MutateNet(self, mutations):
        return self.net.Mutate(mutations)
    
    def ScoreSelf(self):
        offset = 0
        if self.visited != self.destinations: #if we didn't visit every city
            offset = -0.5
        if self.timeTravelled == 0 or self.currentProfit == 0:
            return -1

        return (1 / self.timeTravelled) * (self.currentProfit / self.totalProfit) + offset
    
    def GetTimeTravelled(self, targetCity):
        if self.currentDestination == None:
            return 0
        velocity = self.maxVelocity - (self.currentWeight/self.maxWeight)
        distance = CalculateDistance(targetCity.x, self.currentDestination.x, targetCity.y, self.currentDestination.y)
        return distance/velocity
    
    def Travel(self):
        self.score = 0
        self.timeTravelled = 0
        self.currentWeight = 0
        self.currentProfit
        self.currentDestination = None
        self.visited = []
        self.itemsCollected = []

        for moveID in range(len(self.destinations)):
            inputs = [self.currentWeight / self.totalWeight, self.timeTravelled / self.totalDistance, self.currentProfit / self.totalProfit, self.maxWeight / self.totalWeight] #array we send to the net
            indexes = []
            distances = []
            profits = []
            weights = []
            
            for d in self.destinations:
                if d in self.visited: #we have been here before
                    distances.append(0)
                    profits.append(0)
                    weights.append(0)
                    indexes.append(-1)
                else: #we have not been here before
                    indexes.append(1)
                    
                    if len(self.visited) == 0: #if we haven't gone anywhere yet
                        distances.append(1 / self.highestDistance) #all distances are same cost when we can start on all
                    else: #we are somewhere
                        #get the distance to everywhere else
                        if d == self.currentDestination:
                            distances.append(0)
                        else:
                            distances.append(CalculateDistance(d.x, self.currentDestination.x, d.y, self.currentDestination.y) / self.highestDistance) #calculate distance
                    
                    #get the potential profits and add to list, also add weight (avoid divide by zero)
                    for i in d.items:
                        if i.profit > 0:
                            profits.append(i.profit / self.highestProfit)
                            self.itemsCollected.append(i)
                            
                            if (i.weight != 0):
                                weights.append(i.weight / self.highestWeight)
                            else:
                                weights.append(i.weight)


            inputs.extend(indexes)
            inputs.extend(distances)
            inputs.extend(profits)
            inputs.extend(weights)

            #get output after using the input
            outputs = self.net.Input(inputs)
            highestIndex = 0
            for index, val in enumerate(outputs):
                if val > highestIndex:
                    highestIndex = index
                    if val >= 1:
                        break

            city = self.destinations[highestIndex]

            #visit target location
            self.timeTravelled += self.GetTimeTravelled(city)
            self.currentDestination = city
            self.visited.append(city)

            printString = ""
            for i in self.visited:
                printString += str(i.index) + ", "

            print(printString)
            #gather items
            for i in self.currentDestination.items: #we currently take ALL ITEMS no matter what, maybe we can also decide to in the future miss some
                if self.currentWeight + i.weight <= self.maxWeight and i.profit > 0:
                    self.currentProfit += i.profit
                    self.currentWeight += i.weight
        
        #once we are finished with our journey, score ourselves
        self.score = self.ScoreSelf()
        return self.score