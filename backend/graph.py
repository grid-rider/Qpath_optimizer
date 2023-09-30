# @file graph.py
# @author Evan Brody, Ninad Moharir
# @brief Implements classes for working with undirected, weighted graphs.

from __future__ import annotations
from shapely.geometry import Point, Polygon
from PathFinder import PathFinder
import numpy as np
import math

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
    min_dist = 0 # approx. 1 mile
    pop_rad = 1 / 60 # approx. 1 mile
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
            self.weight = 1

# Represents a connection between two vertices.
# @field vtx1 Vertex The first vertex.
# @field vtx2 Vertex The second vertex.
# @field weight float How "costly" it is to move along this edge.
# @field index int The index this has in its Graph's edge list.
class Edge:
    def __init__(self, vtx1: Vertex, vtx2: Vertex, weight: float=None, index: int=None) -> None:
        self.vtx1 = vtx1
        self.vtx2 = vtx2
        self.weight = weight
        self.index = index
        
        self.vtx1.edges.append(self)
        self.vtx2.edges.append(self)

    # Returns the length of this edge.
    # @return float The distance from vertex 1 to vertex 2.
    def length(self) -> float:
        return self.vtx1.dist(self.vtx2)
    
    # Evaluates how "costly" it is to move along this edge.
    def eval(self) -> None:
        self.weight = self.vtx1.weight * self.vtx2.weight * (self.length() ** 2) * 10**20

# Represents a collection of vertices and any edges that may connect them.
# @field vertices Vertex[] The set of vertices in the graph.
# @field edges Edge[] The set of edges in the graph.
# @field ppoints PopPoint[] The relevant population data.
class Graph:
    def __init__(self, vertices: list=[], edges: list=[], ppoints: list=[]) -> None:
        self.vertices = vertices.copy()
        self.edges = edges.copy()
        self.ppoints = ppoints.copy()
        
        for i, v in enumerate(self.vertices):
            v.index = i
            
        for i, e in enumerate(self.edges):
            e.index = i
    
    # Adds a vertex to the graph.
    # @param v Vertex The vertex to add.
    def add_vertex(self, v: Vertex) -> None:
        self.vertices.append(v)
        v.index = len(self.vertices) - 1
        # Connect it to every vertex past a given distance
        for v2 in self.vertices:
            if v.dist(v2) < Vertex.min_dist: continue
            new_edge = self.connect_vertices(v.index, v2.index)
            if new_edge is not None: new_edge.eval()
    
    # Adds an edge to the graph.
    # @param e Edge The edge to add.
    def add_edge(self, e: Edge) -> None:
        self.edges.append(e)
        e.index = len(self.edges) - 1
        e.eval()
        
    # Removes a vertex from the graph along with all of its edges.
    # @param vi int The index of the vertex to remove.
    def remove_vertex(self, vi: int) -> None:
        if vi > len(self.vertices) - 1: return
        for i in range(vi+1, len(self.vertices)):
            self.vertices[i].index -= 1
        
        removed_vertex = self.vertices.pop(vi)
        removed_vertex.index = None
        
        to_remove = []
        for e in self.edges:
            if e.vtx1.index == None or e.vtx2.index == None:
                to_remove.append(e.index)
        
        for i in range(len(to_remove) - 1, -1, -1):
            self.remove_edge(to_remove[i])
        
    # Removes an edge from the graph.
    # @param ei int The index of the edge to remove.
    def remove_edge(self, ei: int) -> None:
        if ei > len(self.edges) - 1: return
    
        for i in range(ei+1, len(self.edges)):
            self.edges[i].index -= 1
        
        removed_edge = self.edges.pop(ei)
        removed_edge.index = None
        
    # Connects two given vertices within the graph.
    # @param v1 Vertex The index of the first vertex.
    # @param v2 Vertex The index of the second vertex.
    # @return Edge The created edge, or None if creation fails.
    def connect_vertices(self, v1i: int, v2i: int) -> Edge:
        for edge in self.edges:
            if edge.vtx1.index == v1i and edge.vtx2.index == v2i or \
               edge.vtx1.index == v2i and edge.vtx2.index == v1i:
                return None
        
        new_edge = Edge(self.vertices[v1i], self.vertices[v2i])
        self.add_edge(new_edge)
        
        return new_edge
    
    # Removes any vertices not within the rectangle specified
    # by the two parameter vertices, along with any edges crossing
    # outside the rectangle.
    # @param v1 Vertex The first corner of the rectangle.
    # @param v2 Vertex The second corner of the rectangle.
    def cull_not_in_rect(self, v1: Vertex, v2: Vertex) -> None:
        # Finding the corners of our rectangle
        alat = v1.lat if v1.lat < v2.lat else v2.lat
        blat = v1.lat if v1.lat > v2.lat else v2.lat
        
        alon = v1.lon if v1.lon < v2.lon else v2.lon
        blon = v1.lon if v1.lon > v2.lon else v2.lon
        
        # Culling
        to_remove = []
        for v in self.vertices:
            if v == v1 or v == v2: continue
            if alat < v.lat < blat and alon < v.lon < blon: continue
            to_remove.append(v.index)
            
        for i in range(len(to_remove) - 1, -1, -1):
            self.remove_vertex(to_remove[i])

    # Generates a weight graph from the edges and vertices given.
    # @return 2-D numpy array The weight graph.
    def gen_matrix(self) -> np.array:

        # Creates a regular 2-D array with weights.
        # Initializes all weights to infinity.
        reg_matrix = [[PathFinder.penalty] * len(self.vertices) for _ in range(len(self.vertices))]
        for edge in self.edges:
            i1 = edge.vtx1.index
            i2 = edge.vtx2.index
            reg_matrix[i1][i2] = edge.weight
            reg_matrix[i2][i1] = edge.weight

        # Makes sure weights of edges that start and end at the same vertex are 0
        for i in range(len(self.vertices)):
            reg_matrix[i][i] = 0

        # Converts regular array to numpy array.
        np_matrix = []
        for row in reg_matrix:
            np_row = np.array(row)
            np_matrix.append(np_row)
        np_matrix = np.array(np_matrix)

        return np_matrix