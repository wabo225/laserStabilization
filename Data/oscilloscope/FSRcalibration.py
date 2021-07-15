from numpy.lib.shape_base import expand_dims
import pyvisa
import time
import numpy as np
from datetime import date
import struct
from matplotlib import pyplot as plt

from Tektronics import Oscilloscope as Osc
divsPerScreen = 10

def wavelengthPerPixel(oscilloscope):
    # distance between FP peaks two peaks must be on either side of split
    curv = oscilloscope.query_binary_values("CURV?",'B')
    curv = np.array(curv)
    splitCurve= np.split(curv,20)
    left= np.argmax(splitCurve[0])
    right= np.argmax(splitCurve[1])
    
    return 3.045*10**-12/(1250-left + right)

# Visa Connection Creation
rm = pyvisa.ResourceManager()
print(rm.list_resources())
o = Osc.Oscilloscope(rm.open_resource(rm.list_resources()[0])) # The Oscilloscope may not always be the first entry, but it has been for our USB Driver


# Sweep Expansion
def findSweep(o):
    o.setChannel(3)
    o.curvInit()
    o.CURV()
    voltsPerPix= float(o.VerticalParams("SCA"))*8/255
    secondsPerPix=float(o.HorizontalParams("SCA"))/float(o.HorizontalParams(Osc.HorOptions.RECO))*divsPerScreen
    
    #Slope in Pix
    sweepCurv = o.CURV()
    sweepCurv = [sum(sweepCurv[0+10*i:10+10*i])/10 for i in range(len(sweepCurv)//10)]

    slopeSweep = np.gradient(sweepCurv)/10
    slopeSweep= slopeSweep[slopeSweep>0]
    sweepAvg=np.mean(slopeSweep)
    #slope in Volts per Second
    sweepAvg=sweepAvg*voltsPerPix/secondsPerPix
    
    return sweepAvg

sweep=findSweep(o)
# o.print("VOLTS per SECOND", sweep)
# o.print("SECONDS per 15V sweep", 15/sweep)
expansions = [1,2,5,10,20,50,100]
o.print("hScale", float(o.HorizontalParams("SCA")))
print(0.01*np.array(expansions)-np.array([15/sweep for i in range(len(expansions))]) )
o.print("SweepExpansion", 
    expansions[np.argmin(np.abs( # index of minimum value of absolute value of difference in risetime options and calculated risetime
        0.01*np.array(expansions)-np.array([15/sweep for i in range(len(expansions))]) 
    )
)])

"""a=[]
for i in range(0,20):
    a.append(wavelengthPerPixel(oscilloscope)/timePerPixel(oscilloscope))
    time.sleep(1)
a=np.array(a)
print("mean:", np.mean(a))
print("std :", np.std(a))"""
 

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