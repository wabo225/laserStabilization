from NewFocus.laserController import Laser, Sense

l = Laser("GPIB1::1::INSTR")
l.initializeControllers()

l.write(l.controls.wavelength.wavelength(778.24))


# l.system.mcontrol(False)