import numpy as np
from scipy.ndimage import convolve

def rollingAverage(d: np.ndarray, N:int=10) -> np.ndarray:
  '''
    This function returns an array of equal size to the one given, with each column 
    (except the first) representing an average of the 10 points near itself.

    @param d: np.ndarray   columns with time data
    @param N: int    Represents the size of the convolution filter. 
    @returns np.ndarray
  '''
  return np.concatenate((d[:,0:1], convolve(d[:,1:], np.reshape(np.ones(N)/N,(N,1)), mode='constant')), axis=1)
  
def numDer(d: np.ndarray) -> np.ndarray:
  '''
    This function takes the numerical derivative of all of the columns 
    (Except the first), and returns an array of the same size.
    
    @param d: np.ndarray   columns with time data
    @returns np.ndarray
    
    @todo Make to take the Nth derivative?
  '''
  # Take the numerical derivative
  return np.concatenate((d[:,0:1],np.array([np.gradient(d[:,j]) for j in range(1,np.shape(d)[1])]).T), axis=1)
