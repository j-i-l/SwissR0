__author__ = 'Jonas I Liechti'

import pickle
import matplotlib as mpl
from matplotlib import pyplot as plt
import matplotlib.cm as cm
import numpy as np
from descartes import PolygonPatch
from geograph import plot_for_talks
from math import log
import glob

# #percentage of the potentially susceptible population
potential_susceptible = 0.01
#which year to take the population sizes
year = 1950
#ref year
ref_year = 2000
#the local connectivity
p_loc = 0.1
#rate of the exponential distribution
gamma = 0.0001
counter = 0
pickle_name = '%d_w_%s_pot_susceptibles' % (year, str(potential_susceptible).replace('.', '_')) \
    + '_ploc_' + str(p_loc).replace('.', '_') + '_gamma_' + str(gamma).replace('.', '_')

#ref year
ref_pickle_name = '%d_w_%s_pot_susceptibles' % (ref_year, str(potential_susceptible).replace('.', '_')) \
    + '_ploc_' + str(p_loc).replace('.', '_') + '_gamma_' + str(gamma).replace('.', '_')


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


#load info from the volkszaehlung
with open('pickles/VZ_data/' + str(year) + '_district_names.p', 'r') as p_f:
    vz_dist_names = pickle.load(p_f)
with open('pickles/VZ_data/' + str(year) + '_district_counts.p', 'r') as p_f:
    vz_dist_count = pickle.load(p_f)

with open('pickles/network_data/' + pickle_name + '_averaged.p', 'r') as f:
    ok_names, averaged_r0s, averaged_distances, averaged_degrees = pickle.load(f)
#get the ref values
with open('pickles/network_data/' + ref_pickle_name + '_averaged.p', 'r') as f:
    ref_ok_names, ref_averaged_r0s, ref_averaged_distances, ref_averaged_degrees = pickle.load(f)

rel_diff_r0s = map(
    lambda i: averaged_r0s[i] / float(ref_averaged_r0s[i]) if ref_averaged_r0s[i] else 0, xrange(len(averaged_r0s))
)

#get the deviation from the average
overall_avg_r0 = sum(averaged_r0s) / float(len(averaged_r0s))

norm_averaged_r0s = map(lambda x: x / overall_avg_r0, averaged_r0s)


#get the deviation from the average
ref_overall_avg_r0 = sum(ref_averaged_r0s) / float(len(ref_averaged_r0s))

ref_norm_averaged_r0s = map(lambda x: x / ref_overall_avg_r0, ref_averaged_r0s)

min_val = min(rel_diff_r0s)
max_val = max(rel_diff_r0s)

print min_val, max_val
my_cmap = cm.get_cmap('autumn_r')  # or any other one
norm = mpl.colors.Normalize(min_val, max_val)  # the color maps work for [0, 1]
#norm = mpl.colors.LogNorm(min_val, max_val)  # the color maps work for [0, 1]


plot_for_talks()
fig, ax = plt.subplots()
#print sum(areas)
#for i in xrange(len(map_dist_polygons)):
for dist_name in map_dist_names:
    if dist_name in ok_names:
        map_id = map_dist_names.index(dist_name)
        _id = ok_names.index(dist_name)
    else:
        map_id = map_dist_names.index(dist_name)
        _id = -1
    if _id == -1:
        color_i = 'gray'
        alpha = 0
    else:
        if averaged_r0s[_id] == 0:
            color_i = 'gray'
        else:
            color_i = my_cmap(norm(rel_diff_r0s[_id]))
        alpha = 1
    simplified_polygon = map_dist_polygons[map_id].simplify(100)
    ax.add_patch(PolygonPatch(simplified_polygon, facecolor=color_i, edgecolor=(1, 1, 1, 0.), linewidth=0.01, alpha=alpha, zorder=1))

#addig the lakes and stuff
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
    if vz_id < 0:
        if vz_id == -2:
            color_i = 'blue'
        elif vz_id == -1:
            color_i = 'gray'
        simplified_polygon = map_dist_polygons[map_id].simplify(100)
        ax.add_patch(PolygonPatch(simplified_polygon, facecolor=color_i, edgecolor=(1, 1, 1, 0.), linewidth=0.01, zorder=1))


#ax.add_collection(PolyCollection(polygons, closed=True))
ax.autoscale_view()
plt.axis('off')
plt.savefig("plots/r0_%d_rel_diff_0_01.svg" % year, bbox_inches='tight')
plt.show()

fig1, ax1 = plt.subplots(figsize=(1, 10))
fig1.subplots_adjust(top=0.95, bottom=0.01, left=0.3, right=0.99)
gradient = np.linspace(0, 1, 256)
gradient = np.vstack((gradient, gradient))
y_pos = np.linspace(0, 256, 6)
new_y_labels = map(lambda x: str(round(x, 1)), np.linspace(min_val, max_val, 6))
ax1.get_xaxis().set_visible(False)
ax1.set_yticks(y_pos)
# set the tick labels
ax1.set_yticklabels(new_y_labels)

ax1.imshow(gradient.T, aspect='auto', cmap=my_cmap)
#y_pos = np.linspace(0, 256, 10)
ax1.get_xaxis().set_visible(False)
#fig.text(x_text, y_text, name, va='center', ha='right', fontsize=10)
fig1.savefig("plots/r0_%d_colormap_rel_diff_0_01.svg" % year, bbox_inches='tight')
plt.show()