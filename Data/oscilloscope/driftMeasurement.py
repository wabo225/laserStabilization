from numpy.lib.shape_base import expand_dims
import pyvisa
import time
import numpy as np
from datetime import date
from Tektronics import Oscilloscope as Osc
from toptica.lasersdk.dlcpro.v1_9_0 import DLCpro, SerialConnection
# import asyncio

def delta_frequency(delta_pixels, scale, expansion):
    expansions = {'1':467.2578713474481, '2':236.221920452312, '5':95.57796824314684}
    pixelsPerDivision = 250
    return expansions[str(expansion)]*float(delta_pixels)*float(scale)/pixelsPerDivision

def main():
    # Visa Connection Creation
    rm = pyvisa.ResourceManager()
    # resources = rm.list_resources()
    oscilloscope = rm.open_resource(rm.list_resources()[0]) # The Oscilloscope may not always be the first entry, but it has been for our USB Driver
    o = Osc.Oscilloscope(oscilloscope)

    file = open('data\FrequencyDrift' +str(date.today())+'trial6.csv','w')  # filename

    expansion = Osc.findSweep(o)
    scale = o.HorizontalParams(Osc.HorizontalOptions.SCA)
    file.write("Sweep Expansion, "+ str(expansion) + '\n')
    print("Sweep Expansion, "+ str(expansion))
    # file.write("Set Current, "+sys.argv[1]+'\n')
    # print("Set Current, "+sys.argv[1]+'\n')
    # file.write("Power (mW), "+sys.argv[1]+'\n')
    # print("Power (mW), "+sys.argv[1]+'\n')

    # change these values 
    duration = 45 # minutes
    timeBetween = .25 # >= .1 min = 6 sec
    
    o.setChannel(4) # set channel for curv
    o.curvInit()
    o.write("ACQ:MOD AVE")
    o.write("ACQ:NUMAV 128")

    time0 = time.time()
    x_init = np.argmax(o.CURV())
    with DLCpro(SerialConnection('COM4')) as dlc:
        file.write('P,'+ str(dlc.laser1.dl.lock.pid2.gain.p.get())+'\n')
        file.write('I,'+ str(dlc.laser1.dl.lock.pid2.gain.i.get())+'\n')
        file.write('D,'+ str(dlc.laser1.dl.lock.pid2.gain.d.get())+'\n')
        file.write('All,'+ str(dlc.laser1.dl.lock.pid2.gain.all.get())+'\n')
        file.write('t (s), Frequency Drift (GHz), Active Current (mA), Piezo Voltage \n')
        for i in np.arange(0, duration, timeBetween):
            delta_pixels = np.argmax(o.CURV()) - x_init
            dnu = delta_frequency(delta_pixels, scale, expansion)
            act_curr = dlc.laser1.dl.cc.current_act.get()
            piez_curr = dlc.laser1.dl.pc.voltage_act.get()
            out = str(round(time.time() - time0,3)) + ', ' + str(dnu) + ', ' + str(act_curr) + ', ' + str(piez_curr) + '\n'
            print(out, end='')
            file.write(out)
            time.sleep(timeBetween*60)

    file.close()
    oscilloscope.close()

if __name__ == '__main__':
    main()