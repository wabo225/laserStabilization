import numpy as np
from os import listdir, path, stat
from datetime import date
from matplotlib import markers, pyplot as plt
from scipy import stats

'''
    This program was made to do customizable statistics on given files 
    formatted by driftMeasurement.py. That program takes data from an 
    oscilloscope, displaying a fabry-perot signal, and returns a csv 
    file with the amount of drift at each point in time. Since finding 
    an absolute frequency cannot be done, all frequencies are relative 
    to the frequency at the start of the trial.

    Here scipy is used to perform linear regression
'''


path_to_data = '../../Data/FrequencyDrift'
d = str(date.today())

print(*listdir(path_to_data), sep='\n')

def callback(file_name: str):
    return file_name.endswith('.csv') and file_name.find("23trial") != -1

csv_paths = list(filter(callback, listdir(path_to_data)))

for i in range(len(csv_paths)):
    print(csv_paths[i])
    with open(path_to_data+'/'+csv_paths[i], 'r') as f:
        # [print(f.readline(), end='') for j in range(4)]
        sweep = int(f.readline().split(',')[1])
        P = float(f.readline().split(',')[1])
        I = float(f.readline().split(',')[1])
        D = float(f.readline().split(',')[1])
        All = float(f.readline().split(',')[1])
        print(f'Sweep Expansion: {str(sweep)}')
        print(f'              P: {str(P)}')
        print(f'              I: {str(I)}')
        print(f'              D: {str(D)}')
        print(f'           Gain: {str(All)}\n')
        # print(f.readline())
        columns = f.readline().split(',')
        dat = np.genfromtxt(f,delimiter=',')
        dat = np.reshape(dat,(-1,len(columns)))
        print()
        # print(dat)
        time = dat[:,0]
        frequency_drift = dat[:,1]
        current = dat[:,2]

        regressOb = stats.linregress(time,frequency_drift)
        line = lambda x : regressOb[0]*x + regressOb[1]
        
        labels = ['No Locking', 'Top of Fringe Locking']
        plt.scatter(time, frequency_drift, marker='o', s=4, label=labels[i])
        plt.plot(time, line(time))

        pass

plt.grid(color='grey')
plt.xlabel('Time (s)')
plt.ylabel('Frequency Drift (GHz)')
plt.legend()
plt.show()