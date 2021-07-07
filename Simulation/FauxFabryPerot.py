from matplotlib import pyplot as plt
import numpy as np
from scipy.signal import sawtooth


bell = lambda t, mu=0, sigma=1, squish=1 : squish*np.exp(-0.5*(t-mu)**2/sigma**2)

sawto = lambda x, width=1, phase=0, dcOffset=0 : 0.5*(sawtooth(2*np.pi*x + phase, width)+1) + dcOffset
sawtoothBasis = lambda x, phase=0, dcOffset=0 : (x-1 + phase/(2*np.pi)) + dcOffset
sawtoInv = lambda y, phase=0, dcOffset=0 : y+1-phase/(2*np.pi) - dcOffset
t = np.arange(0,2,0.01)

wavelengths = np.arange(0.2,1,0.4)
# print(wavelengths)
mus = list(sawtoInv(wavelengths, phase=np.pi))
mus = mus + list(sawtoInv(wavelengths, phase=np.pi)-np.ones(2)) + list(sawtoInv(wavelengths, phase=np.pi) + np.ones(2))

interferometer = lambda x, mus : sum([bell(x, mu=mu, sigma=0.05, squish=0.8) for mu in mus])

np.array(sawto(t,width=1, phase=np.pi))
plt.plot(t, sawto(t, width=1, phase=np.pi), t, interferometer(t,mus))
plt.title("Faux Fabry Perot")
plt.xlabel("Time")
plt.ylabel("Voltage")
plt.show()