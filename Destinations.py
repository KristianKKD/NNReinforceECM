
import xml.etree.ElementTree as ET #for reading the XML file

#Data
class Item:
    index = 0
    weight = 0
    profit = 0

    def __init__(self, index, profit, weight):
        self.index = int(index)
        self.profit = int(profit)
        self.weight = int(weight)

class Vertex: #city
    index = 0
    x = 0
    y = 0
    items = []

    def __init__(self, myIndex, xCoord, yCoord):
        self.index = int(myIndex)
        self.x = int(xCoord)
        self.y = int(yCoord)
        self.items = []
#

def GetNextTab(input, startPos):
    for i in range(startPos, len(input)):
        c = input[i]
        if c == '\t':
            return i
    return len(input)

#data collection
def CollectData(src):
    print("Loading data from:", src)

    verts = []
    totalItems = 0
    with open(src, 'r') as f:
        status = 0

        for line in f:
            if "NODE_COORD_SECTION" in line:
                status = 1
                continue
            elif "ITEMS SECTION" in line:
                status = 2
                continue
            
            line = line.strip()
            if status == 1:
                #get info
                index = line[0:GetNextTab(line, 0)]
                xCoord = line[len(index) + 1:GetNextTab(line, len(index) + 1)]
                yCoord = line[len(index) + len(xCoord) + 2:GetNextTab(line, len(index) + len(xCoord) + 2)]
                #append to verts list
                verts.append(Vertex(index, xCoord, yCoord))
            elif status == 2:
                #get info
                index = line[0:GetNextTab(line, 0)]
                profit = line[len(index) + 1:GetNextTab(line, len(index) + 1)]
                weight = line[len(index) + len(profit) + 2:GetNextTab(line, len(index) + len(profit) + 2)]
                cityID = line[len(index) + len(profit) + len(weight) + 3:GetNextTab(line, len(index) + len(profit) + len(weight) + 3)]
                #create item and append
                newItem = Item(index, profit, weight)
                totalItems += 1
                #give relevant item to city
                verts[int(cityID) - 1].items.append(newItem)

    return (verts, totalItems)

import numpy

def find_nearest_index(lst, target):
    return min(range(len(lst)), key=lambda i: abs(lst[i] - target))

# Example list of float values between -1 and 1
values = numpy.linspace(0, 1, 58)

# Given target value
target_value = 0.6

# Find the index of the nearest value
nearest_index = find_nearest_index(values, target_value)

print(f"The nearest value to {target_value} is at index {nearest_index}: {values[nearest_index]}")