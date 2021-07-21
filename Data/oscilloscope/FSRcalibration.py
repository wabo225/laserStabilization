import pyvisa
import numpy as np
from datetime import date
import time

from Tektronics import Oscilloscope as Osc
divsPerScreen = 10
fsr=1.5E9 # Hz

secondsPerPixel = lambda o : float(o.HorizontalParams(Osc.HorizontalOptions.SCA))/float(o.HorizontalParams(Osc.HorizontalOptions.RECO))*divsPerScreen

def wavelengthPerSecond(o):
    # distance between FP peaks two peaks must be on either side of split
    o.setChannel(3)
    o.curvInit()
    curv = o.CURV()
    splitCurve= np.split(curv,2)
    left= np.argmax(splitCurve[0])
    right= np.argmax(splitCurve[1])
    wavPerPix= 3.045*10**-12/(1250-left + right) # most likely wrong wavlength conversion
    timeScale=secondsPerPixel(o)
    return wavPerPix/timeScale

def frequencyPerSecond(o: Osc.Oscilloscope):
    # distance between FP peaks two peaks must be on either side of split
    o.setChannel(4)
    o.curvInit()
    curv = o.CURV()
    splitCurve= np.split(np.array(curv),2)
    left= np.argmax(splitCurve[0])
    right= np.argmax(splitCurve[1])
    freqPerPix= fsr/(1250-left + right)
    timeScale=secondsPerPixel(o)
    return freqPerPix/timeScale

# Visa Connection Creation
rm = pyvisa.ResourceManager()
print(rm.list_resources())
o = Osc.Oscilloscope(rm.open_resource(rm.list_resources()[0])) # The Oscilloscope may not always be the first entry, but it has been for our USB Driver
# print("Seconds per Pixel: " + secondsPerPixel)

# def wavPerSecTest(o):
#     file = open('data\sweepExpansionScale'+str(date.today())+'.csv','w')

a=[]
for i in range(0,20):
    a.append(frequencyPerSecond(o))
    time.sleep(1)
a=np.array(a)
print("mean:", np.mean(a)*10**-9 , 'GHz')
print("std :", np.std(a)*10**-9 , 'GHz')
 

# a.tofile('data\DriftData'+str(date.today())+'.csv', sep=',')

""" Trials of Wavelength per Pixel

Sweep Expansion 1x
TimeScale: 500 us
mean: 2.45155788599e-15 m/pix
std : 9.17315695996e-17  

Sweep expansion 2x
Time Scale 1.0 ms
mean: 2.43321901137e-15 m/pix
std : 8.35195824369e-17

Sweep Expansion 5x
Time Scale: 2.50ms
mean: 2.43156993271e-15 m/pix
std : 9.56261336715e-17


Wavelength Per Second 

Sweep Expansion 5x
Time Scale: 2.50 ms
mean: 2.40859781236e-09 m/s
std : 7.21063275215e-11

Sweep Expansion 1x
Time Scale: 0.5ms
mean: 1.21545088822e-08 m/s
std : 3.95912244864e-10

"""