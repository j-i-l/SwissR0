__author__ = 'Jonas I Liechti'

import matplotlib as mpl
from matplotlib import pyplot as plt
import numpy as np
from geograph import plot_for_talks


gamma = 0.0001
#this is a mean distance of 1000m.
p_loc = 0.1

dists = np.linspace(1, 100000, 100001)

def exponential_proba(distance, ):
    """
    Returns a exponentially distributed connection probability.
    :param distance:
    :return:
    """
    return p_loc * np.exp(-1 * (gamma * distance))

plot_for_talks()
mpl.rcParams['font.size'] = 20
#print filter(lambda x: 'axes' in x, mpl.rcParams.keys())

fig, ax = plt.subplots()
ax.plot(dists, map(lambda x: exponential_proba(x), dists), color='red')
ax_ticks = ax.get_xticks()
ax.set_xticks(ax_ticks)
print ax_ticks[0]
#ax1.set_yscale('log')
# set the tick labels
ax.set_xticklabels(map(lambda x: str(int(x / 1000.)), ax_ticks))
ax.set_xlabel('distance [km]')
ax.set_ylabel(u'$p_{c}$', fontsize=25)
fig.savefig('plots/used_exp_dist.svg', bbox_inches='tight')
fig.savefig('plots/used_exp_dist.pdf', bbox_inches='tight')
plt.show()