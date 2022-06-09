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
      if adjacencyList.get(target) is None:
        adjacencyList[target] = []

      adjacencyList[source].append(target)
    
    return mapOfEdges, adjacencyList

def initGraph(documentPath):
  with open(documentPath, mode="r", encoding="utf-8") as f:
    data = geojson.load(f)

  graph = Graph(data["nodes"], data["links"])
  return graph

graph = initGraph("data/calles_san_juan_de_lurigancho.json")

with open("adjacency_list.json", mode="w", encoding="utf-8") as f:
  adjacencyList = json.dumps(graph.adjacencyList)
  f.write(adjacencyList)

'''def remap_keys(edges):
  return [{"key": k, "value": v} for k, v in edges.items()]

with open("calles.json", mode="w", encoding="utf-8") as f:
  calles = json.dumps(remap_keys(graph.edges))
  f.write(calles)'''

'''with open("intersecciones.json", mode="w", encoding="utf-8") as f:
  intersecciones = json.dumps(graph.nodes)
  f.write(intersecciones)'''

#print(graph.nodes[181285635])
#print(graph.adjacencyList[5723856941])
#print(graph.nodes[5723856941])
#print(graph.nodes[8231346943])
#print(graph.nodes[1342139130])
#print(graph.edges[(8231346943, 1342139130)])

'''node_ini = 8231346943
print(graph.adjacencyList[node_ini])
for node in graph.adjacencyList[node_ini]:
  print(graph.edges[(node_ini, node)])'''
#print(graph.nodes[5723856944])
#print(graph.edges[(5723856941, 5723856944)])
#print(graph.nodes)