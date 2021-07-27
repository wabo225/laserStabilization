from os import write
import pyvisa
import time
import numpy as np
from datetime import date
import struct

#Oscilloscope Scale
xDivsPerScreen = 10
wavPerXPix = lambda o : float(o.HorizontalParams("SCA"))/float(o.HorizontalParams("RECO"))*xDivsPerScreen


def paramRef(dlc, command):
    dlc.write("(param-ref " + command + ")")
    return dlc.read().strip()


# Visa Connection Creation
rm = pyvisa.ResourceManager()
# print(rm.list_resources())
resources = rm.list_resources()
oscilloscope = rm.open_resource(rm.list_resources()[0]) # The Oscilloscope may not always be the first entry, but it has been for our USB Driver
dlc = rm.open_resource(rm.list_resources()[2]) # Again. This will very likely be wrong if this code is run on any other computer.

# Initialize CURV
oscilloscope.write("DAT INIT")
oscilloscope.write("DAT:SOU CH4")
oscilloscope.write("DAT:WID 2")
oscilloscope.write("DAT:ENC RPB") # set oscilloscope to send unsigned char 

print(oscilloscope.query("DAT?"))
# print(oscilloscope.query("WFMPre?"))

print()

file.close()
oscilloscope.close()
dlc.close()
