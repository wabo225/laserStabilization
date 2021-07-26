import numpy as np
from matplotlib import pyplot as plt

a = np.loadtxt("LaserOnPixelData.txt", dtype=int)
print(np.sum(a[:,0]*a[:,1]))