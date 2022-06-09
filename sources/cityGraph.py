import json
import random

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

  def traffic_by_hour(self):
    pass

  def calculate_traffic_factor(val):
    pass

  def calculate_weight(self):
    pass

  def update_weight(self):
    pass

adjacencyListPath = "adjacency_list.json"
streetsPath = "calles.json"
intersectionsPath = "intersecciones.json"