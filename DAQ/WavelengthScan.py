from NewFocus.laserController import Laser, Sense
from NewFocus.laserController import Wavelength, Scan

l = Laser("GPIB1::1::INSTR")
l.initializeControllers()

w = Wavelength

l.write(l.controls.wavelength.wavelength(780.24))
w.write(w.Wavelength.slewForward(0.1))
w.write(w.Wavelength.scan.start(780.1))
w.write(w.Wavelength.scan.stop(78.4))


# l.system.mcontrol(False)