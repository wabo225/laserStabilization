from os import write
import pyvisa
import time
import numpy as np
from datetime import date
import struct

#Oscilloscope Scale
xDivsPerScreen = 10
wavPerXPix = lambda o : float(o.HorizontalParams("SCA"))/float(o.HorizontalParams("RECO"))*xDivsPerScreen

def getXofPeak(oscilloscope):
    # Add the ability to convert this number into a usable number matching the wavemeter?
    curv = oscilloscope.query_binary_values("CURV?",'B') # unsigned char: C standard integer
    curv = np.array(curv)
    xpix = curv.argmax()
    # oscopeScreenScale = queryScale(oscilloscope)/2500 #timeperpixel
    
    return xpix


def paramRef(dlc, command):
    dlc.write("(param-ref " + command + ")")
    return dlc.read().strip()


# Visa Connection Creation
rm = pyvisa.ResourceManager()
# print(rm.list_resources())
resources = rm.list_resources()
oscilloscope = rm.open_resource(rm.list_resources()[0]) # The Oscilloscope may not always be the first entry, but it has been for our USB Driver
dlc = rm.open_resource(rm.list_resources()[2]) # Again. This will very likely be wrong if this code is run on any other computer.

# Initialize CURV
oscilloscope.write("DAT INIT")
oscilloscope.write("DAT:SOU CH4")
oscilloscope.write("DAT:WID 1")
oscilloscope.write("DAT:ENC RPB") # set oscilloscope to send unsigned char 

print(oscilloscope.query("DAT?"))
# print(oscilloscope.query("WFMPre?"))

# change these values 
minutes = 15
timeBetween = .15 # >= .1 min = 6 sec
time0 = time.time()
startingPixel = getXofPeak(oscilloscope)
file = open('data\DriftLockingDataPID1'+str(date.today())+'.csv','w')  # filename
for i in np.arange(0, minutes, timeBetween):
    x = getXofPeak(oscilloscope)
    temp = paramRef(dlc, "'laser1:dl:tc:temp-act")
    out = str(round(time.time() - time0,3)) + ', ' + str(x) + ', ' + temp + '\n'
    print(out, end='')
    file.write(out)
    time.sleep(timeBetween*60)

file.close()
oscilloscope.close()

# a.tofile('data\DriftData'+str(date.today())+'.csv', sep=',')