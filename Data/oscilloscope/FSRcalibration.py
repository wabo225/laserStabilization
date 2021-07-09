from os import write
import pyvisa
import time
import numpy as np
from datetime import date
import struct

def wavelengthPerPixel(oscilloscope):
    # distance between FP peaks two peaks must be on either side of split
    curv = oscilloscope.query_binary_values("CURV?",'B')
    curv = np.array(curv)
    splitCurve= np.split(curv,20)
    left= np.argmax(splitCurve[0])
    right= np.argmax(splitCurve[1])
    return 3.045*10**-12/(1250-left + right)

# Visa Connection Creation
rm = pyvisa.ResourceManager()
print(rm.list_resources())

oscilloscope = rm.open_resource(rm.list_resources()[0]) # The Oscilloscope may not always be the first entry, but it has been for our USB Driver

# Initialize CURV
oscilloscope.write("DAT INIT")
oscilloscope.write("DAT:SOU CH4")
oscilloscope.write("DAT:WID 1")
oscilloscope.write("DAT:ENC RPB")

print(oscilloscope.query("DAT?"))
# print(oscilloscope.query("WFMPre?"))

oscilloscope.close()

# a.tofile('data\DriftData'+str(date.today())+'.csv', sep=',')


