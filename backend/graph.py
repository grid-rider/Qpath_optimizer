# @file graph.py
# @author Evan Brody, Ninad Moharir
# @brief Implements classes for working with undirected, weighted graphs.

from __future__ import annotations
from shapely.geometry import Point, Polygon
import numpy as np
import math

# TODO: Add automatic weight calculation to the constructors for Vertex and Edge, once the eval functions are in a workable state.

PENALTY = 99999

# Represents a cluster of population.
# @field lon float The longitude of the point.
# @field lat float The latitude of the point.
# @field pop int The total population associated with this point.
class PopPoint:
    def __init__(self, lon: float, lat: float, pop: int) -> None:
        self.lon = lon
        self.lat = lat
        self.pop = pop
    
    # Returns the distance from this point to a vertex.
    # @field other Vertex The vertex to calculate distance to.
    # @return float The distance to the vertex.
    def dist(self, other: Vertex):
        return math.sqrt((self.lon - other.lon) ** 2 + (self.lat - other.lat) ** 2)

# Represents a vertex on a graph overlaid on the Earth's surface.
# @field lon float The longitude of the vertex.
# @field lat float The latitude of the vertex.
# @field edges Edge[] The edges this vertex is connected to.
# @field weight float How appropriate this location is for a subway station.
#                     A lower weight value means that it's more appropriate.
# @field index int The index this has in its graph's vertex array.
class Vertex:
    pop_rad = 1 / 60 # in degrees, approx. 1 mile
    def __init__(self, lon: float, lat: float, weight: float=None, index: int=None) -> None:
        self.lon = lon
        self.lat = lat
        self.edges = []
        self.weight = weight
        self.index = index

    # Returns the distance from this vertex to another.
    # @field other Vertex The vertex to calculate distance to.
    # @return float The distance to the other vertex.
    def dist(self, other: Vertex) -> float:
        return math.sqrt((self.lon - other.lon) ** 2 + (self.lat - other.lat) ** 2)
    
    # Evaluates the appropriateness of this location for a subway station.
    # @param pop_points PopPoint[] The population points to consider.
    def eval(self, pop_points: list) -> None:
        weighted_pop_count = 0
        for p in pop_points:
            dist = p.dist(self)
            if dist <= self.pop_rad and dist != 0:
                weighted_pop_count += p.pop / dist
        
        if weighted_pop_count != 0:
            self.weight = 1 / weighted_pop_count
        else:
            self.weight = float('inf')

# Represents a connection between two vertices.
# @field vtx1 Vertex The first vertex.
# @field vtx2 Vertex The second vertex.
# @field weight float How "costly" it is to move along this edge.
class Edge:
    def __init__(self, vtx1: Vertex, vtx2: Vertex, weight: float=None) -> None:
        self.vtx1 = vtx1
        self.vtx2 = vtx2
        self.weight = weight
        
        self.vtx1.edges.append(self)
        self.vtx2.edges.append(self)

    # Returns the length of this edge.
    # @return float The distance from vertex 1 to vertex 2.
    def length(self) -> float:
        return self.vtx1.dist(self.vtx2)

# Represents a collection of vertices and any edges that may connect them.
# @field vertices Vertex[] The set of vertices in the graph.
# @field edges Edge[] The set of edges in the graph.
class Graph:
    def __init__(self, vertices: list=[], edges: list=[]) -> None:
        self.vertices = vertices.copy()
        self.edges = edges.copy()
        
        for i, v in enumerate(self.vertices):
            v.index = i
    
    # Adds a vertex to the graph.
    # @param v Vertex The vertex to add.
    def add_vertex(self, v: Vertex) -> None:
        self.vertices.append(v)
    
    # Adds an edge to the graph.
    # @param e Edge The edge to add.
    def add_edge(self, e: Edge) -> None:
        self.edges.append(e)
        
    # Connects two given vertices within the graph.
    # @param v1 Vertex The index of the first vertex.
    # @param v2 Vertex The index of the second vertex.
    # @return Edge The created edge, or None if creation fails.
    def connect_vertices(self, v1: int, v2: int) -> Edge:
        for edge in self.edges:
            if edge.vtx1.index == v1 and edge.vtx2.index == v2 or \
               edge.vtx1.index == v2 and edge.vtx2.index == v1:
                return None
        
        new_edge = Edge(v1, v2)
        self.edges.append(new_edge)
        
        return new_edge

    # Generates a weight graph from the edges and vertices given.
    # @return 2-D numpy array The weight graph.
    def gen_matrix(self) -> np.array:

        # Creates a regular 2-D array with weights.
        # Initializes all weights to infinity.
        reg_matrix = [[float('inf')] * len(self.vertices) for _ in range(len(self.vertices))]
        for edge in self.edges:
            i1 = edge.vtx1.index
            i2 = edge.vtx2.index
            reg_matrix[i1][i2] = edge.weight
            reg_matrix[i2][i1] = edge.weight

        # Makes sure weights of edges that start and end at the same vertex are infinity.
        for i in range(len(self.edges)):
            reg_matrix[i][i] = float('inf')

        # Converts regular array to numpy array.
        np_matrix = []
        for row in reg_matrix:
            np_row = np.array(row)
            np_matrix.append(np_row)
        np_matrix = np.array(np_matrix)

        return np_matrix