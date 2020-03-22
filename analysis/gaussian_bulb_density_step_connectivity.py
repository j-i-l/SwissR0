__author__ = 'Jonas I Liechti'
CONTENT = """
    generate a locally random network with step function for the connection probability and
     gaussian bulb for host density.
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
#Gaussian parameters
a = 3
b = L / 2.
c = 15.
d = 2
#integral of the gaussian is only defined for d = 0 and is a* abs(c) * (np.pi)**(0.5)


def gaussian_density(coord):
    """
    Return a constant density at each coord.
    :param coord:
    :return:
    """
    return a * np.exp(-1 * (coord - b)**2 / float(2 * c**2)) + d


def step_proba(distance, ):
    """
    Returns a constant connection probability.
    :param distance:
    :return:
    """
    if distance <= d_l:
        return p_loc
    else:
        return 0.

plt.plot(xrange(L), [gaussian_density(coord) for coord in xrange(L)])
plt.show()

density_grid = create_host_density(geo_grid=grid, density_fct=gaussian_density)
print density_grid
print max(density_grid)
host_grid = create_hosts(density_grid)
#print get_distance(333, 1, host_grid)
deg, e_l = create_network(host_grid, step_proba)

average_degree = sum(deg) / float(len(deg))
print deg
print average_degree
s_deg = list(set(deg))
s_deg.sort()
deg_count = [0] * len(s_deg)
for i in xrange(len(s_deg)):
    deg_count[i] = deg.count(s_deg[i])
plt.scatter(s_deg, deg_count,)
plt.yscale("log")
#bins = np.linspace(0, 3, 101)
#plt.xticks(bins, ["2^%s" % i for i in bins])
#plt.hist(deg, log=True,)# bins=bins)
#plt.hist(deg, bins=np.linspace(0, 100, 101),)
plt.show()