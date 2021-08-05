from math import floor
from typing import Tuple, List
import numpy as np
from os import listdir

# from scipy import optimize
# from scipy.stats import norm

# this file defines a function to separate out some of the more complicated numpy indexing

def dataExtractor(path_to_data: str, filename_filter: str, headerSize:int=1, delim:str=',') -> List[np.ndarray]:
  ''' Takes data out of a set of files and returns a list of ndarrays'''
  
  def callback(file_name: str):
    return file_name.endswith('.csv') and file_name.find(filename_filter) != -1

  filenames = list(filter(callback, listdir(path_to_data)))

  out = []
  for filename in filenames:
    with open(f'{path_to_data}/{filename}') as f:
      [f.readline() for i in range(headerSize)]
      out.append(np.genfromtxt(f, dtype=float,delimiter=delim))
  return out


def removeSections(a: np.ndarray, indeces: Tuple):
  '''
  Starting from off, each index toggles the inclusion rows below it. 
  It is the Union of datapoints between the indexes of every second element in indeces and its right neighbor
  '''
  if len(indeces)%2==1:
    raise ValueError(f"Parameter Indeces must contain an even number of elements. Contains {len(indeces)}")
  if max(indeces) > np.shape(a)[0]:
    raise IndexError(f"Toggling input out of range of supplied array. index: {max(indeces)} > len: {np.shape(a)[0]}")
  return np.concatenate([a[indeces[i]:indeces[i+1],:] for i in range(0,len(indeces),2)])

if __name__ == "__main__":
  toggleIndeces = (0, 10, 90, 100)
  example = np.reshape(np.arange(0,100), (100,1))
  # out = np.concatenate((example, np.random.rand(100,2)))
  out = np.concatenate((example, np.random.rand(100,2)), axis=1)
  out = removeSections(out, toggleIndeces)
  print(out)
