__author__ = 'Jonas I Liechti'
import dxfgrabber
from matplotlib import pylab as plt
from descartes import PolygonPatch
import matplotlib as mpl
import numpy as np
import pickle
from shapely.geometry import Polygon



import matplotlib.cm as cm
import matplotlib.patches as patches






def area_of_polygon(x, y):
    """Calculates the area of an arbitrary polygon given its verticies"""
    area = 0.0
    for i in xrange(-1, len(x)-1):
        area += x[i] * (y[i+1] - y[i-1])
    return abs(area) / 2.0


dxf = dxfgrabber.readfile('Data/dxf/GG25_A_B_v2.dxf')
#for _ in xrange(len(dxf.entities)):
    #print dxf.entities[_].layer
polygons = []
areas = []
names = []
centroids = []  #those are the centers of the districts
bounds = []
for _ in range(len(dxf.entities))[:10]:
    try:
        polygons.append(Polygon(dxf.entities[_].points))
        #polygons.append(dxf.entities[_].points)
        areas.append(area_of_polygon(*zip(*dxf.entities[_].points)))
        names.append(dxf.entities[_].layer)
    #    x, y = zip(*dxf.entities[_].points)
    #    plt.plot(x, y, label=dxf.entities[_].layer)
    except AttributeError:
        new_block = dxf.blocks.get(dxf.entities[_].name)
        ref_point = list(dxf.entities[_].insert)[:-1]
        missing_element = map(lambda x: (x[0] + ref_point[0], x[1] + ref_point[1]), new_block[0].points)
        #missing_element.append(missing_element[0])#polygons.append(missing_element)
        holes = []
        for i in xrange(1, len(new_block)):
            to_cut = map(lambda x: (x[0] + ref_point[0], x[1] + ref_point[1]), new_block[i].points)
            #to_cut.append(to_cut[0])
            #to_cut.append(missing_element[-1])
            holes.append(to_cut)
            #missing_element.extend(to_cut)
        #cop = {"type": "Polygon", "coordinates": [missing_element]}
        #print shape(cop).area
        polygons.append(Polygon(missing_element, holes))
        #polygons.append(missing_element)
        areas.append(area_of_polygon(*zip(*missing_element)))
        names.append(dxf.entities[_].layer)
    #get the centroid
    centroids.append(polygons[-1].centroid.coords)
    bounds.append(polygons[-1].bounds)
#ax.autoscale_view()
#plt.legend()

#to access the exterior coords:
print list(polygons[0].exterior.coords)
#for the interior:
print polygons[0].interiors
#get the centroid point:
print polygons[0].centroid
#get the surface area:
print polygons[0].area
#give the bounding box (minx,miny,maxx,maxy)
print polygons[0].bounds
#find if a point is within a polygon:
point = polygons[0].centroid
print point.within(polygons[0])  #issue: not sure if this works properly
#get the distance between two points:
print point.distance(point)
#we can export polygons, points etc with the svg method
print point.svg()
with open('pickles/map/district_names.p', 'w') as p_f:
    pickle.dump(names, p_f)
with open('pickles/map/district_polygons.p', 'w') as p_f:
    pickle.dump(polygons, p_f)
with open('pickles/map/district_centroids.p', 'w') as p_f:
    pickle.dump(centroids, p_f)
with open('pickles/map/district_areas.p', 'w') as p_f:
    pickle.dump(areas, p_f)
with open('pickles/map/district_bounds.p', 'w') as p_f:
    pickle.dump(bounds, p_f)
