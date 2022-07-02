import json
import copy
import math
import heapq as hq
import sys
import os
sys.path.append(os.path.abspath("../"))
from adjacencyListGenerator import generateAdjacencyListForUI, generateLocationListForUI

def transformGraph():
    adjacencyListPath = "../../data/adjacency_list.json"
    streetsPath = "../../data/calles.json"
    intersectionsPath = "../../data/intersecciones.json"

    G = generateAdjacencyListForUI(adjacencyListPath, streetsPath)
    Loc = generateLocationListForUI(intersectionsPath)

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
