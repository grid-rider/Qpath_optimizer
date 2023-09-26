# @file map.py
# @author Evan Brody
# @brief Defines functions that can create an info-rich grid overlay on NYC.

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
LAT_MIN = 40.48
LON_MAX = -73.65
LAT_MAX = 40.93

PRECISION = 20

NYC_CSV = "data/nyc_pop_data.csv"

def gen_pgrid(filename: str) -> list:
    nyc_pop = pd.read_csv(filename)

    pgrid = []

    for i in nyc_pop.index:
        lon = nyc_pop["Longitude"][i]
        lat = nyc_pop["Latitude"][i]
        pop = nyc_pop["TotalPop"][i]

        pgrid.append(PopPoint(lon, lat, pop))
        
    return pgrid

def gen_vgrid(pgrid: list) -> list:
    lons = np.linspace(LON_MIN, LON_MAX, PRECISION)
    lats = np.linspace(LAT_MIN, LAT_MAX, PRECISION)
    
    gpgrid = GeoSeries([Point(lon, lat) for lon in lons for lat in lats])
    boroughs = GeoDataFrame.from_file("data/boroughs/borough_bounds.shp")
    in_nyc = np.array([gpgrid.within(geom) for geom in boroughs.geometry]).sum(axis=0)
    gpgrid = GeoSeries([pt for i, pt in enumerate(gpgrid) if in_nyc[i]])

    vgrid = [Vertex(pt.x, pt.y) for pt in gpgrid]
    for v in vgrid: v.eval(pgrid)

    return vgrid

def get_nyc_grid():
    pgrid = gen_pgrid()
    return gen_vgrid(pgrid)