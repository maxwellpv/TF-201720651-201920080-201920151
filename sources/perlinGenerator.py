import cityGraph as gp

def bfs(graph: gp.CityGraph):
  seen = { k: False for k, v in graph.adjacencyList.items() }

  finish = False
  cont = 0

  def bfsUtil(node):
    nonlocal cont

    queue = []

    queue.append(node)
    seen[node] = True

    while queue:
      if cont > 50:
        break
      curr_node = queue.pop(0)
      for child_node in graph.adjacencyList[curr_node]:
        child_node = str(child_node)
        if not seen[child_node]:
          seen[child_node] = True
          print(curr_node, child_node)
          queue.append(child_node)
          cont += 1

  for k in graph.adjacencyList.keys():
    if finish:
      break
    if not seen[k]:
      bfsUtil(k)


#bfs(cityGraph)