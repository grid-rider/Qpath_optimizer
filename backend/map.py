# @file map.py
# @author Evan Brody
# @brief Defines functions that can create an info-rich grid overlay on NYC.

import os
import numpy as np
from geopandas import GeoDataFrame, GeoSeries
from shapely.geometry import Point, Polygon
import pandas as pd
from graph import (
    PopPoint,
    Vertex,
    Edge,
    Graph
)

LON_MIN = -74.28
LON_MAX = -73.65
LAT_MIN = 40.48
LAT_MAX = 40.93
PRECISION = 30
NYC_CSV = "data/nyc_pop_data.csv"

# Generates a list of PopPoints given a file to read from.
# @param filename str The name of the file to read from.
# @return PopPoint[] A list of PopPoints with the given data.
def gen_pgrid(filename: str) -> list:
    
    nyc_pop = pd.read_csv(os.path.join(os.path.dirname(__file__),filename))

    pgrid = []

    for i in nyc_pop.index:
        lon = nyc_pop["Longitude"][i]
        lat = nyc_pop["Latitude"][i]
        pop = nyc_pop["TotalPop"][i]

        pgrid.append(PopPoint(lon, lat, pop))
        
    return pgrid

# Generates a list of vertices given a list of PopPoints
# to calculate weights from.
# @param pgrid PopPoints[] A list of PopPoints to calculate weights with
# @return Vertex[] A list of weighted vertices
def gen_vgrid(pgrid: list) -> list:
    lons = np.linspace(LON_MIN, LON_MAX, PRECISION)
    lats = np.linspace(LAT_MIN, LAT_MAX, PRECISION)
    
    gpgrid = GeoSeries([Point(lon, lat) for lon in lons for lat in lats])
    boroughs = GeoDataFrame.from_file(os.path.join(os.path.dirname(__file__),"data/boroughs/borough_bounds.shp"))
    in_nyc = np.array([gpgrid.within(geom) for geom in boroughs.geometry]).sum(axis=0)
    gpgrid = GeoSeries([pt for i, pt in enumerate(gpgrid) if in_nyc[i]])

    vgrid = [Vertex(pt.x, pt.y) for pt in gpgrid]
    for v in vgrid: v.eval(pgrid)

    return vgrid

# Generates a graph using NYC population data.
# @return Graph A graph with weighted vertices and edges.
def get_nyc_graph() -> Graph:
    pgrid = gen_pgrid(NYC_CSV)
    vgrid = gen_vgrid(pgrid)
    
    nyc_graph = Graph(vgrid)
    nyc_graph.ppoints = pgrid
    
    for i, v1 in enumerate(vgrid):
        for j, v2 in enumerate(vgrid):
            if i == j: continue
            if v1.dist(v2) > Vertex.min_dist: continue
            edge = nyc_graph.connect_vertices(i, j)
            if edge is not None: edge.eval()
    
    return nyc_graph