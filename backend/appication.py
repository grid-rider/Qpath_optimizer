from flask import Flask, request
import json, sys, os

from map import get_nyc_graph, gen_pgrid
from graph import Vertex
from PathFinder import PathFinder



application = Flask(__name__)

@application.route("/path/generate", methods=["POST"])
def generate():
        
    def find_path(start_point: dict, end_point: dict):
        nyc_graph = get_nyc_graph()
        
        s = Vertex(start_point["lng"], start_point["lat"])
        t = Vertex(end_point["lng"], end_point["lat"])
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
            coords.append({"lat" : v.lat, "lng" : v.lon})
            
        return coords

    
    content_type = request.headers.get('Content-Type')
    try:
        if (content_type == 'application/json'):
            parsed_reqest = request.json
            start_point = parsed_reqest.get("start_point")
            end_point = parsed_reqest.get("end_point")
            
            print(start_point["lat"])
            # path = [start_point, { "lat": 40.7431, "lng": -73.971321 }, { "lat": 40.7531, "lng": -73.961321 }, end_point] #ToDo Generate ideal path
            path = find_path(start_point, end_point)
            print(path)
            return json.dumps({"path" : path}), 200 #OK 
        else:
            return 'Content-Type not supported!', 400 #Bad-request
    except Exception as e:
        print("Error occured ", e)
        return ("Server side error: " + str(e)), 500  #Server-side error 

if __name__ == "__main__":
	application.run(host='0.0.0.0', port=80, debug=True) ## Using webcommon port 80    




# def find_path(start_point: dict, end_point: dict):
#     nyc_graph = get_nyc_graph()
    
#     s = Vertex(start_point["lng"], start_point["lat"])
#     t = Vertex(end_point["lng"], end_point["lat"])
#     s.eval(nyc_graph.ppoints)
#     t.eval(nyc_graph.ppoints)

#     nyc_graph.add_vertex(s)
#     nyc_graph.add_vertex(t)
#     edge = nyc_graph.connect_vertices(s.index, t.index)
#     nyc_graph.cull_not_in_rect(s, t)
    
#     nyc_matrix = nyc_graph.gen_matrix()
#     print("Matrix shape:", nyc_matrix.shape)
#     pf = PathFinder(nyc_matrix)
#     print(s.index, t.index)
#     solution = pf.find_sp(s.index, t.index)
#     print(solution)
#     print("======")
#     coords = []
#     for i in solution:
#         v = nyc_graph.vertices[i]
#         coords.append({"lat" : v.lat, "lng" : v.lon})
        
#     return coords

# if __name__ == "__main__":  
#     find_path({ "lat": 40.69225180346094, "lng": -73.98728337928011 }, { "lat": 40.72533293170276, "lng": -73.9516821667593 })