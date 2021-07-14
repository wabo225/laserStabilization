from matplotlib import pyplot as plt
import numpy as np
from scipy.signal import sawtooth
from scipy.stats import linregress as linFit
#bell = lambda t, mu=0, sigma=1, squish=1 : squish*np.exp(-0.5*(t-mu)**2/sigma**2)
"""
sawto = lambda x, width=1, phase=0, dcOffset=0 : 0.5*(sawtooth(2*np.pi*x + phase, width)+1) + dcOffset
sawtoothBasis = lambda x, phase=0, dcOffset=0 : (x-1 + phase/(2*np.pi)) + dcOffset
sawtoInv = lambda y, phase=0, dcOffset=0 : y+1-phase/(2*np.pi) - dcOffset
t = np.arange(0,2,0.01)
saw = 2*sawto(t, width=1, phase=np.pi)
x=np.gradient(saw,t)
slopeSort= x[x >= 0]
wavelengths = np.arange(0.2,1,0.4)
# print(wavelengths)
plt.plot(np.round(slopeSort,3))
plt.title("Fabry Perot Output Example")
plt.xlabel("Time")
plt.ylabel("Voltage")
plt.show() """
testList=[*range(1,20,2)]
#testFn=linFit(testList)
testSlope= np.gradient(testList)
print(testSlope)
