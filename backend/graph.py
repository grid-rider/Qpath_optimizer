# @file graph.py
# @author Evan Brody
# @brief Implements classes for working with undirected, weighted graphs.

import numpy as np

# TODO: Add automatic weight calculation to the constructors for Vertex and Edge, once the eval functions are in a workable state.

# Represents a vertex on a graph overlaid on the Earth's surface.
# @field lat float The latitude of the point.
# @field lng float The longitude of the point.
# @field weight float How appropriate this location is for a subway station.
#                     A lower weight value means that it's more appropriate.
# @field index int The index this has in its graph's vertex array.
class Vertex:
    def __init__(self, lat: float, lng: float, weight: float=None, index: int=None) -> None:
        self.lat = lat
        self.lng = lng
        self.weight = weight
        self.index = index

# Represents a connection between two vertices.
# @field vtx1 Vertex The first vertex.
# @field vtx2 Vertex The second vertex.
# @field weight float How "costly" it is to move along this edge.
class Edge:
    def __init__(self, vtx1: Vertex, vtx2: Vertex, weight: float=None) -> None:
        self.vtx1 = vtx1
        self.vtx2 = vtx2
        self.weight = weight

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
    def add_vertex(v: Vertex) -> None:
        self.vertices.append(v)
    
    # Adds an edge to the graph.
    # @param e Edge The edge to add.
    def add_edge(e: Edge) -> None:
        self.edges.append(e)
        
    # Connects two given vertices within the graph.
    # @param v1 Vertex The index of the first vertex.
    # @param v2 Vertex The index of the second vertex.
    # @return Edge The created edge, or None if creation fails.
    def connect_vertices(v1: int, v2: int) -> Edge:
        for edge in self.edges:
            if edge.vtx1.index == v1 and edge.vtx2.index == v2 or \
               edge.vtx1.index == v2 and edge.vtx2.index == v1:
                return None
        
        new_edge = Edge(v1, v2)
        self.edges.append(new_edge)
        
        return new_edge
