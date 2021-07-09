from os import write
import pyvisa
import time
import numpy as np
from datetime import date
import struct

def getXofPeak(oscilloscope):
    # Add the ability to convert this number into a usable number matching the wavemeter?
    curv = oscilloscope.query_binary_values("CURV?",'B') # unsigned char: C standard integer
    curv = np.array(curv)
    wavelength = curv.argmax()
    oscopeScalingFactor = (queryScale(oscilloscope)*1000)**-1
    return wavelength

def queryScale(oscilloscope):
    return oscilloscope.query('HOR:MAI:SCA?')



# Visa Connection Creation
rm = pyvisa.ResourceManager()
print(rm.list_resources())

oscilloscope = rm.open_resource(rm.list_resources()[0]) # The Oscilloscope may not always be the first entry, but it has been for our USB Driver

# Initialize CURV
oscilloscope.write("DAT INIT")
oscilloscope.write("DAT:SOU CH4")
oscilloscope.write("DAT:WID 1")
oscilloscope.write("DAT:ENC RPB") # set oscilloscope to send unsigned char 

print(oscilloscope.query("DAT?"))
# print(oscilloscope.query("WFMPre?"))

minutes = 15
timeBetween = .05 # > .1 min = 6 sec
time0 = time.time()
startingPixel = getXofPeak(oscilloscope)
file = open('data\DriftLockingData'+str(date.today())+'.csv','w')
for i in np.arange(0, minutes, timeBetween):
    x = getXofPeak(oscilloscope)
    out = str(round(time.time() - time0,3)) + ', ' + str(x) + '\n'
    print(out, end='')
    file.write(out)
    time.sleep(timeBetween*60)



file.close()
oscilloscope.close()

# a.tofile('data\DriftData'+str(date.today())+'.csv', sep=',')


