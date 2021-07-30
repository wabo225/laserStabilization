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

with DLCpro(SerialConnection('COM4')) as d:
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
        d.laser1.dl.cc.current_set.set(128+i*0.01)
        
        # update data stores. 
        tstart.append(time()-start)
        x.append(d.laser1.dl.cc.current_act.get())
        y.append(b.frequency())
        tend.append(time()-start)  # tstart and tend can be used for horizontal error bars, accounting for time difference between measurements and communications
        
        # Uncomment for scatterplot
        # plt.scatter(tend[-1],y[-1],color="wheat", marker='x')

        # Uncomment for line plot
        plt.plot(tend,y,color="wheat")

        plt.autoscale()
        plt.pause(0.03)

        isLocked = d.laser1.dl.lock.lock_enabled.get()
        # d.laser1.dl.cc.current_set.set(128)


a = np.array([tstart, tend,x,y]).transpose()
np.savetxt(f'{pathToData}/trial{getNextTrialNumber(pathToData)}{description}.csv', a, delimiter=',')