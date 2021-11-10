import pyvisa

class Laser:
    def __init__(self, resource_name) -> None:       
        rm = pyvisa.ResourceManager()
        self.inst = rm.open_resource(resource_name)
        print(self.inst.query("*IDN?"))
        # self.system.mcontrol(True)
    
    def initializeControllers(self):
        self.output = Output()
        self.sense = Sense()
        self.system = System()
        self.controls = Controls()
        self.queries = Queries()
    
    def query(self, command):
        return self.inst.query(command)

    def write(self, command):
        return self.inst.write(command)

    def OPC(self):
         ("*OPC?")

    def __del__(self):
        # self.system.mcontrol(False) # disables remote control
        self.inst.close()
        print("Communication to New Focus 6300 has been closed.")

class Output:
    def __init__(self) -> None:
       self._command = ":OUTPut"
       self.scan = Scan(self._command)

    def track(self):
        '''exit track mode to ready mode'''
        return (f'{self._command}:TRACK OFF')

    def laserOn(self, on: bool=None) -> bool:
        '''Turn laser on/off or read the state if no boolean argument is given'''
        if on is not None:
            return (f'{self._command} {"ON" if on else "OFF"}')
        else:
            return bool( (f'{self._command}?'))
class Scan:
    def __init__(self, command) -> None:
        self._command = command + ":SCAN"
    
    def reset(self):
        '''Stop and return to start wavelength'''
        return (self._command+":RESEt")

    def start(self):
        '''start/restart scan'''
        return (self._command+":STARt")

    def stop(self):
        '''Stop/Pause scan'''
        return (self._command+":STOP")
class Sense:
    def __init__(self) -> None:
        self._command = ":SENSe"
        self.temperature = Temperature(self._command)
    def current(self) -> float:
        '''read current level <value mA>'''
        return  (f'{self._command}:CURRent:DIODe?')
    def power(self) -> float:
        '''read front facet power <value mW>'''
        return  (f'{self._command}:POWER:FRONt?')
    def powerRear(self) -> float:
        '''read rear facet power <value proportional to power, arbitrary units> '''
        return  (f'{self._command}:POWER:REAR?')
    def piezo(self) -> float:
        '''read piezoelectric voltage <value 0-100%>'''
        return  (f'{self._command}:VOLTage:PIEZo?')
    def auxiliary(self) -> float:
        '''read user analog voltage <0-5V>'''
        return  (f'{self._command}:VOLTage:AUXiliary?')
    def wavelength(self) -> float:
        '''Read output wavelenghth <value nm>'''
        return  (f'{self._command}:WAVElength')
class Temperature:
    def __init__(self, command) -> None:
        self._command = command + ":TEMPerature"
    def diode(self):
         (f'{self._command}:DIODe')
    def diodeSetPoint(self):
         (f'{self._command}:SETPoint:DIODe')
    def cavity(self):
         (f'{self._command}:CAVity')
    def cavitySetPoint(self):
         (f'{self._command}:SETPoint:CAVity')
class System:
    def __init__(self) -> None:
       self._command = ":SYSTem"
    def winput(self, on: bool):
        '''Enables and disables wavelength input mode'''
        return (f'{self._command}:WINPut {"ON" if on else "OFF"}')
    def mcontrol(self, on):
        '''Enables and disables remote mode'''
        return (f'{self._command}:MCONtrol {"INT" if on else "EXT"}')
class Controls:
    def __init__(self) -> None:
       self.wavelength = Wavelength()
    def current(self, setpoint: float):
        '''write diode current set point'''
        return (f":CURRent {setpoint}")
    def temperature(self, setpoint: float):
        '''write diode temperature set point'''
        return (f":TEMPerature {setpoint}")
    def voltage(self, setpoint: float):
        '''write piezoelectric-voltage set point'''
        return (f":VOLTage {setpoint}")
class Wavelength:
    def wavelength(self, setpoint: float):
        '''write output wavelength set point'''
        return (f":WAVElength {setpoint}")
    def slewForward(self, setpoint: float):
        '''write forward slew-rate set point'''
        return (f":WAVElength:SLEWrate:FORWard {setpoint}")
    def slewReturn(self, setpoint: float):
        '''write return slew-rate set point'''
        return (f":WAVElength:SLEWrate:RETurn {setpoint}")
    def start(self, setpoint:float):
        '''write scan start-wavelength'''
        return (f":WAVElength:STARt {setpoint}")
    def stop(self, setpoint:float):
        '''write scan stop-wavelength'''
        return (f":WAVElength:STOP {setpoint}")

class Queries:
    def __init__(self) -> None:
        pass

if __name__ == "__main__":
    pyvisa.ResourceManager().list_resources()     
    l = Laser()
