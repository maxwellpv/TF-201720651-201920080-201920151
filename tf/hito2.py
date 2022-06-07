from datetime import datetime
import math
import random
import geojson
import json

class Graph:
  def __init__(self, nodes, edges):
    self.nodes = self.processNodes(nodes)
    self.edges, self.adjacencyList = self.processEdges(edges)

  def processNodes(self, nodes):
    mapOfNodes = {}
    for node in nodes:
      mapOfNodes[node["id"]] = node
    return mapOfNodes

  def processEdges(self, egdes):
    mapOfEdges = {}
    adjacencyList = {}

    for edge in egdes:
      source = edge["source"]
      target = edge["target"]

      mapOfEdges[(source, target)] = edge

      if adjacencyList.get(source) is None:
        adjacencyList[source] = []
      adjacencyList[source].append(target)
    
    return mapOfEdges, adjacencyList

  def traffic_factor(self, time):
    factor = round(random.uniform(3, 7)*math.cos(2 * (time / 3) - 1) * math.sin((time / 6) - 2) + 5, 3)
    if factor > 10: return 10
    if factor < 0: return 0
    return factor

def initGraph(documentPath):
  with open(documentPath, mode="r", encoding="utf-8") as f:
    data = geojson.load(f)

  graph = Graph(data["nodes"], data["links"])
  return graph

graph = initGraph("./TF/calles_san_juan_de_lurigancho.json")