__author__ = 'Jonas I Liechti'

from geograph import plot_for_talks
import pickle
import matplotlib as mpl
from matplotlib import pyplot as plt
import matplotlib.cm as cm
import numpy as np
from descartes import PolygonPatch
from math import log


ref_year = 2000
#which year to take the population sizes
year = 2000

#load info from the map
with open('pickles/map/district_polygons.p', 'r') as f:
    map_dist_polygons = pickle.load(f)
with open('pickles/map/district_names.p', 'r') as f:
    map_dist_names = pickle.load(f)
with open('pickles/map/district_bounds.p', 'r') as f:
    map_dist_bounds = pickle.load(f)
with open('pickles/map/district_areas.p', 'r') as f:
    map_dist_areas = pickle.load(f)

#matching names:
with open('pickles/matched_' + str(year) + '_district_names.p', 'r') as f:
    ok_names = pickle.load(f)
with open('pickles/mapping_' + str(year) + '_district_names.p', 'r') as f:
    mapping = pickle.load(f)


#load ref_year info from the volkszaehlung
with open('pickles/VZ_data/' + str(ref_year) + '_district_names.p', 'r') as p_f:
    ref_vz_dist_names = pickle.load(p_f)
with open('pickles/VZ_data/' + str(ref_year) + '_district_counts.p', 'r') as p_f:
    ref_vz_dist_count = pickle.load(p_f)
print ref_vz_dist_count
#load info from the volkszaehlung
with open('pickles/VZ_data/' + str(year) + '_district_names.p', 'r') as p_f:
    vz_dist_names = pickle.load(p_f)
with open('pickles/VZ_data/' + str(year) + '_district_counts.p', 'r') as p_f:
    vz_dist_count = pickle.load(p_f)

population_total = sum(vz_dist_count)


#rescaled_count = map(lambda x: int(round(potential_susceptible * x, 0)), vz_dist_count)

min_val = min(ref_vz_dist_count)
max_val = max(ref_vz_dist_count)
print min_val, max_val
#min_val += 0.0000000000001


my_cmap = cm.get_cmap('autumn_r')  # or any other one
#norm = mpl.colors.LogNorm(min_val, max_val)  # the color maps work for [0, 1]
norm = mpl.colors.Normalize(min_val, 10000)  # the color maps work for [0, 1]

plot_for_talks()
fig, ax = plt.subplots()
#print sum(areas)
#for i in xrange(len(map_dist_polygons)):
for dist_name in map_dist_names:

    if dist_name in vz_dist_names:
        map_id = map_dist_names.index(dist_name)
        vz_id = vz_dist_names.index(dist_name)
    elif '/' in dist_name:
        vz_id = vz_dist_names.index(dist_name)
        map_id = map_dist_names.index(dist_name.replace('/', ''))
    elif 'Saas ' in dist_name:
        vz_id = vz_dist_names.index(dist_name)
        map_id = map_dist_names.index(dist_name.replace('Saas ', 'Saas-'))
    elif dist_name in mapping:
        vz_id = vz_dist_names.index(dist_name)
        map_id = map_dist_names.index(mapping[dist_name])
    elif 'see' in dist_name and dist_name not in vz_dist_names:
        map_id = map_dist_names.index(dist_name)
        vz_id = -2
    elif u'see ' in dist_name or u'Lac' in dist_name or u'Lago' in dist_name:
        map_id = map_dist_names.index(dist_name)
        vz_id = -2
    else:
        map_id = map_dist_names.index(dist_name)
        vz_id = -1
    if vz_id == -2:
        color_i = 'blue'
    elif vz_id == -1:
        color_i = 'gray'
    else:
        color_i = my_cmap(norm(vz_dist_count[vz_id]))
    simplified_polygon = map_dist_polygons[map_id].simplify(100)
    ax.add_patch(PolygonPatch(simplified_polygon, facecolor=color_i, edgecolor=(1, 1, 1, 0.), linewidth=0.01, zorder=1))
#ax.add_collection(PolyCollection(polygons, closed=True))
ax.autoscale_view()
plt.axis('off')
plt.savefig("plots/vz_%d_normal.svg" % year, bbox_inches='tight')
plt.show()

fig1, ax1 = plt.subplots(figsize=(1, 10))
fig1.subplots_adjust(top=0.95, bottom=0.01, left=0.3, right=0.99)
gradient = np.linspace(0, 1, 256)
gradient = np.vstack((gradient, gradient))
ax1.imshow(gradient.T, aspect='auto', cmap=my_cmap)
#y_pos = np.linspace(0, 256, 10)
"""
biggest = int(log(max_val, 10))
y_pos = [biggest/log(max_val, 10) * 256]
y_labels = [unicode('$' + '10^{%s}' % str(biggest) + '$')]
print biggest
print biggest
print max_val
while biggest:
    y_pos.append(biggest/log(max_val, 10) * 256)
    y_labels.append(unicode('$' + '10^{%s}' % str(biggest) + '$'))
    biggest -= 1
#y_pos = np.linspace(0, 256, 10)
#new_y_labels = map(lambda x: str(round(x, 1)), np.linspace(min_val, max_val, 10))
ax1.get_xaxis().set_visible(False)
ax1.set_yticks(y_pos[::-1])
#ax1.set_yscale('log')
# set the tick labels
ax1.set_yticklabels(y_labels[::-1])#new_y_labels)
"""
y_pos = np.linspace(0, 256, 10)
new_y_labels = map(lambda x: str(round(x, 1)), np.linspace(min_val, 10000, 10))
ax1.get_xaxis().set_visible(False)

#fig.text(x_text, y_text, name, va='center', ha='right', fontsize=10)
fig1.savefig("plots/vz_%d_colormap_normal.svg" % year, bbox_inches='tight')
plt.show()