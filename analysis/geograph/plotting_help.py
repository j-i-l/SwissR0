__author__ = 'Jonas I Liechti'
import matplotlib as mpl
def plot_for_talks():
    mpl.rcParams['font.size'] = 40
    mpl.rcParams['lines.linewidth'] = 3
    #mpl.rcParams['font.family'] = 'Comic Sans MS'
    #mpl.rcParams['axes.labelsize'] = 10
    mpl.rcParams['figure.subplot.left'] = .2
    mpl.rcParams['figure.subplot.right'] = .8
    mpl.rcParams['figure.subplot.bottom'] = .2
    mpl.rcParams['figure.subplot.top'] = .8