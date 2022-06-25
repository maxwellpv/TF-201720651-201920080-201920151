from datetime import datetime
import json
import sys

#sys.path.insert(1, '../sources')  # path of the folder where the cityGraph is saved
from sources.cityGraph import CityGraph


def generateAdjacencyListForUI(cityGraph: CityGraph):
    curr_time = datetime.now().hour

    def getWeight(city1, city2):
        street = cityGraph.streets[(city1, city2)]
        val = street["val"]
        length = street["length"]
        return cityGraph.calculate_weight(val, length, curr_time)

    new_adjacencyList = {}
    for key, arr in cityGraph.adjacencyList.items():
        key = int(key)
        new_adjacencyList[key] = list(map(lambda x: (x, getWeight(key, x)), arr))

    return new_adjacencyList


def generateLocationListForUI(intersectionsPath):
    with open(intersectionsPath) as file:
        data = json.load(file)

    transform = dict()
    for i in data:
        transform[int(i)] = (data[i]['y'], data[i]['x'])

    return transform


adjacencyListPath = "../data/adjacency_list.json"
streetsPath = "../data/calles.json"
intersectionsPath = "../data/intersecciones.json"

cityGraph = CityGraph(adjacencyListPath=adjacencyListPath, streetsPath=streetsPath, intersectionsPath=intersectionsPath)

new_adjacencyList = generateAdjacencyListForUI(cityGraph)
locationsList = generateLocationListForUI(intersectionsPath)
print(new_adjacencyList)
# print(locationsList)
