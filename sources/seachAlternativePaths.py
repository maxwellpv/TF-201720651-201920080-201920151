import math
from operator import indexOf
from cityGraph import CityGraph
import heapq as hq
from datetime import datetime

def dijkstraAdditionalPaths(graph: CityGraph, node_start, target, time, alternative_paths_count, calculated_paths):
  if (alternative_paths_count <= 0):
    return

  seen = {}
  path = {}
  cost = {}
  
  for k in graph.adjacencyList.keys():
    seen[int(k)] = False
    path[int(k)] = -1
    cost[int(k)] = math.inf

  pqueue = [(0, node_start, -1)]

  while pqueue:
    c, node, parent = hq.heappop(pqueue)
    if not seen[node]:
      seen[node] = True
      for child_node in graph.adjacencyList[str(node)]:
        present = False
        for cpath in calculated_paths:
          if node in cpath:
            index = cpath.index(node)

            if (index + 1 < len(cpath)):
              if cpath[index + 1] == child_node:
                present = True
                break

        if not seen[child_node] and not present:
          street = graph.streets[(node, child_node)]
          val = street["val"]
          length = street["length"]

          new_cost = c + graph.calculate_weight(val, length, time)

          if new_cost < cost[child_node]:
            cost[child_node] = new_cost
            path[child_node] = node
            hq.heappush(pqueue, (new_cost, child_node, node))

  node = target
  p = [node]
  while path[node] != -1:
    p.append(path[node])
    node = path[node]
  p.reverse()
  print("path:", p, "cost:", cost[target])
  calculated_paths.append(p)

  dijkstraAdditionalPaths(graph, node_start, target, time, alternative_paths_count = alternative_paths_count - 1, calculated_paths = calculated_paths)


def dijkstraNoWeight(graph: CityGraph, node_start, target, time):
  seen = {}
  path = {}
  cost = {}

  for k in graph.adjacencyList.keys():
    seen[int(k)] = False
    path[int(k)] = -1
    cost[int(k)] = 0

  pqueue = [(0, node_start)]

  while pqueue:
    c, node = hq.heappop(pqueue)

    for child_node in graph.adjacencyList[str(node)]:
      if not seen[child_node]:
        street = graph.streets[(node, child_node)]
        val = street["val"]
        length = street["length"]

        new_cost = c + graph.calculate_weight(val, length, time)

        if new_cost > cost[node]:
          seen[node] = True
          cost[child_node] = new_cost
          path[child_node] = node
          hq.heappush(pqueue, (new_cost, child_node))

  node = target
  p = [node]
  while path[node] != -1:
    p.append(path[node])
    node = path[node]

  p.reverse()
  print("path:", p, "cost:", cost[target])

def dijkstra(graph: CityGraph, node_start, target, time):
  seen = {}
  path = {}
  cost = {}
  alternativePath = {}

  for k in graph.adjacencyList.keys():
    seen[int(k)] = False
    path[int(k)] = -1
    alternativePath[int(k)] = []
    cost[int(k)] = math.inf

  pqueue = [(0, node_start, -1)]

  while pqueue:
    c, node, parent = hq.heappop(pqueue)

    if not seen[node]:
      seen[node] = True
      for child_node in graph.adjacencyList[str(node)]:
        if not seen[child_node]:
          street = graph.streets[(node, child_node)]
          val = street["val"]
          length = street["length"]

          new_cost = c + graph.calculate_weight(val, length, time)

          if new_cost < cost[child_node]:
            cost[child_node] = new_cost
            path[child_node] = node
            hq.heappush(pqueue, (new_cost, child_node, node))
        else:
          alternativePath[child_node].append(node)
    else:
      alternativePath[node].append(parent)

  def getPathAndCost(start, ext):
    node = start
    p = [node]
    while path[node] != -1:
      p.append(path[node])
      node = path[node]
    p.reverse()

    c = 0
    start_aux = start

    for u in ext:
      try:
        street = graph.streets[(start_aux, u)]
        val = street["val"]
        length = street["length"]
        c += graph.calculate_weight(val, length, time)
      except:
        c += 0
      start_aux = u

    p.extend(ext)

    return (tuple(p), cost[start] + c)

  def getPaths(start):
    path_len = 1
    p = set()
    p.add(getPathAndCost(start, [])) #Se obtiene el camino más corto

    '''
      Se obtienen los caminos más cortos de los caminos alternativos,
      añadiendo el último tramos hasta el target
    '''
    for node in alternativePath[start]: 
      if path_len >= 3:
        break

      p.add(getPathAndCost(node, [target]))
      path_len += 1

    '''
      En caso que no hallan completado los 3 caminos en total,
      se obtienen los caminos más cortos de los caminos alternativos,
      de los caminos alternativos
    '''
    for u in alternativePath[start]:
      for v in alternativePath[u]:
        if path_len >= 3:
          break
        
        new_path = getPathAndCost(v, [u, target])

        if not new_path in p:
          p.add(new_path)
          path_len += 1

    p = list(p)
    p.sort(key=lambda path: path[1])
    return p

  return getPaths(target)

adjacencyListPath = "data/adjacency_list.json"
streetsPath = "data/calles.json"
intersectionsPath = "data/intersecciones.json"

cityGraph = CityGraph(adjacencyListPath=adjacencyListPath, streetsPath=streetsPath, intersectionsPath=intersectionsPath)

curr_time = datetime.now().hour
source = 2922174404
target = 3474378534

paths = dijkstra(cityGraph, source, target, curr_time)

cont = 0
for path, cost in paths: 
  print(f"path #{cont}:", list(path), "cost:", cost)
  cont += 1