from datetime import datetime
import json
import math

def generateAdjacencyListForUI(adjacencyListPath, streetsPath):
    adjacencyList = {}
    streets = {}
    curr_time = datetime.now().hour
    keyValues = {}

    def initData():
        with open(adjacencyListPath, mode="r", encoding="utf-8") as f:
            nonlocal adjacencyList
            adjacencyList = json.load(f)
            adjacencyList = [(int(key), value) for key, value in adjacencyList.items()]
            adjacencyList = sorted(adjacencyList, key=lambda x: x[0])

            i = 0
            for key, val in adjacencyList:
                keyValues[key] = i
                i += 1

        with open(streetsPath, mode="r", encoding="utf-8") as f:
            nonlocal streets
            streetsList = json.load(f)

            for element in streetsList:
                k, v = element

                key = tuple(element[k])
                value = element[v]

                streets[key] = value

    def traffic_by_hour(time):
        factor = round(5 * math.cos(2 * (time / 3) - 1) * math.sin((time / 6) - 2) + 5, 3)
        if factor > 10: return 10
        if factor < 0: return 0
        return factor

    def calculate_traffic_factor(val, time):
        value = val * traffic_by_hour(time)
        return value / 10

    def calculate_weight(val, length, time):
        return length * calculate_traffic_factor(val, time)

    def getWeight(city1, city2):
        street = streets[(city1, city2)]
        val = street["val"]
        length = street["length"]
        return calculate_weight(val, length, curr_time)

    def getNewAdjacencyList():
        nonlocal adjacencyList
        nonlocal keyValues
        newAdjacencyList = []
        for key, arr in adjacencyList:
            newAdjacencyList.append(list(map(lambda x: (keyValues[x], getWeight(key, x)), arr)))
        return newAdjacencyList

    initData()
    return getNewAdjacencyList()

def generateLocationListForUI(intersectionsPath):
    with open(intersectionsPath) as file:
        data = json.load(file)
        data = [(int(key), (value['x'], value['y'])) for key, value in data.items()]
        data = sorted(data, key=lambda x: x[0])

    locations = []
    for k, v in data:
        locations.append(v)
    
    return locations


adjacencyListPath = "data/adjacency_list.json"
streetsPath = "data/calles.json"
intersectionsPath = "data/intersecciones.json"

print(generateAdjacencyListForUI(adjacencyListPath, streetsPath)[:10])
print(generateLocationListForUI(intersectionsPath)[:10])
