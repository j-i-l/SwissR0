__author__ = 'Jonas I Liechti'

import pickle
import matplotlib as mpl
from matplotlib import pyplot as plt
import matplotlib.cm as cm
import numpy as np
from descartes import PolygonPatch

# #percentage of the potentially susceptible population
potential_susceptible = 0.001
#which year to take the population sizes
year = 2000
#the local connectivity
p_loc = 0.1
#rate of the exponential distribution
gamma = 0.0001
counter = 0
pickle_name = '%d_w_%s_pot_susceptibles' % (year, str(potential_susceptible).replace('.', '_')) \
    + '_ploc_' + str(p_loc).replace('.', '_') + '_gamma_' + str(gamma).replace('.', '_') + '_' + str(counter)

with open('pickles/host_networks/' + pickle_name + '.p', 'rb') as f:
    ok_names, all_names, all_susc, edges, degrees, distances = pickle.load(f)
degrees.append(len(edges[-1]))


def get_R0(n_id):
    neighbours_degrees = [degrees[nn] for nn in edges[n_id]]
    deg = len(neighbours_degrees)
    return sum([max(0, k - 1) * neighbours_degrees.count(k) / float(deg) for k in set(neighbours_degrees)])

def get_avg_dist(n_id):
    neighbours_dists = distances[n_id]
    deg = len(neighbours_dists)
    return sum(neighbours_dists) / float(deg) if deg else 0


r0s = []
avg_distances = []
for n_id in xrange(len(all_susc)):
    avg_distances.append(get_avg_dist(n_id))
    r0s.append(get_R0(n_id))
print r0s
print avg_distances
avg_r0 = sum(r0s) / float(len(r0s))
avg_avg_dist = sum(avg_distances) / float(len(avg_distances))
print avg_r0, avg_avg_dist


#reorder them by district
#the counter for ok_names:
c = 0
current_district = ok_names[c]
distr_names = [current_district]
if current_district == all_names[0]:
    distr_degrees = [[degrees[0]]]
    distr_r0s = [[r0s[0]]]
    distr_avg_dist = [[avg_distances[0]]]
else:
    distr_degrees = [[]]
    distr_r0s = [[]]
    distr_avg_dist = [[]]
for i in xrange(1, len(all_names)):
    if all_names[i] != current_district:
        c += 1
        if all_names[i] == ok_names[c]:
            current_district = all_names[i]
            distr_names.append(current_district)
            distr_degrees.append([])
            distr_r0s.append([])
            distr_avg_dist.append([])
        else:
            while all_names[i] != ok_names[c]:
                print 'empty district', ok_names[c]
                distr_names.append(ok_names[c])
                distr_degrees.append([])
                distr_r0s.append([])
                distr_avg_dist.append([])
                c += 1
            current_district = all_names[i]
    distr_degrees[-1].append(degrees[i])
    distr_r0s[-1].append(r0s[i])
    distr_avg_dist[-1].append(avg_distances[i])
for _i in xrange(c, len(ok_names)):
    distr_names.append(ok_names[_i])
    distr_degrees.append([])
    distr_r0s.append([])
    distr_avg_dist.append([])
print distr_names
print distr_r0s
district_avg_r0s = map(lambda x: sum(x) / float(len(x)) if len(x) else 0, distr_r0s)
print district_avg_r0s
print sum(district_avg_r0s) / float(len(district_avg_r0s))

with open('pickles/network_data/' + pickle_name + '.p', 'w') as f:
    pickle.dump((ok_names, distr_degrees, distr_avg_dist, distr_r0s), f)

#load info from the map
with open('pickles/map/district_polygons.p', 'r') as f:
    map_dist_polygons = pickle.load(f)
with open('pickles/map/district_names.p', 'r') as f:
    map_dist_names = pickle.load(f)
with open('pickles/map/district_bounds.p', 'r') as f:
    map_dist_bounds = pickle.load(f)
with open('pickles/map/district_areas.p', 'r') as f:
    map_dist_areas = pickle.load(f)

#get the matched district names:
with open('pickles/matched_' + str(year) + '_district_names.p', 'r') as f:
    ok_names = pickle.load(f)

min_val = min(district_avg_r0s)
max_val = max(district_avg_r0s)

my_cmap = cm.get_cmap('jet')  # or any other one
norm = mpl.colors.Normalize(min_val, max_val)  # the color maps work for [0, 1]

print len(district_avg_r0s)
print len(distr_names)
print len(ok_names)
print len(map_dist_names)
#to do: this is somehow not of the same length.
fig, ax = plt.subplots()
#print sum(areas)
#for i in xrange(len(map_dist_polygons)):
for dist_name in map_dist_names:
    if dist_name in distr_names:
        vz_id = distr_names.index(dist_name)
        color_i = my_cmap(norm(district_avg_r0s[vz_id]))
    else:
        color_i = 'blue'
    map_id = map_dist_names.index(dist_name)
    simplified_polygon = map_dist_polygons[map_id].simplify(100)
    ax.add_patch(PolygonPatch(simplified_polygon, facecolor=color_i, edgecolor='none', alpha=0.8, zorder=1))

#ax.add_collection(PolyCollection(polygons, closed=True))
ax.autoscale_view()
plt.axis('off')
plt.savefig("plots/test.svg", bbox_inches='tight')
plt.show()

fig1, ax1 = plt.subplots(figsize=(2, 10))
fig1.subplots_adjust(top=0.95, bottom=0.01, left=0.3, right=0.99)
gradient = np.linspace(0, 1, 256)
gradient = np.vstack((gradient, gradient))
ax1.imshow(gradient.T, aspect='auto', cmap=my_cmap)
y_pos = np.linspace(0, 256, 6)
new_y_labels = map(lambda x: str(round(x, 1)), np.linspace(min_val, max_val, 6))
ax1.get_xaxis().set_visible(False)
ax1.set_yticks(y_pos)
# set the tick labels
ax1.set_yticklabels(new_y_labels)
pos = list(ax1.get_position().bounds)
x_text = pos[0] - 0.01
y_text = pos[1] + pos[3]/2.
labels = [item.get_text() for item in ax1.get_yticklabels()]
print ax1.get_yticklabels()
print labels

labels[1] = 'Testing'
ax.set_xticklabels(labels)
#fig.text(x_text, y_text, name, va='center', ha='right', fontsize=10)
plt.show()