# @file graph.py
# @author Evan Brody, Ninad Moharir
# @brief Implements classes for working with undirected, weighted graphs.

import numpy as np
import math

# TODO: Add automatic weight calculation to the constructors for Vertex and Edge, once the eval functions are in a workable state.

# Represents a vertex on a graph overlaid on the Earth's surface.
# @field lat float The latitude of the point.
# @field lng float The longitude of the point.
# @field edges Edge[] The edges this vertex is connected to.
# @field weight float How appropriate this location is for a subway station.
#                     A lower weight value means that it's more appropriate.
# @field index int The index this has in its graph's vertex array.
class Vertex:
    def __init__(self, lat: float, lng: float, weight: float=None, index: int=None) -> None:
        self.lat = lat
        self.lng = lng
        self.edges = []
        self.weight = weight
        self.index = index

    # Returns the distance from this vertex to another.
    # @field other Vertex The vertex to calculate distance to.
    # @return float The distance to the other vertex.
    def dist(self, other: Vertex) -> float:
        return sqrt((self.lat - other.lat) ** 2 + (self.lng - other.lng) ** 2)

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
