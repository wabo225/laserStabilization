from typing import List, Tuple
import numpy as np
from lib import DataIsolation
from scipy.stats import linregress
from matplotlib import pyplot as plt
from scipy.optimize import minimize
from scipy.ndimage import convolve
plt.rcParams['axes.facecolor'] = 'AAAAAA'

def linearlyRemoveBackground(data: List[np.ndarray], Indeces: List[Tuple], N=10):
  assert len(data) == len(Indeces)
  
  # isolate points where abs second derivative is greater than a threshold
  isFromTopas = True
  background_isolated = []
  
  for i in range(len(data)):
    
    if isFromTopas:
      data[i] = data[i][:,0:3]
    
    # apply moving average via convolution
      # this convolution does not mutate the data. It is only used for picking valuable toggle points for use in DataIsolation.removeSections()
    d2 = np.concatenate((data[i][:,0:1], convolve(data[i][:,1:], np.reshape(np.ones(N)/N,(N,1)), mode='constant')), axis=1)
    
    # Take the numerical derivative
    d2 = np.concatenate((d2[:,0:1],np.array([np.gradient(d2[:,j]) for j in range(1,np.shape(d2)[1])]).T), axis=1)

    # Take the Absolute Value
    d2 = np.abs(d2)
    
    # Take the numerical derivative again
    d2 = np.concatenate((d2[:,0:1],np.array([np.gradient(d2[:,j]) for j in range(1,np.shape(d2)[1])]).T), axis=1)

    # plt.plot(d2[:,0], d2[:,1])

    # plt.plot(d2[:,0],d2[:,1])
    background_isolated.append(DataIsolation.removeSections(data[i], Indeces[i]))
  return background_isolated

if __name__ == "__main__":
  path_to_files = '../../Data/TOPAS Data'
  filter_str = 'Overlap2'
  arrays = DataIsolation.dataExtractor(path_to_files, filter_str)
  background = linearlyRemoveBackground(arrays, [[0,122,366,449,570,664, 728,729]])
  
  linResult1 = linregress(background[0][:,0],background[0][:,1])
  linResult2 = linregress(background[0][:,0],background[0][:,2])
  line = lambda linRegressResult : lambda x : linRegressResult[0]*x + linRegressResult[1]
  linearBackgroundReducedDoppler = np.array(arrays[0][:729,1]) - np.array([line(linResult1)(x) for x in arrays[0][:729,0]])
  linearBackgroundReducedDopplerFree =np.array(arrays[0][:729,2]) - np.array([line(linResult2)(x) for x in arrays[0][:729,0]])
  
  fn = lambda gain : sum((gain*linearBackgroundReducedDoppler-linearBackgroundReducedDopplerFree)**2)
  linearBackgroundReducedDoppler = minimize(fn, x0=1).x[0]*linearBackgroundReducedDoppler
  # plt.plot(arrays[0][:729,0],linearBackgroundReducedDopplerFree-linearBackgroundReducedDoppler,color='blue')
  plt.plot(arrays[0][:729,0],linearBackgroundReducedDoppler,color='orange')
  plt.plot(arrays[0][:729,0],linearBackgroundReducedDopplerFree,color='red')
  

  plt.autoscale()
  plt.show()