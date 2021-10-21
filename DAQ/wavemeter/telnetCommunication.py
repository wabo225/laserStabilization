from Bristol import Bristol
import numpy as np

'''
Example code for using the Bristol class found here in the DAQ/wavemeter folder

And debugging for 2021
'''

b = Bristol()

print("           All:", b.MeasAll())
print("    Wavelength:", b.wavelength())
print("     Frequency:", b.frequency())
print("     Intensity:", b.intensity(), sep='')

statusBin = [int(i) for i in "{:b}".format(int(b.MeasAll().split(',')[1]))]
statusBin = np.array(list(np.zeros(32-len(statusBin), int)) + statusBin)

print("Status Decoded:")
for i in range(31,0, -1):
    if statusBin[i] == 1:
        print("               ", np.arange(31, 0,-1)[i])

# b.write("SENSe:EXPosure:AUTO ON")
print("Auto Exposure Status:", b.query("SENSe:EXPosure:AUTO?"))




# These commands should be run alongside communication with the DLC