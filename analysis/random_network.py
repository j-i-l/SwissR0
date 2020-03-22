__author__ = 'Jonas I Liechti'
CONTENT = """
    generate a random network (Erdos-Renjy) with the geoGraph method.
"""
from geograph import *

N = 10000
L = 1000
grid = range(L)
#constant host density
rho = N / float(L)
#constant connection probability
p_c = 0.1


def const_density(coord ):
    """
    Return a constant density at each coord.
    :param coord:
    :return:
    """
    return rho


def constant_proba(distance ):
    """
    Returns a constant connection probability.
    :param distance:
    :return:
    """
    return p_c

density_grid = create_host_density(geo_grid=grid, density_fct=const_density)
host_grid = create_hosts(density_grid)
deg, e_l = create_network(host_grid, constant_proba)

from matplotlib import pyplot as plt

average_degree = sum(deg) / float(len(deg))
print average_degree
plt.hist(deg, bins=np.linspace(800, 1200, 401),)
plt.show()