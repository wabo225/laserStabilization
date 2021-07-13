import pythonControl.functions as laserVisa

import pyvisa
rm = pyvisa.ResourceManager()
dlc = rm.open_resource(rm.list_resources()[2])

laserVisa.paramDisp(dlc, "'laser1")

dlc.close()