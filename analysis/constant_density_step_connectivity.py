__author__ = 'Jonas I Liechti'
CONTENT = """
    generate a locally random network with step function for the connection probability and
     constant host density.
     We use the geoGraph method.
"""
from geograph import *
from matplotlib import pyplot as plt

N = 10000
L = 1000
grid = range(L)
#constant host density
rho = N / float(L)
#local connection probability
p_loc = 0.1
#limit distance:
d_l = 20
#decay rate
gamma = 0.1



def const_density(coord):
    """
    Return a constant density at each coord.
    :param coord:
    :return:
    """
    return rho


def step_proba(distance, ):
    """
    Returns a constant connection probability.
    :param distance:
    :return:
    """
    if distance <= d_l:
        return p_loc
    else:
        return 0

plt.plot(xrange(100), [step_proba(distance) for distance in xrange(100)])
plt.show()

density_grid = create_host_density(geo_grid=grid, density_fct=const_density)
host_grid = create_hosts(density_grid)
print get_distance(333, 1, host_grid)
deg, e_l = create_network(host_grid, step_proba)

average_degree = sum(deg) / float(len(deg))
print average_degree
plt.hist(deg, bins=np.linspace(0, 100, 101),)
plt.show()