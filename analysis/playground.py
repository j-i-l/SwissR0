__author__ = 'Jonas I Liechti'
from matplotlib import pyplot as plt
from geograph import *

hosts_grid = [range(1000), range(1000, 2000), range(2000, 3000), range(3000, 4000), range(4000, 5000), range(5000, 6000)]
print hosts_grid

p_loc = 0.01
gamma = 0.2


def exponential_proba(distance, ):
    """
    Returns a exponentially distributed connection probability.
    :param distance:
    :return:
    """
    return p_loc * np.exp(-1 * (gamma * distance))

degs, edges, grid_deg = create_local_scale_free_network(hosts_grid, exponential_proba)

s_deg = list(set(degs))
s_deg.sort()
deg_count = [0] * len(s_deg)
for i in xrange(len(s_deg)):
    deg_count[i] = degs.count(s_deg[i])
plt.scatter(s_deg, deg_count,)
plt.xscale('log')
plt.yscale("log")
#bins = np.linspace(0, 3, 101)
#plt.xticks(bins, ["2^%s" % i for i in bins])
#plt.hist(deg, log=True,)# bins=bins)
#plt.hist(deg, bins=np.linspace(0, 100, 101),)
plt.show()