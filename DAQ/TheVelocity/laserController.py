import pyvisa
from pyvisa.errors import Error

class Laser:
    def __init__(self, resource_name) -> None:       
        rm = pyvisa.ResourceManager()
        self.inst = rm.open_resource(resource_name)
        print(self.inst.query("*IDN?"))
        self.output = Output(self)
        self.sense = Sense(self)
        self.system = System(self)
        self.controls = Controls(self)
        self.queries = Queries(self)

    
    def OPC(self):
        self.inst.query("*OPC?")

    def __del__(self):
        self.system.mcontrol(False) # disables remote control
        self.inst.close()
        print("Communication to New Focus 6300 has been closed.")

class Output:
    _command = ":OUTPut"
    def __init__(self, laser_instance: Laser) -> None:
       self = laser_instance
       self.scan = Scan(laser_instance, self._command)

    def track(self):
        '''exit track mode to ready mode'''
        self.inst.write(f'{self._command}:TRACK OFF')

    def laserOn(self, on: bool=None) -> bool:
        '''Turn laser on/off or read the state if no boolean argument is given'''
        if on is not None:
            self.inst.write(f'{self._command} {"ON" if on else "OFF"}')
            return on 
        else:
            return bool(self.inst.query(f'{self.command}?'))
class Scan:
    def __init__(self, laser_instance: Laser, command) -> None:
        self = laser_instance
        self._command = command + ":SCAN"
    
    def reset(self):
        '''Stop and return to start wavelength'''
        self.inst.write(self._command+":RESEt")

    def start(self):
        '''start/restart scan'''
        self.inst.write(self._command+":STARt")

    def stop(self):
        '''Stop/Pause scan'''
        self.inst.write(self._command+":STOP")
class Sense:
    def __init__(self, laser_instance: Laser) -> None:
        self = laser_instance
        self._command = ":SENSe"
        self.temperature = Temperature(self._command)
    def current(self) -> float:
        '''read current level <value mA>'''
        return self.inst.query(f'{self._command}:CURRent:DIODe?')
    def power(self) -> float:
        '''read front facet power <value mW>'''
        return self.inst.query(f'{self.command}:POWER:FRONt?')
    def powerRear(self) -> float:
        '''read rear facet power <value proportional to power, arbitrary units> '''
        return self.inst.query(f'{self.command}:POWER:REAR?')
    def piezo(self) -> float:
        '''read piezoelectric voltage <value 0-100%>'''
        return self.inst.query(f'{self._command}:VOLTage:PIEZo?')
    def auxiliary(self) -> float:
        '''read user analog voltage <0-5V>'''
        return self.inst.query(f'{self._command}:VOLTage:AUXiliary?')
    def wavelength(self) -> float:
        '''Read output wavelenghth <value nm>'''
        return self.inst.query(f'{self._command}:WAVElength')
class Temperature:
    def __init__(self, laser_instance: Laser, command) -> None:
        self = laser_instance
        self._command = command + "TEMPerature"
    def diode(self):
        self.inst.query(f'{self.command}:DIODe')
    def diodeSetPoint(self):
        self.inst.query(f'{self.command}:SETPoint:DIODe')
    def cavity(self):
        self.inst.query(f'{self.command}:CAVity')
    def cavitySetPoint(self):
        self.inst.query(f'{self.command}:SETPoint:CAVity')
class System:
    def __init__(self, laser_instance: Laser) -> None:
       self = laser_instance
       self._command = ":SYSTem"
    def winput(self, on: bool):
        '''Enables and disables wavelength input mode'''
        self.inst.write(f'{self._command}:WINPut {"ON" if on else "OFF"}')
    def mcontrol(self, on):
        '''Enables and disables remote mode'''
        self.inst.write(f'{self._command}:MCONtrol {"INT" if on else "EXT"}')
class Controls:
    def __init__(self, laser_instance: Laser) -> None:
       self = laser_instance
       self.wavelength = Wavelength(self)
    def current(self, setpoint: float):
        '''write diode current set point'''
        self.inst.write(f":CURRent {setpoint}")
    def temperature(self, setpoint: float):
        '''write diode temperature set point'''
        self.inst.write(f":TEMPerature {setpoint}")
    def voltage(self, setpoint: float):
        '''write piezoelectric-voltage set point'''
        self.inst.write(f":VOLTage {setpoint}")
class Wavelength:
    def __init__(self, laser_instance: Laser) -> None:
       self = laser_instance
    def wavelength(self, setpoint: float):
        '''write output wavelength set point'''
        self.inst.write(f":WAVElength {setpoint}")
    def slewForward(self, setpoint: float):
        '''write forward slew-rate set point'''
        self.inst.write(f":WAVElength:SLEWrate:FORWard {setpoint}")
    def slewReturn(self, setpoint: float):
        '''write return slew-rate set point'''
        self.inst.write(f":WAVElength:SLEWrate:RETurn {setpoint}")
    def start(self, setpoint:float):
        '''write scan start-wavelength'''
        self.inst.write(f":WAVElength:STARt {setpoint}")
    def stop(self, setpoint:float):
        '''write scan stop-wavelength'''
        self.inst.write(f":WAVElength:STOP {setpoint}")
class Queries:
    def __init__(self) -> None:
        pass

if __name__ == "__main__":
    pyvisa.ResourceManager().list_resources()     
