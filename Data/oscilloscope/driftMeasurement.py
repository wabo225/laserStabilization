import pyvisa
import time
import numpy as np
from datetime import date
import sys
# from Tektronics.FPgetSweep import findSweep
from Tektronics import Oscilloscope as Osc

def main():
    # Visa Connection Creation
    rm = pyvisa.ResourceManager()
    resources = rm.list_resources()
    oscilloscope = rm.open_resource(rm.list_resources()[0]) # The Oscilloscope may not always be the first entry, but it has been for our USB Driver
    o = Osc.Oscilloscope(oscilloscope)

    # dlc = rm.open_resource(rm.list_resources()[2]) # Again. This will very likely be wrong if this code is run on any other computer.
    # Initialize CURV
    o.curvInit()

    # change these values 
    minutes = 10
    timeBetween = .2 # >= .1 min = 6 sec
    
    time0 = time.time()
    
    file = open('data\Drift' +str(date.today())+'.csv','w')  # filename

    expansion, voltsPerPixel, secondsPerPixel = Osc.findSweep(o)
    file.write("V/Pixel" + str(voltsPerPixel) + '\n')
    file.write("s/Pixel" + str(secondsPerPixel) + '\n')
    file.write("Sweep Expansion,"+ str(1) + '\n')
    
    for i in np.arange(0, minutes, timeBetween):
        x = np.argmax(o.CURV())
        # temp = paramRef(dlc, "'laser1:dl:tc:temp-act")
        out = str(round(time.time() - time0,3)) + ', ' + str(x) + '\n'
        print(out, end='')
        file.write(out)
        time.sleep(timeBetween*60)

    file.close()
    oscilloscope.close()
    # dlc.close()