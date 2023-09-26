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
    
    print(nyc_graph.gen_matrix())
    pf = PathFinder(nyc_graph.gen_matrix())
    print(pf.find_sp(s.index, t.index))

c1 = (-74.1, 40.5)
c2 = (-74.0, 40.6)
main(c1, c2)