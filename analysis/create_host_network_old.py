__author__ = 'Jonas I Liechti'


import pickle
import random
import numpy as np
import glob

counter = 1

#percentage of the potentially susceptible population
potential_susceptible = 0.001
#which year to take the population sizes
year = 1950
pickle_name = '%d_w_%s_pot_susceptibles' % (year, str(potential_susceptible).replace('.', '_'))


def get_dist(a, b):
    return ((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) ** 0.5

#slope = (0 - 0.01) / float(100000)
p_loc = 0.1


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


print 'pickles/host_distributions/' + pickle_name + '.p'
the_files = glob.glob('pickles/host_distributions/' + pickle_name + '_*.p')
print the_files
for a_file in the_files:
    print a_file
    counter = a_file.split('_')[-1].replace('.p', '')
    print counter
    with open(a_file, 'rb') as f:
        ok_names, susc = pickle.load(f)  #this is a list of names and a list of hosts per name
    """
    all_susc = []
    all_names = []

    #pw_distance = []
    for i in xrange(len(susc)):
        all_susc.extend(susc[i])
        all_names.extend([ok_names[i] for _ in xrange(len(susc[i]))])
    N = len(all_susc)
    edges = [[] for _ in xrange(N)]
    degrees = []
    distances = [[] for _ in xrange(N)]
    for i in xrange(N - 1):
        for j in xrange(i + 1, N):
            distance = get_dist(all_susc[i], all_susc[j])
            if random.random() < exponential_proba(distance):
                edges[i].append(j)
                edges[j].append(i)
                distances[i].append(distance)
                distances[j].append(distance)
            #edges[-1].append((i, j))
            #pw_distance[-1].append(get_dist(all_susc[i], all_susc[j]))
        degrees.append(len(edges[i]))
        print N - i, degrees[-1]
    degrees.append(len(edges[-1]))
"""

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

    #with open('pickles/host_networks/' + pickle_name + '_ploc_' + str(p_loc).replace('.', '_') + '_gamma_' +
    #                  str(gamma).replace('.', '_') + '_' + counter + '_other.p', 'wb') as f:
    #    pickle.dump((ok_names, all_names, all_susc, edges, degrees, distances), f)

    with open('pickles/host_networks/' + pickle_name + '_ploc_' + str(p_loc).replace('.', '_') + '_gamma_' +
                      str(gamma).replace('.', '_') + '_' + counter + '_other.p', 'wb') as f:
        pickle.dump((ok_names, edges, degrees, distances), f)

from matplotlib import pyplot as plt

#plt.hist(degrees, bins=20, normed=True)
#plt.show()