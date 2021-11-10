from NewFocus.laserController import Laser

l = Laser("GPIB1::1::INSTR")
l.initializeControllers()

l.write(l.controls.wavelength.wavelength(780.24))
l.write(l.wavelength.slewForward(0.1))
l.write(l.wavelength.scan.start(780.1))
l.write(l.wavelength.scan.stop(780.4))

l.system.mcontrol(False)