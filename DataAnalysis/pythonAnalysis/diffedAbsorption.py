import matplotlib
import numpy as np
from matplotlib import pyplot as plt
from os import listdir

from numpy.core.fromnumeric import shape

path_to_data = '../../Data/Topas Data'

def callback(filterString: str):
    return lambda file_name : -1 != file_name.find(filterString) and file_name.endswith('.csv')

file_filter = "L1Difference1"

csv_paths = list(filter(callback(file_filter), listdir(path_to_data)))

for csv in csv_paths:
    with open(path_to_data + '/'  + csv) as f:
        xl, yl, temp1, temp2 = f.readline().split(';')
        dat = np.genfromtxt(f,dtype=float, delimiter=';')
        # plt.plot(dat[:,0],dat[:,2])
        print(np.shape(dat))
        # dat[:,1] = dat[:,1] - dat[:,2]
        print(dat[:,1])
        # plt.pause(0.5)
        # plt.plot(dat[:,0], dat[:,1])
        # plt.xlabel(xl)
        # plt.ylabel(yl)
        plt.autoscale()

plt.show()
