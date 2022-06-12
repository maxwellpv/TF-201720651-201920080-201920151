import math
from cityGraph import CityGraph
import heapq as hq
from datetime import datetime

def dijkstraMin(graph: CityGraph, node_start, target, time):
  seen = {}
  path = {}
  cost = {}

  for k in graph.adjacencyList.keys():
    seen[int(k)] = False
    path[int(k)] = -1
    cost[int(k)] = math.inf

  pqueue = [(0, node_start)]

  while pqueue:
    c, node = hq.heappop(pqueue)

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
            hq.heappush(pqueue, (new_cost, child_node))

  node = target
  p = [node]
  while path[node] != -1:
    p.append(path[node])
    node = path[node]

  p.reverse()
  print("path:", p, "cost:", cost[target])

adjacencyListPath = "data/adjacency_list.json"
streetsPath = "data/calles.json"
intersectionsPath = "data/intersecciones.json"

cityGraph = CityGraph(adjacencyListPath=adjacencyListPath, streetsPath=streetsPath, intersectionsPath=intersectionsPath)

curr_time = datetime.now().hour
source = 181285629
target = 2922174405

dijkstraMin(cityGraph, source, target, curr_time)