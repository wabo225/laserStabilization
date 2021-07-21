import numpy as np
from matplotlib import pyplot as plt
from  toptica.lasersdk.dlcpro.v2_2_0 import DLCpro, SerialConnection
from toptica.lasersdk.utils.dlcpro import extract_float_arrays

def main():
    with DLCpro(SerialConnection('COM4')) as dlc:
        # retrieve scan raw data from device
        scanData = np.array(extract_float_arrays('xyY', dlc.laser1.scope.data.get())['y'])
        
        '''
        the fourier transform of the xy plots.
        when y is the voltage output of the 
        '''
        # plt.plot(np.abs(np.fft.fft(scanData)[1:1000]))
        # plt.show()
        return np.max(np.abs(np.fft.fft(scanData)[1:1000])[20:50])
        
        
        
if __name__ == '__main__':
    print(f'Maximum height of {main()}')
