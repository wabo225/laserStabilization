from Bristol import Bristol

'''
Example code for using the Bristol class found here in the DAQ/wavemeter folder
'''

b = Bristol()

print("       All:", b.MeasAll())
print("Wavelength:", b.wavelength())
print(" Frequency:", b.frequency())

# These commands should be run alongside communication with the DLC