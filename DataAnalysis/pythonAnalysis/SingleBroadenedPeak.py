import numpy as np
from matplotlib import pyplot as plt
from lib.posterTheme import Colors
from lib.statsCalculus import numDer

plt.rcParams['axes.facecolor'] = Colors.gray

path_to_data = '../../Data/TOPAS Data'
filename = 'L1Difference2.csv'

with open(path_to_data+'/'+filename) as f:
  columns = f.readline().split()
  dat = np.genfromtxt(f,delimiter=',')
  dat2 = numDer(dat)

plt.grid(ls='--')
plt.plot(dat[:,0],dat[:,2], color=Colors.red)
plt.plot(dat2[:,0],dat2[:,2]+0.3*np.ones(np.shape(dat2[:,2])), color=Colors.ukblue)

plt.xlabel('Peizo (V)')
plt.ylabel('Transmission Intensity')
plt.title(r'Hyperfine ${}^{87}Rb \; F=3$ Spectrum')

plt.show()