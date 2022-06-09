import json
import math
from cityGraph import CityGraph
from perlin_noise import PerlinNoise

def generatePerlinNoise(n):
  noise = PerlinNoise(octaves = 8, seed = 1234)
  xd, yd = n * 5, 1
  pnoise = [[noise([i/xd, j/yd]) for i in range(xd)] for j in range(yd)]
  
  values = []
  mini = math.inf
  maxi = -math.inf

  for v in pnoise:
    for e in v:
      e = int(e * 100)
      mini = min(mini, e)
      maxi = max(maxi, e)
      values.append(e)

  if mini < 0:
    values = list(map(lambda x: x + abs(mini), values))

  diff = maxi - mini
  convertor = diff / 50

  values = list(map(lambda x: int(x / convertor), values))
  return values

def bfs(graph: CityGraph, perNoise):
  seen = {}
  for k, v in graph.adjacencyList.items():
    for e in v:
      seen[(k, e)] = False

  indexPer = 0

  def bfsUtil(node):
    nonlocal indexPer

    queue = []

    queue.append(node)
    seen[node] = True

    while queue:
      curr_node = queue.pop(0)
      for child_node in graph.adjacencyList[str(curr_node)]:
        if not seen[(str(curr_node), child_node)]:
          seen[(str(curr_node), child_node)] = True
          queue.append(child_node)

          graph.streets[(int(curr_node), int(child_node))].update({"val": perNoise[indexPer]})

          indexPer += 1

  for k, v in graph.adjacencyList.items():
    for e in v:
      if not seen[(k, e)]:
        bfsUtil(k)

adjacencyListPath = "data/adjacency_list.json"
streetsPath = "data/calles.json"
intersectionsPath = "data/intersecciones.json"

cityGraph = CityGraph(adjacencyListPath=adjacencyListPath, streetsPath=streetsPath, intersectionsPath=intersectionsPath)
perNoise = generatePerlinNoise(len(cityGraph.streets))

bfs(cityGraph, perNoise)

isSucces = True
for v in cityGraph.streets.values():
  try:
    if v["val"] is not None:
      break
  except:
    isSucces = False
    continue

def remap_keys(edges):
    return [{"key": k, "value": v} for k, v in edges.items()]

if isSucces:
  print("exito :)")
  
  with open("calles.json", mode="w", encoding="utf-8") as f:
    streets = json.dumps(remap_keys(cityGraph.streets))
    f.write(streets)
else:
  print("F")