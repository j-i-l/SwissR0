__author__ = 'Jonas I Liechti'
import time
import numpy as np
from numpy import random as nrand


def create_host_density(geo_grid, density_fct, conversion=None):
    """
    create the host distribution as a grid
    :param geo_grid: the space on which the hosts will be distributed.
    :param density_fct: function that returns the density as a fct on the spacial coordinates
    :param conversion: function to handle the conversion from grid coordinates (indexes) to arguments of the
        density function
    :return:
    """
    try:
        len(geo_grid[0])
        dim = 2
    except TypeError:
        dim = 1
    except IndexError:
        IndexError('geo_grid must be a list or list of lists.')
    if dim == 1:
        density_dist = []
        for coord in geo_grid:
            density_dist.append(density_fct(coord))
    else:
        print 'This is not implemented jet...'
    return density_dist

#resolution = 1
#grid = np.linspace(0, L - resolution, L / float(resolution))


def create_hosts(density_grid):
    host_grid = []
    counter = 0
    for cell in density_grid:
        host_grid.append([])
        for _ in xrange(int(cell)):
            host_grid[-1].append(counter)
            counter += 1
    return host_grid

from bisect import bisect_left


def create_hosts_proba(density_grid, N):
    """
    This method uses a probabilistic approach to place the hosts on the grid
    :param density_grid:
    :param N: Size of the network
    :return:
    """
    total_ = float(sum(density_grid))
    cumul_resc_density_grid = map(lambda x: x / total_, density_grid)
    cumul_resc_density_grid = [sum(cumul_resc_density_grid[:i]) for i in xrange(1, len(cumul_resc_density_grid))]
    host_grid = [[] for _ in xrange(len(density_grid))]
    counter = 0
    for _ in xrange(N):
        host_grid[bisect_left(cumul_resc_density_grid, nrand.rand())].append(counter)
        counter += 1
    print host_grid
    return host_grid


def create_network(host_grid, connection_proba_fct, scale_free=False):
    """
    This method creates the network and returns a list of edges.
    Note: This method works only for 1D structures.
    :param host_grid:
    :param connection_proba_fct:
    :return:
    """
    if scale_free:
        pass
    else:
        nrand.seed(int(time.time()))  #create a new seed.
        edges = []  #will hold the list of edges (tubles).
        degrees = [0] * (max(max(host_grid, key=lambda x: max(x) if len(x) else 0)) + 1)
        for i in xrange(len(host_grid)):
            for j in xrange(len(host_grid[i])):
                for _i in xrange(len(host_grid[:i+1])):
                    if _i == i:
                        max_index = min(j, len(host_grid[i]))
                    else:
                        max_index = len(host_grid[_i])
                    for _j in xrange(max_index):
                        if nrand.rand() < connection_proba_fct(i - _i):
                            edges.append((host_grid[i][j], host_grid[_i][_j]))
                            degrees[host_grid[i][j]] += 1
                            degrees[host_grid[_i][_j]] += 1

        return degrees, edges


def create_local_scale_free_network(host_grid, connection_proba_fct):
    """
    This method is intended to create scale free host_distributions with geographical constraints.

    :param host_grid:
    :param connection_proba_fct:
    :return:
    """
    edges = []
    N = max(max(host_grid, key=lambda x: max(x))) + 1
    degrees = [0] * N
    #M = N(N-1)pc
    #M = (N-2)m0
    grid_deg = [[0] * len(host_grid[i]) for i in xrange(len(host_grid))]
    m0 = 3  #to do: compute the m0 form N and the connection_proba
    #get the local scale free host_distributions
    for i in xrange(len(host_grid)):
        #do the first round: make a connection to all of the m0 initial nodes
        for _ in xrange(m0):
            edges.append((host_grid[i][m0], host_grid[i][_]))
            degrees[host_grid[i][m0]] += 1
            degrees[host_grid[i][_]] += 1
            grid_deg[i][m0] += 1
            grid_deg[i][_] += 1
        for _j in xrange(len(host_grid[i][m0:])):
            j = _j + m0
            for _ in xrange(m0):  #add the m0 links
                deg_dist = [sum(grid_deg[i][:_k]) / float(sum(grid_deg[i][:j])) for _k in xrange(1, j + 1)]
                _index = bisect_left(deg_dist, nrand.rand())  #get the node to which we want to connect
                edges.append((host_grid[i][j], host_grid[i][_index]))
                degrees[host_grid[i][j]] += 1
                degrees[host_grid[i][_index]] += 1
                grid_deg[i][j] += 1
                grid_deg[i][_index] += 1
    #get the scale free host_distributions inbetween locations.
    #this is wind random connections inbetween
    for i in xrange(1, len(host_grid)):
        for j in xrange(len(host_grid[i])):
            for _i in xrange(len(host_grid[:i])):
                if _i == i:
                    max_index = min(j, len(host_grid[i]))
                else:
                    max_index = len(host_grid[_i])
                for _j in xrange(max_index):
                    if nrand.rand() < connection_proba_fct(i - _i):
                        edges.append((host_grid[i][j], host_grid[_i][_j]))
                        degrees[host_grid[i][j]] += 1
                        degrees[host_grid[_i][_j]] += 1
    return degrees, edges, grid_deg


def create_global_scale_free_network(host_grid, connection_proba_fct):
    """
    This method is intended to create scale free host_distributions with geographical constraints.

    :param host_grid:
    :param connection_proba_fct:
    :return:
    """
    edges = []
    N = max(max(host_grid, key=lambda x: max(x))) + 1
    degrees = [0] * N
    #M = N(N-1)pc
    #M = (N-2)m0
    grid_deg = [[0] * len(host_grid[i]) for i in xrange(len(host_grid))]
    m0 = 3  #to do: compute the m0 form N and the connection_proba
    #get the local scale free host_distributions
    for i in xrange(len(host_grid)):
        #do the first round: make a connection to all of the m0 initial nodes
        for _ in xrange(m0):
            edges.append((host_grid[i][m0], host_grid[i][_]))
            degrees[host_grid[i][m0]] += 1
            degrees[host_grid[i][_]] += 1
            grid_deg[i][m0] += 1
            grid_deg[i][_] += 1
        for _j in xrange(len(host_grid[i][m0:])):
            j = _j + m0
            for _ in xrange(m0):  #add the m0 links
                deg_dist = [sum(grid_deg[i][:_k]) / float(sum(grid_deg[i][:j])) for _k in xrange(1, j + 1)]
                _index = bisect_left(deg_dist, nrand.rand())  #get the node to which we want to connect
                edges.append((host_grid[i][j], host_grid[i][_index]))
                degrees[host_grid[i][j]] += 1
                degrees[host_grid[i][_index]] += 1
                grid_deg[i][j] += 1
                grid_deg[i][_index] += 1
    #get the scale free host_distributions inbetween locations.
    #this is wind random connections inbetween
    #to do!
    return degrees, edges, grid_deg


def get_distance(n1, n2, hosts_grid):
    """
    Compute the distance between the two nodes
    :param n1:
    :param n2:
    :return:
    """
    _runner = len(hosts_grid)
    no_exit = 2  #each match reduces -> after the 2nd match no_exit is false.
    i1, i2 = None, None
    while no_exit:
        if not _runner:
            print 'at least one of the two nodes could not be found in the hosts_grid'
            break
        if n1 in hosts_grid[_runner - 1]:  #the -1 comes form _runner being len of hosts_grid, so we are 1 off.
            i1 = _runner
            no_exit -= 1
        if n2 in hosts_grid[_runner - 1]:
            i2 = _runner
            no_exit -= 1
        _runner -= 1
    try:
        return abs(i1 - i2)
    except TypeError:
        raise TypeError('at least one of the two nodes could not be found in the hosts_grid')