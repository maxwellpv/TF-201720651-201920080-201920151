import json
import math

class CityGraph:
  def __init__(self, adjacencyListPath, streetsPath, intersectionsPath):
    self.adjacencyList = {}
    self.streets = {}
    self.intersections = {}

    self.initGraph(adjacencyListPath, streetsPath, intersectionsPath)

  def initGraph(self, adjacencyListPath, streetsPath, intersectionsPath):
    with open(adjacencyListPath, mode="r", encoding="utf-8") as f:
      self.adjacencyList = json.load(f)

    with open(streetsPath, mode="r", encoding="utf-8") as f:
      streetsList = json.load(f)

      for element in streetsList:
        k, v = element

        key = tuple(element[k])
        value = element[v]

        self.streets[key] = value

    with open(intersectionsPath, mode="r", encoding="utf-8") as f:
      self.intersections = json.load(f)

  def traffic_by_hour(self, time):
    factor = round(5 * math.cos(2 * (time / 3) - 1) * math.sin((time / 6) - 2) + 5, 3)
    if factor > 10: return 10
    if factor < 0: return 0
    return factor

  def calculate_traffic_factor(self, val, time):
    value = val * self.traffic_by_hour(time)
    # Rango esperado... Perlin[0..50] * Hora[0..10] = [0-500]
    # Rango deseado [0-50]
    return value / 10

  def calculate_weight(self, val, length, time):
    return length * self.calculate_traffic_factor(val, time)

  def update_weight(self, key, time):
    self.streets[key].weight = self.calculate_weight(self.streets[key].val, self.streets[key].length, time)

adjacencyListPath = "adjacency_list.json"
streetsPath = "calles.json"
intersectionsPath = "intersecciones.json"