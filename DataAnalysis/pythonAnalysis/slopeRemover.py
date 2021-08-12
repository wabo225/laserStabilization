from typing import Callable, List
import numpy as np
from numpy.core.fromnumeric import argmin
from scipy.sparse.extract import find
from scipy.stats.stats import friedmanchisquare
from lib import DataIsolation
from scipy.stats import linregress
from matplotlib import pyplot as plt
from scipy.optimize import minimize, curve_fit
from scipy.signal import find_peaks
from lib import statsCalculus
from wavelengthCorrection import getCorrection, GHZtoNM
from lib.posterTheme import Colors


plt.rcParams['axes.facecolor'] = Colors.gray

def removeLinearBackground(arrays: np.ndarray, sectionsTuple: List[List[int]]= [], column:int=1, N=10):
  if len(sectionsTuple) ==0:
    sectionsTuple = [0, np.shape(arrays)[1]]
  background = DataIsolation.removeSections(arrays, sectionsTuple)
  linRegressResult = linregress(background[:,0],background[:,column])
  return lambda x : linRegressResult[0]*x + linRegressResult[1]

def removeBackgroundOfFnType(fitFunction: Callable, arrays: np.ndarray, sectionsTuple: List[List[int]]= [], column:int=1, N=10):
  '''
  fitFunction : callable
    The model function, f(x, …). It must take the independent variable as the first argument and the parameters to fit as separate remaining arguments.
  '''
  if len(sectionsTuple) ==0:
    sectionsTuple = [0, np.shape(arrays)[1]]
  background = DataIsolation.removeSections(arrays, sectionsTuple)
  popt, pcov = curve_fit(fitFunction, background[:,0],background[:,column])
  return lambda x : fitFunction(x, *popt), np.sqrt(np.diag(pcov))

parabola = lambda x, a, b, c: np.power(a*x,2) + b*x + c

ReLU = lambda y, base : [i if i > base else base for i in y]

def detectPeaks(array, base):
  pass


if __name__ == "__main__":
  path_to_files = '../../Data/TOPAS Data'
  filter_str = 'Overlap2'
  arrays = DataIsolation.dataExtractor(path_to_files, filter_str)

  sections = [0,122,366,449,570,664, 728,729]

  linResult1 = removeLinearBackground(arrays[0], sections, column=1)
  linResult2 = removeLinearBackground(arrays[0], sections, column=2)

  # quadResult1, pcov1 = removeBackgroundOfFnType(parabola, arrays[0], sections, column=1)
  # quadResult2, pcov2 = removeBackgroundOfFnType(parabola, arrays[0], sections, column=2)

  # linearBackgroundReducedDoppler = np.array(arrays[0][100:729,1]) - np.array([linResult1(x) for x in arrays[0][100:729,0]])
  # linearBackgroundReducedDopplerFree = np.array(arrays[0][100:729,2]) - np.array([linResult1(x) for x in arrays[0][100:729,0]])
  
  # fn = lambda gain : sum((gain*linearBackgroundReducedDoppler-linearBackgroundReducedDopplerFree)**2)
  # linearBackgroundReducedDoppler = minimize(fn, x0=1).x[0]*linearBackgroundReducedDoppler

  # output = np.concatenate(
  #   (arrays[0][100:729,0:1],
  #   np.reshape(linearBackgroundReducedDopplerFree-linearBackgroundReducedDoppler, (-1,1))),
  #   axis=1
  # )
  # correction= lambda *args : GHZtoNM(getCorrection()(*args))
  # plt.plot(correction(output[:,0]), output[:,1],color='blue',linewidth=0.6)
  # plt.plot(correction(output[:,0]), linearBackgroundReducedDopplerFree, color='orange', label='Saturated Absorption')
  # plt.plot(correction(output[:,0]), linearBackgroundReducedDoppler, color='red', label='Doppler-Broadened')

  # plt.ylabel(r'Transmission')
  # plt.xlabel(r'Frequency (GHz)')
  # plt.title(r'Comparison of $Rb$ Spectra')
  # plt.ticklabel_format(useOffset=False)
  # plt.legend()
  # plt.autoscale()
  # plt.show()

  def fn(x, a1, b1, c1, a2, b2, c2, a3, b3, c3, a4, b4, c4, a5, b5, c5):
    return (
      a1*np.exp(-1/2*(x-b1)**2/c1**2)
    + a2*np.exp(-1/2*(x-b2)**2/c2**2)
    + a3*np.exp(-1/2*(x-b3)**2/c3**2)
    + a4*np.exp(-1/2*(x-b4)**2/c4**2)
    + a5*x**2+b5*x+c5
    )

  def curry(fn, *args):
    return lambda x: fn(x, *args)

  p0=[
      -0.08, 55.5, .3,
      -0.12, 57.7, .3,
      -0.05, 63, .5,
      -0.03, 67.5, .5,
      0, -0.05, 0.35
      ]
  
  # arrays[0][:,0] = GHZtoNM(arrays[0][:,0])


  # plt.plot(arrays[0][:,0], arrays[0][:,2]) 

  # plt.plot()
  
  p0 = curve_fit(fn, xdata=arrays[0][:,0], ydata=arrays[0][:,1], 
    p0=p0)[0]
  # print(p0)

  gainFn = lambda gain : sum((gain*curry(fn, *p0)(arrays[0][:,0])-arrays[0][:,2])**2)
  gainUpdated0 = lambda *args: minimize(gainFn, x0=1).x[0]*fn(*args)
  adtnlGain = 1.1
  gainUpdated1 = lambda *args: adtnlGain*gainUpdated0(*args)

  
  # plt.plot(arrays[0][:,0], curry(gainUpdated1, *p0)(arrays[0][:,0]), label='Background Fit')
  # plt.plot(arrays[0][:,0], arrays[0][:,2], label='Total Spectrum')

  # arrays[0][:,0] = getCorrection()(arrays[0][:,0])
  useable = 200
  freqDomain = arrays[0]
  baselineRemoved = ReLU(arrays[0][:,2]-curry(gainUpdated1, *p0)(arrays[0][:,0]), -0.0659)[useable:-1]
  # plt.plot(freqDomain, baselineRemoved)
  peakIndeces = find_peaks(baselineRemoved)[0]
  peakIndeces = [index + 200 for index in peakIndeces]
  
  
  # plt.plot(freqDomain[:,0][50:785], arrays[0][:,2][50:785], label='Saturated Absorption Spectrum')
  
  # plt.plot(freqDomain[:,0], arrays[0][:,2]-curry(gainUpdated1, *p0)(arrays[0][:,0]), label='Background Reduced')
  peaks = []
  for i in peakIndeces:    
    peak = [freqDomain[useable:-1,0][i-200], list(arrays[0][:,2]-curry(gainUpdated1, *p0)(arrays[0][:,0]))[i]]
    # plt.scatter(*peak)
    peaks.append(peak)
  
  peaks = np.array(peaks)
  
  F2CO13 = peaks[1,0]
  F2CO23 = peaks[0,0]

  conversion = getCorrection(F2CO13, 384_227.903_408_097)
  
  freqDomain = conversion(freqDomain)
  peaks = conversion(peaks)
  plt.xlabel(r"Frequency (GHz)")
  
  # freqDomain = GHZtoNM(freqDomain)
  # peaks= GHZtoNM(peaks)
  # plt.xlabel(r"Wavelength (nm)")

  plt.plot(freqDomain[150:750,0], arrays[0][150:750,2], label=r'Doppler Free $Rb$ Spectra', color=Colors.red)
  plt.scatter(peaks[:,0], [arrays[0][i,2] for i in peakIndeces], color=Colors.red)
  alpha = 'abcdefghijkl'

  [plt.text(peaks[i,0], arrays[0][peakIndeces[i],2], s=f'({alpha[i]})', ha='left' if i%2==1 else 'right') for i in range(len(peaks[:,0]))]

  print(f'F=2 CO13->CO23:  {(peaks[0,0]-peaks[1,0])} GHz')
  # print(freqDomain[:,0])
  
  deltaFreq = np.array([freqDomain[i,0] - freqDomain[i+1,0] for i in range(0,len(freqDomain[:,0])-1)])
  deltaFreq = np.average(deltaFreq)
  # print(f'{np.std(deltaFreq)=}')

  print(f'{(peaks[0,0]-peaks[1,0])/deltaFreq=}')

  print(f'{deltaFreq=} GHz')
  
  plt.grid(ls='--')
  plt.ticklabel_format(useOffset=False)
  plt.ylabel(r"Transmission")
  plt.title(r'Hyperfine $Rb$ Spectrum')
  plt.legend()
  plt.show()
