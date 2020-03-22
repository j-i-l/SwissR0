__author__ = 'Jonas I Liechti'
import dxfgrabber
from matplotlib import pylab as plt
from matplotlib.collections import PolyCollection
import pickle


def area_of_polygon(x, y):
    """Calculates the area of an arbitrary polygon given its verticies"""
    area = 0.0
    for i in xrange(-1, len(x)-1):
        area += x[i] * (y[i+1] - y[i-1])
    return abs(area) / 2.0

fig, ax = plt.subplots()
dxf = dxfgrabber.readfile('Data/dxf/GG25_A_B_v2.dxf')
#for _ in xrange(len(dxf.entities)):
    #print dxf.entities[_].layer
polygons = []
areas = []
names = []
for _ in xrange(len(dxf.entities)):
    try:
        polygons.append(dxf.entities[_].points)
        areas.append(area_of_polygon(*zip(*dxf.entities[_].points)))
        names.append(dxf.entities[_].layer)
    #    x, y = zip(*dxf.entities[_].points)
    #    plt.plot(x, y, label=dxf.entities[_].layer)
    except AttributeError:
        new_block = dxf.blocks.get(dxf.entities[_].name)
        ref_point = list(dxf.entities[_].insert)[:-1]
        missing_element = map(lambda x: (x[0] + ref_point[0], x[1] + ref_point[1]), new_block[0].points)
        missing_element.append(missing_element[0])#polygons.append(missing_element)
        for i in xrange(1, len(new_block)):
            to_cut = map(lambda x: (x[0] + ref_point[0], x[1] + ref_point[1]), new_block[i].points)
            to_cut.append(to_cut[0])
            to_cut.append(missing_element[-1])
            missing_element.extend(to_cut)
        #cop = {"type": "Polygon", "coordinates": [missing_element]}
        #print shape(cop).area
        polygons.append(missing_element)
        areas.append(area_of_polygon(*zip(*missing_element)))
        names.append(dxf.entities[_].layer)
#ax.autoscale_view()
#plt.legend()

#with open('pickles/map_district_names.p', 'w') as p_f:
#    pickle.dump(names, p_f)

print sum(areas)
ax.add_collection(PolyCollection(polygons, closed=True))
ax.autoscale_view()
plt.show()