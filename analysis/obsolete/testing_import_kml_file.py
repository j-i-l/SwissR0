__author__ = 'Jonas I Liechti'
from pykml import parser

with open('Data/cantons.kml', 'r') as f:
    doc = parser.parse(f)

root = doc.getroot()

print len(root.Document.getchildren())

switzerland = root.Document.getchildren()[0]

print 'n', switzerland.name

print 'content count ', len(switzerland.getchildren())

switzerland_name = switzerland.getchildren()[0].pyval
switzerland_style = switzerland.getchildren()[1].getchildren()
print switzerland_style
cantons = switzerland.getchildren()[3:]

print 'cantons:\n', '\n'.join(map(lambda x: x.name.pyval, cantons))

cantons_names = [canton.getchildren()[0].pyval for canton in cantons]
cantons_styles = [canton.getchildren()[1].getchildren() for canton in cantons]
print cantons_styles
outer_boundaries = []
for canton in cantons:
    try:
        outer_boundaries.append(canton.Polygon.outerBoundaryIs.LinearRing.coordinates.pyval.split(' '))
    except AttributeError:
        for part in canton.MultiGeometry.getchildren():
            outer_boundaries.append(part.outerBoundaryIs.LinearRing.coordinates.pyval.split(' '))


#print 'districts', outer_boundaries
outer_coords = []
outer_xs = []
outer_ys = []
for boundaries in outer_boundaries:
    outer_coords.append(map(lambda x: tuple(map(lambda xx: float(xx), x.split(','))), boundaries))
    xs, ys = zip(*outer_coords[-1])
    outer_xs.append(xs)
    outer_ys.append(ys)

from matplotlib import pyplot as plt
for i in xrange(len(outer_xs)):
    plt.plot(outer_xs[i], outer_ys[i])
plt.show()