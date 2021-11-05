from wavemeter.Bristol import Bristol
from toptica.lasersdk.dlcpro.v1_9_0 import DLCpro, SerialConnection
import numpy as np
from matplotlib import pyplot as plt
from time import time
import re
from os import listdir

duration = 100
pathToData = '../Data/wavemeter'
description = 'testRun'

def getNextTrialNumber(pathToData: str):
    trials = filter(lambda filename : filename.find('trial') != -1, listdir(pathToData))
    indices = [int(re.search(r'.*trial(\d*)', trial).group(1)) for trial in trials]
    if len(indices) == 0:
        return 1
    return max(indices) + 1

with DLCpro(SerialConnection('COM9')) as d:
    b = Bristol()
    x = []
    tend = []
    tstart = []
    y = []
    start = time()
    ax = plt.gca()
    ax.set_facecolor('dimgray')
    for i in range(duration):
        # set current based on function of index of sample loop
        # d.laser1.dl.pc.voltage_set.set(38+i*0.16)
        
        # update data stores. 
        tstart.append(time()-start)
        x.append(b.frequency())
        
        # d.io.fine_2.value_act
        y.append(d.io.fine_1.value_act.get())
        tend.append(time()-start)  # tstart and tend can be used for horizontal error bars, accounting for time difference between measurements and communications
        
        # Uncomment for scatterplot
        # plt.scatter(tend[-1],y[-1],color="wheat", marker='x')

        # Uncomment for line plot
        plt.plot(x,y,color="wheat")

        plt.autoscale()
        plt.pause(0.04)

        # isLocked = d.laser1.dl.lock.lock_enabled.get()
        # d.laser1.dl.cc.current_set.set(128)


a = np.array([tstart, tend,x,y]).transpose()
np.savetxt(f'{pathToData}/trial{getNextTrialNumber(pathToData)}{description}.csv', a, delimiter=',')