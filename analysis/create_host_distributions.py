__author__ = 'Jonas I Liechti'

import pickle
import random
from shapely.geometry import Point

counters = range(10)
for counter in counters:
    #percentage of the potentially susceptible population
    potential_susceptible = 0.01
    #which year to take the population sizes
    year = 2000
    pickle_name = '%d_w_%s_pot_susceptibles_%s_corrected.p' % (year, str(potential_susceptible).replace('.', '_'), str(counter))

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

    population_total = sum(vz_dist_count)

    rescaled_count = map(lambda x: int(round(potential_susceptible * x, 0)), vz_dist_count)

    susc = []
    for dist_name in ok_names:
        print dist_name
        if '/' in dist_name:
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
            vz_id = -1
        elif u'see ' in dist_name or u'Lac' in dist_name or u'Lago' in dist_name:
            map_id = map_dist_names.index(dist_name)
            vz_id = -1
        elif dist_name in vz_dist_names:
            map_id = map_dist_names.index(dist_name)
            vz_id = vz_dist_names.index(dist_name)
        else:
            map_id = map_dist_names.index(dist_name)
            vz_id = -1
        district_bounds = map_dist_bounds[map_id]
        district_poly = map_dist_polygons[map_id]
        its_nodes = []
        if vz_id >= 0:
            #issue: so far we will have always 1 dude in each district
            for node in xrange(max(1, rescaled_count[vz_id])):
                x_tent = 0.
                y_tent = 0.
                not_in = True
                while not_in:
                    x_tent = random.uniform(district_bounds[0], district_bounds[2])
                    y_tent = random.uniform(district_bounds[1], district_bounds[3])
                    if district_poly.contains(Point(x_tent, y_tent)):
                        its_nodes.append((x_tent, y_tent))
                        not_in = False
        #print len(its_nodes)
        susc.append(its_nodes)
    print 'total: ', sum(map(lambda x: len(x), susc))
    with open('pickles/host_distributions/' + pickle_name, 'wb') as f:
        pickle.dump((ok_names, susc), f)
    #from matplotlib import pyplot as plt

    #for suscs in susc:
    #    plt.plot(*zip(*suscs), linestyle='None', marker='o', markeredgecolor='None')
    #plt.show()

#for suscs in susc:
#    plt.plot(*zip(*suscs), linestyle='None', marker='o', markeredgecolor='None')
#plt.show()

    #print susc
            #while ()