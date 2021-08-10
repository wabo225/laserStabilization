from typing import Callable
import numpy as np
from lib.BristolAnalysis import openBristolFile
from scipy.constants import c


path_to_data = "../../Data"

def _pm(midpoint, separation):
  return midpoint - separation, midpoint + separation

def _linInterp(x0,y0,x1,y1,x2,y2) -> Callable:
  # point slope form interpolation
  return lambda x : y2 + (x-x2)*((y1-y0)/(x1-x0))

def GHZtoNM(GHz):
  return c/GHz


def findSlopeOnSawtooth(x:np.ndarray, y:np.ndarray=None):
  '''
  if y is not given, the function tries to use the second column of x
  if both are given, they are assumed to have shape (1,n) or (n,1)
  '''
  if y is None:
    y = x[:,1]
    x = x[:,0]

  # print(*y, sep='\n')
  # print(*x, sep='\n')
  
  return np.min(y), np.max(y)
  
def getCorrection(Piezo_of_Transition: float, Theoretical_Value: float, wavelength_calibration_filename = 'wavelengthCalibration'):
  '''
  Piezo_of_Transition: (V)
  Theoretical_Value: (GHz)
  '''
  d = openBristolFile(path_to_data + '/' + wavelength_calibration_filename +'.csv')
  freqRange = findSlopeOnSawtooth(d[:,0:2]) 
  with open(path_to_data + '/'+wavelength_calibration_filename+'Meta.txt') as meta:
    current = float(meta.readline().split()[1])
    scanAmplitude = float(meta.readline().split()[1])
    scanOffset = float(meta.readline().split()[1])
    scanFrequency = float(meta.readline().split()[1])
  
  scanRange = _pm(scanOffset, scanAmplitude/2)
  # print(f'{scanRange=}')
  # print(f'{freqRange=}')

  return _linInterp(scanRange[0], freqRange[0],scanRange[1],freqRange[1], Piezo_of_Transition, Theoretical_Value)


if __name__ == "__main__":
  getCorrection()
