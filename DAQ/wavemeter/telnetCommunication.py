from Bristol import Bristol
import numpy as np

'''
Example code for using the Bristol class found here in the DAQ/wavemeter folder

And debugging for 2021
'''

b = Bristol()

print(" Auto Exposure:", b.query(":SENSe:EXP:AUTO?"))
b.write(":SENS:EXP:AUTO ON")

# print("           All:", b.MeasAll())
print("    Wavelength:", b.wavelength())
print("     Frequency:", b.frequency())
print("     Intensity:", b.intensity(), sep='')

# b.write("SENSe:EXPosure:AUTO ON")
# print("Auto Exposure Status:", b.query("SENSe:EXPosure:AUTO?"))

print(b.getConstants())

# These commands should be run alongside communication with the DLC