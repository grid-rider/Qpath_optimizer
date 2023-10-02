# @file test.py
# @author Evan Brody
# @brief Ties things together to test

from map import get_nyc_graph, gen_pgrid
from graph import Vertex
from PathFinder import PathFinder

def main(c1: tuple, c2: tuple):
    nyc_graph = get_nyc_graph()
    
    s = Vertex(c1[0], c1[1])
    t = Vertex(c2[0], c2[1])
    s.eval(nyc_graph.ppoints)
    t.eval(nyc_graph.ppoints)
    
    nyc_graph.add_vertex(s)
    nyc_graph.add_vertex(t)
    edge = nyc_graph.connect_vertices(s.index, t.index)
    nyc_graph.cull_not_in_rect(s, t)
    
    nyc_matrix = nyc_graph.gen_matrix()
    print("Matrix shape:", nyc_matrix.shape)
    pf = PathFinder(nyc_matrix)
    solution = pf.find_sp(s.index, t.index)
    print(solution)
    print("======")
    coords = []
    for i in solution:
        v = nyc_graph.vertices[i]
        coords.append((v.lat, v.lon))
        print(v.lat, v.lon)
        
    return coords

c3 = (-73.978138, 40.679835)
c4 = (-73.917568, 40.718213)

main(c3, c4)