__author__ = 'Jonas I Liechti'

import numpy as np
import scipy.stats as ss
import scipy.optimize as so
from matplotlib import pyplot as plt
import pickle

year = 1980

with open('Data/Cumulative_Dist_Distance_tW_' + str(year) + '.csv', 'r') as f:
    content = f.readlines()
content = map(lambda x: x.replace('\n', '').split(','), content)
distance = []
cumulative_proba = []
for line in content:
    distance.append(max(0, float(line[0])))
    cumulative_proba.append(max(0, float(line[1])))
print distance
print cumulative_proba
print content


def to_cdf(xs, *params):
    return np.array(map(lambda x: ss.gamma.cdf(x, *params), xs))

a, b = so.curve_fit(to_cdf, np.array(distance), np.array(cumulative_proba), p0=2)
print 'mean: ', a / b
with open('pickles/distance_tW_gamma_parameter_' + str(year) + '.p', 'wb') as f:
    pickle.dump((a,b), f)

#plt.plot(distance, cumulative_proba)
plt.plot(distance, map(lambda x: ss.gamma.pdf(x, a, b)[0][0], distance))
plt.show()



#ss.rv_continuous.fit()

def cdf_exp_dist(x, l):
    return 1 - np.exp((-1) * l * x)


diff = []
lambdas = np.linspace(0.0001, 0.1, 100000)
print lambdas
for l in lambdas:
    diff.append(sum(map(lambda i: abs(cdf_exp_dist(distance[i],l) - cumulative_proba[i]), xrange(6, len(distance)))))



plt.plot(lambdas, diff)
plt.show()

id_l = lambdas[diff.index(min(diff))]

plt.plot(distance, cumulative_proba)
plt.plot(distance, map(lambda x: cdf_exp_dist(x, id_l), distance))
plt.show()
