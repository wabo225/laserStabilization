import pyvisa
import time
import numpy as np
from datetime import date
import struct

def wavelengthPerPixel(oscilloscope):
    # distance between FP peaks two peaks must be on either side of split
    curv = oscilloscope.query_binary_values("CURV?",'B')
    curv = np.array(curv)
    splitCurve= np.split(curv,20)
    left= np.argmax(splitCurve[0])
    right= np.argmax(splitCurve[1])
    
    return 3.045*10**-12/(1250-left + right)

def queryScale(oscilloscope):
    return float(oscilloscope.query('HOR:MAI:SCA?'))

def timePerPixel(oscilloscope):
    return  queryScale(oscilloscope)/2500

def wavelengthPerSecond(oscilloscope):
    return wavelengthPerPixel(oscilloscope)/timePerPixel(oscilloscope)



# Visa Connection Creation
rm = pyvisa.ResourceManager()
print(rm.list_resources())

oscilloscope = rm.open_resource(rm.list_resources()[0]) # The Oscilloscope may not always be the first entry, but it has been for our USB Driver

# Initialize CURV
oscilloscope.write("DAT INIT")
oscilloscope.write("DAT:SOU CH4")
oscilloscope.write("DAT:WID 1")
oscilloscope.write("DAT:ENC RPB")

print(oscilloscope.query("DAT?"))


a=[]
for i in range(0,20):
    a.append(wavelengthPerPixel(oscilloscope)/timePerPixel(oscilloscope))
    time.sleep(1)
a=np.array(a)
print("mean:", np.mean(a))
print("std :", np.std(a))
oscilloscope.close() 

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