from NewFocus import laserController
import numpy as np

l = laserController.Laser("GPIB1::1::INSTR")
l.initializeControllers()
# l.write(l.controls.voltage(50))
print()
print("   Current:", l.query(l.sense.current()))
print("     Power:", l.query(l.sense.power()))
print("Wavelength:", l.query(l.sense.wavelength()))
# print("Piezo Scan-")
print("     Piezo:", l.query(l.sense.piezo()))
# print("     Amplitude:", str(1), "Vpp")
# print("     Frequency:", str(1), "Hz")
# print("     Fn Offset:", str(50.0), 'mV')
print()

l.write(l.system.mcontrol(False))