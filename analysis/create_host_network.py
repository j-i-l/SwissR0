__author__ = 'Jonas I Liechti'


import pickle
import random
import numpy as np
import glob

#percentage of the potentially susceptible population
potential_susceptible = 0.01
#which year to take the population sizes
year = 1950
pickle_name = '%d_w_%s_pot_susceptibles' % (year, str(potential_susceptible).replace('.', '_'))


def get_dist(a, b):
    return ((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) ** 0.5

#slope = (0 - 0.01) / float(100000)
p_loc = 0.01


#def linear_decay(dist):
#    """
#        returns the probability for a connection given a linear decay
#    """
#    return max(0, p_loc + slope * dist)

gamma = 0.0001
#this is a mean distance of 1000m.

def exponential_proba(distance, ):
    """
    Returns a exponentially distributed connection probability.
    :param distance:
    :return:
    """
    return p_loc * np.exp(-1 * (gamma * distance))
#issue: remove the _corrected
the_files = glob.glob('pickles/host_distributions/' + pickle_name + '_*_corrected.p')
print the_files
for a_file in the_files:
    print a_file
    counter = a_file.split('_')[-2].replace('.p', '')
    print counter
    with open(a_file, 'rb') as f:
        ok_names, susc = pickle.load(f)  #this is a list of names and a list of hosts per name

    distances = [[] for _ in range(len(susc))]
    edges = [[] for _ in range(len(susc))]
    degrees = [[] for _ in range(len(susc))]
    for i in xrange(len(susc)):
        distances[i] = [[] for _ in range(len(susc[i]))]
        edges[i] = [[] for _ in range(len(susc[i]))]
        degrees[i] = [0 for _ in range(len(susc[i]))]
    print susc.index([])
    print distances[susc.index([])]
    for i in xrange(len(susc)):
        print 'on ', ok_names[i]
        for j in xrange(len(susc[i]) - 1):
            for _j in xrange(j + 1, len(susc[i])):
                dist = get_dist(susc[i][j], susc[i][_j])
                if random.random() < exponential_proba(dist):
                    distances[i][j].append(dist)
                    distances[i][_j].append(dist)
                    edges[i][j].append((i, _j))
                    edges[i][_j].append((i, j))
            for _i in xrange(i + 1, len(susc)):
                for _j in xrange(len(susc[_i])):
                    dist = get_dist(susc[i][j], susc[_i][_j])
                    if random.random() < exponential_proba(dist):
                        distances[i][j].append(dist)
                        distances[_i][_j].append(dist)
                        edges[i][j].append((_i, _j))
                        edges[_i][_j].append((i, j))
            degrees[i][j] = len(edges[i][j])
        if len(susc[i]):
            j = -1
            for _i in xrange(i + 1, len(susc)):
                for _j in xrange(len(susc[_i])):
                    dist = get_dist(susc[i][j], susc[_i][_j])
                    if random.random() < exponential_proba(dist):
                        distances[i][j].append(dist)
                        distances[_i][_j].append(dist)
                        edges[i][j].append((_i, _j))
                        edges[_i][_j].append((i, j))
            degrees[i][j] = len(edges[i][j])

    #issue: remove the _corrected
    with open('pickles/host_networks/' + pickle_name + '_ploc_' + str(p_loc).replace('.', '_') + '_gamma_' +
                      str(gamma).replace('.', '_') + '_' + counter + '_corrected.p', 'wb') as f:
        pickle.dump((ok_names, edges, degrees, distances), f)