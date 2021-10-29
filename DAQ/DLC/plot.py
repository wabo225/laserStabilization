import numpy as np
from  toptica.lasersdk.dlcpro.v2_2_0 import DLCpro, SerialConnection
from toptica.lasersdk.utils.dlcpro import extract_float_arrays

with DLCpro(SerialConnection('COM9')) as dlc:
    dlc.laser1.scan.offset.get()
    dlc.laser1.scan.amplitude.get()
    
