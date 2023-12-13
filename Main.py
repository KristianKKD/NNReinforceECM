import Agent
import Destinations
import numpy

#collect data to use in model
targetDestinations, totalItems = Destinations.CollectData('resources/a280-n279.txt')

#params
numpy.random.seed(1) #maintain reproducability
agentCount = 10
elites = 3
mutationCount = 5

inputNodeCount = (len(targetDestinations) * 3) + totalItems + 3 + 1 #all data in cities (- items) + all items + weight,profit,timeTravelled + maxWeight
hiddenLayers = 5
hiddenNodesInLayers = 10
outputNodeCount = len(targetDestinations) #next city to go to is the highest value

maxIterations = 10

#agent stats
minVelocity = 0.1
maxVelocity = 10
maxWeight = 99999

#calculate the highest vals and the total vals so we can scale them from -1 to 1
#total represents the cumulative total we can achieve
totalDistance = 9999999 #as each city may have different times to get to each, ignored chance we can't go from a->b, we just assume a huge number
totalProfit = 0
totalWeight = 0 

#highest represents the largest single value
highestDistance = 1
highestProfit = 1
highestWeight = 1
for d in targetDestinations:
    #get highest distance between two cities
    for dOther in targetDestinations:
        if(d == dOther):
            continue
        distance = Agent.CalculateDistance(dOther.x, d.x, dOther.y, d.y)
        highestDistance = distance if distance > highestDistance else highestDistance

    for i in d.items:
        highestProfit = i.profit if i.profit > highestProfit else highestProfit
        highestWeight = i.weight if i.weight > highestWeight else highestWeight

        totalProfit += i.profit
        totalWeight += i.weight

#setup
agents = []
for i in range(agentCount):
    a = Agent.Agent(inputNodeCount, hiddenLayers, hiddenNodesInLayers, outputNodeCount, targetDestinations, minVelocity, maxVelocity, maxWeight, highestDistance, highestProfit, highestWeight, totalDistance, totalProfit, totalWeight)
    agents.append(a)

#main loop
for i in range(maxIterations):
    #have all agents do their journey
    for a in agents:
        a.Travel() #they score themselves after travelling

    if len(agents) > 1:
        #sort the agents in ascending order based on score
        agents = sorted(agents, key=lambda agent: agent.score)

        #mutate all but the top 3
        for i in range(len(agents) - elites):
            agents[i].net.Mutate(mutationCount)

    bestAgent = agents[len(agents) - 1]
    print("Best agent's score: ", bestAgent.score)
    print("Best agent's destinations: ", bestAgent.visited)
    print("Best agent's item profit: ", bestAgent.score)

agents = sorted(agents, key=lambda agent: agent.score)
bestAgent = agents[len(agents) - 1]
print("Best agent's score: ", bestAgent.score)
print("Best agent's destinations: ", bestAgent.visited)
print("Best agent's item profit: ", bestAgent.score)





    

    

