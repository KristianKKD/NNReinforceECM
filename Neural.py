import numpy

def Rand(start=-1, end=1):
    return numpy.random.uniform(start, end)

def RandInt(start=-1, end=1):
    return numpy.random.randint(start, end)

def ActivationFunction(input):
    return (1 / (1 + numpy.exp(-input))) * 0.1

def Clamp(input, min = -1, max = 1):
    if input > max:
        input = max
    elif input < min:
        input = min
    return input

class Edge:
    weight = 0
    nextNodeID = 0

    def __init__(self, nextID):
        self.nextNodeID = nextID
        self.weight = Rand() * 0.1 #initialize very small

class Node:
    id = 0
    heldValue = 0
    bias = 0
    edges = []
    lastNodes = []

    def __init__(self, myID, lastLayer, disableBias):
        self.id = myID
        self.heldValue = 0
        self.bias = 0
        self.edges = []
        self.lastNodes = []

        if not disableBias:
            self.lastNodes = lastLayer.nodes

            for node in self.lastNodes:
                node.AddEdge(myID)
                
            self.bias = Rand()

    def Output(self):
        self.heldValue = self.bias
        for node in self.lastNodes:
            self.heldValue += node.EdgeValue(self.id)
        self.heldValue = Clamp(self.heldValue)

    def EdgeValue(self, targetID):
        return ActivationFunction(self.heldValue * self.edges[targetID].weight)
    
    def AddEdge(self, newNodeID):
        self.edges.append(Edge(newNodeID))

class Layer:
    nodes = []
    isInput = False

    def __init__(self, nodeCount, previousLayer, disableBias):
        self.nodes = []
        self.isInput = not disableBias and (len(previousLayer.nodes) == 0 and disableBias)
        for i in range(nodeCount):
            self.nodes.append(Node(i, previousLayer, disableBias))

class NeuralNet:
    layers = []

    def __init__(self, inputCount, hiddenLayers, hiddenCount, outputCount):
        self.layers = []

        self.layers.append(Layer(inputCount, None, True))
        for i in range(hiddenLayers):
            self.layers.append(Layer(hiddenCount, self.layers[i], False))
        self.layers.append(Layer(outputCount, self.layers[len(self.layers)- 1], False))

    def Mutate(self, mutationCount):
        #mutate random edge n times
        for i in range(mutationCount):
            #get random layer
            lCount = len(self.layers)
            lRand = RandInt(1, lCount - 2) #first hidden layer to last hidden layer
            l = self.layers[lRand]

            #get random node within layer
            nCount = len(l.nodes)
            nRand = RandInt(0, nCount - 1)
            n = l.nodes[nRand]

            #get random edge outgoing from node
            eCount = len(n.edges)
            eRand = RandInt(0, eCount - 1)
            e = n.edges[eRand]

            #random modification to edge
            e.weight = Clamp(e.weight + Rand(-1, 1))

        return self
    
    def Input(self, inputs):
        for inp in inputs:
            self.layers[0].heldValue = Clamp(inp, -1, 1) #just in case, clamp the value
        
        for l in self.layers:
            if not l.isInput:
                for n in l.nodes:
                    n.Output()
        
        outputs = []
        for n in self.layers[len(self.layers) - 1].nodes:
            outputs.append(Clamp(n.heldValue))

        return outputs