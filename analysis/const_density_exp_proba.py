__author__ = 'Jonas I Liechti'
CONTENT = """
    generate a random network (Erdos-Renjy) with the geoGraph method.
"""
from geograph import *
from matplotlib import pyplot as plt

N = 1000
L = 100
grid = range(L)
#constant host density
rho = N / float(L)
#local connection probability
p_loc = 0.1
#decay rate
gamma = 0.1



def const_density(coord ):
    """
    Return a constant density at each coord.
    :param coord:
    :return:
    """
    return rho


def exponential_proba(distance, ):
    """
    Returns a exponentially distributed connection probability.
    :param distance:
    :return:
    """
    return p_loc * np.exp(-1 * (gamma * distance))

plt.plot(xrange(100), [exponential_proba(distance) for distance in xrange(100)])
plt.show()

density_grid = create_host_density(geo_grid=grid, density_fct=const_density)
host_grid = create_hosts_proba(density_grid, N)
plt.plot(range(len(host_grid)), [len(host_grid[i]) for i in range(len(host_grid))])
plt.show()
#print get_distance(33, 1, host_grid)
print host_grid
deg, e_l = create_network(host_grid, exponential_proba)

average_degree = sum(deg) / float(len(deg))
print average_degree
plt.hist(deg, bins=np.linspace(0, 100, 101),)
plt.show()