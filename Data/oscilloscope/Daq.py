from Tektronics.Oscilloscope import Oscilloscope
from Tektronics import *
import pyvisa
from toptica.lasersdk.dlcpro.v1_9_0 import DLCpro, NetworkConnection

with DLCpro(NetworkConnection('')) as dlc:

rm = pyvisa.ResourceManager()

rm = pyvisa.ResourceManager()
oscilloscope = rm.open_resource(rm.list_resources()[0]) # The Oscilloscope may not always be the first entry, but it has been for our USB Driver
o = Oscilloscope(oscilloscope)
o.Horizontal.POS.get()