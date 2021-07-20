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
    
    file = open('data\Drift' +str(date.today())+'.csv','w')  # filename

    expansion = Osc.findSweep(o)
    scale = o.HorizontalParams(Osc.HorizontalOptions.SCA)
    file.write("Sweep Expansion, "+ str(expansion) + '\n')
    print("Sweep Expansion, "+ str(expansion))
    file.write('t (s), Pixel\n')

    # change these values 
    duration = 1 # minutes
    timeBetween = .2 # >= .1 min = 6 sec
    
    o.setChannel(4) # set channel for curv
    o.curvInit()
    o.write("ACQ:MOD AVE")
    o.write("ACQ:NUMAV 128")
    
    delta_wavelength = lambda delta_pixels, scale, expansion : 1.215E-8/250 * (delta_pixels * scale)/expansion

    time0 = time.time()
    x_init = np.argmax(o.CURV())
    for i in np.arange(0, duration, timeBetween):
        delta_pixels = np.argmax(o.CURV()) - x_init
        dlambda = delta_wavelength(delta_pixels, scale, expansion)
        # temp = paramRef(dlc, "'laser1:dl:tc:temp-act")
        out = str(round(time.time() - time0,3)) + ', ' + str(x) + '\n'
        print(out, end='')
        file.write(out)
        time.sleep(timeBetween*60)

    file.close()
    oscilloscope.close()
    # dlc.close()

if __name__ == '__main__':
    main()