import json
import copy
import random as r
from datetime import datetime
import math
import heapq as hq


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
        return calculate_traffic_factor(val, time) * math.log10(length)

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


def transformGraph():
    # n, m = 50, 50
    # Loc = [(i * 100 - r.randint(145, 155), j * 100 - r.randint(145, 155)) for i in range(1, n + 1) for j in range(1, m + 1)]
    # G = [[] for _ in range(n * m)]

    adjacencyListPath = "data/adjacency_list.json"
    streetsPath = "data/calles.json"
    intersectionsPath = "data/intersecciones.json"

    G = generateAdjacencyListForUI(adjacencyListPath, streetsPath)
    Loc = generateLocationListForUI(intersectionsPath)

    # for i in range(n):
    #     for j in range(m):
    #         adjs = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
    #         for u, v in adjs:
    #             if u >= 0 and u < n and v >= 0 and v < m:
    #                 G[i * m + j].append((u * m + v, 0))

    response = {"loc": Loc, "g": G}

    return G, Loc


def dijkstra(G, s, t):
    n = len(G)
    visited = [False] * n
    path = [-1] * n
    cost = [math.inf] * n

    cost[s] = 0
    pqueue = [(0, s)]

    higher = 0
    posh = [0, 0]

    while pqueue:
        g, u = hq.heappop(pqueue)
        if not visited[u]:
            visited[u] = True
            for v, w in G[u]:
                if not visited[v]:
                    f = g + w
                    if f < cost[v]:
                        cost[v] = f
                        path[v] = u
                        hq.heappush(pqueue, (f, v))

    head = t
    while path[head] != -1:
        for v, w in G[head]:
            if w > higher:
                higher = w
                posh = [v, head]
        head = path[head]

    return path, cost, posh


def dijkstraPaths(G1, s, t, higher):
    G2 = copy.deepcopy(G1)

    for h in higher:
        G2[h] = []
        g = False
        i = 0
        while not g:
            i += 1
            g = True
            for j in G2[i]:
                if h in j:
                    i = 0
                    g = False
                    G2[i].remove(j)

    path, cost, posh = dijkstra(G2, s, t)

    return path, cost, posh


G, Loc = transformGraph()


def graph():
    response = {"loc": Loc, "g": G}

    return json.dumps(response)


def paths(s, t):
    bestpath, _, h = dijkstra(G, s, t)
    path1, _, i = dijkstraPaths(G, s, t, h)
    i = i + h
    path2, _, j = dijkstraPaths(G, s, t, i)

    response = {"bestpath": bestpath, "path1": path1, "path2": path2}

    return json.dumps(response)
