import numpy as np
from matplotlib import pyplot as plt
from  toptica.lasersdk.dlcpro.v2_2_0 import DLCpro, SerialConnection
from toptica.lasersdk.utils.dlcpro import extract_float_arrays
import datetime
from os import listdir
import re
from globals import *


def getNextTrialNumber(pathToData: str):
    trials = filter(lambda filename : filename.find('trial') != -1, listdir(pathToData))
    indices = [int(re.search(r'.*trial(\d*)', trial).group(1)) for trial in trials]
    if len(indices) == 0:
        return 1
    return max(indices) + 1

def make_filename(experiment: str) -> str:
    '''
        defines the format of a filename
    '''
    d = datetime.date.today()
    return f'{experiment}{d.month}_{d.day}_{d.year}_trial{getNextTrialNumber(data_location)}'

def captureData(experiment = ''):
    if experiment!='': experiment+='_'

    with DLCpro(SerialConnection('COM9')) as dlc:
        # retrieve scan raw data from device
        '''
        collect data on frequency range or laser parameters
            temperature
            actual current
            actual piezo
            wavelength
            total power

            save that as meta data in the file
        '''
        header = f'''
               unit: {dlc.laser1.scope.channel1.unit.get()}
        temperature: {dlc.laser1.dl.tc.temp_act.get()} 
        act_current: {dlc.laser1.dl.cc.current_act.get()} 
        scan_offset: {dlc.laser1.scan.offset.get()}
           scan_amp: {dlc.laser1.scan.amplitude.get()}
        '''
#  wavelength: {dlc.laser1.dl.}
# total power: {dlc.laser1.dl.}
        
        print(header)
        dlc.laser1.scope.data.get()
        scanData = np.array(extract_float_arrays('xyY', dlc.laser1.scope.data.get())['y'])
        print(scanData)
        label = make_filename(experiment)
        np.savetxt(f'{data_location}\{label}.csv', scanData, delimiter=',')
        print(f'File saved as:     {label}.csv')
        print(f'           in:     {data_location}\\')

if __name__ == "__main__":
    experiment = input('Experiment Type')
    captureData(experiment)