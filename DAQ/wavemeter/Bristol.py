from telnetlib import Telnet
import numpy as np

class Bristol:
    def __init__(self, ip_addr = '10.199.199.1', quiet=False):
        self.dev_addr = ip_addr
        self.wave = Telnet(ip_addr, 23)
        print()
        # [print(self.readline(), end='\n') for i in range(8)]
        [self.readline() for i in range(8)] # flushes the telnet header 
        if not quiet:
            self.wave.write(b'*IDN?\r\n') # Perform a test communication
            print(self.readline(),'\n') # and read the result to the terminal

    class EmptyBuffer(Exception):
        ''' A User defined error message for when you tried to read from an empty telnet buffer'''
        def __init__(self, message="Telnet buffer was empty, and the read command timed out after 3 seconds.") -> None:
            self.message = message
            super().__init__(self.message)
        pass

    def readline(self):
        response = self.wave.read_until(b'\n', timeout=3).decode('utf-8')
        if response == '':
            raise self.EmptyBuffer
            self.__del__(self)
        return response.strip()

    def autoExposure(self, value):
        if value == 'ON' or value == 'off':
            self.write(f':SENS:EXP:AUTO {value}')
        return self.query(':SENS:EXP:AUTO?')

    def MeasAll(self):
        '''
        This function took a maximum of 0.009097 seconds

            a = []
            for i in range(0,100):
                start = timer()
                MeasAll(bristol)
                end = timer()
                a.append(end-start)
            a = np.array(a)
            print(a.mean())
            print(a.max())
        
        '''
        self.wave.write(b':MEAS:ALL?\r\n')
        return self.readline()

    def getConstants(self):
        Kd = self.query(":SENSe:PID:LCONstants:DERivative?")
        Ki = self.query(":SENSe:PID:LCONstants:INTegral?")
        Kp = self.query(":SENSe:PID:LCONstants:PROPortional?")
        return Kd, Ki, Kp

    def setconstants(self, Kd, Ki, Kp):
        self.write(":SENSe:PID:LCONstants:DERivative " + str(Kd) + "\r\n")
        self.write(":SENSe:PID:LCONstants:INTegral " + str(Ki) + "\r\n")
        self.write(":SENSe:PID:LCONstants:PROPortional " + str(Kp) + "\r\n")
    
    def checkFunctionality(self):
        return self.query(":SENSe:PID:FUNCtion?")
    
    def setPointPID(self, setPoint: float = ''):
        if type(setPoint) == float:
            self.write(f':SENSe:PID:SPOint {setPoint}')
        return self.query(':SENSe:PID:SPOint?')
        

    def write(self, message: str) -> None:
        self.wave.write(f'{message}\r\n'.encode('utf-8'))

    def query(self, message: str) -> str:
        ''' 
        @param message: str  Required. Can be these and more, found in the Bristol Manual under ~/Resources/Manuals/Bristol.pdf
            *IDN?
            :MEAS:WAV?
            :MEAS:ALL?
        
        These should all end in '?'
        '''
        self.wave.write(f'{message}\r\n'.encode('utf-8'))
        return self.readline()

    def wavelength(self):
        '''
        This function returns the wavelength read by the wavemeter
        '''
        return float(self.query(":MEAS:WAV?").strip())
    
    def frequency(self):
        '''
        This function returns the frequency read by the wavemeter
        '''
        return float(self.query(":MEAS:FREQ?").strip())

    def intensity(self):
        return self.MeasAll().split(',')[3]

    def __del__(self):
        self.wave.close()
        print(f'\nConnection to {self.dev_addr} closed.')

    def displayStatus(self):
        statusBin = [int(i) for i in "{:b}".format(int(self.MeasAll().split(',')[1]))]
        statusBin = np.array(list(np.zeros(32-len(statusBin), int)) + statusBin)

        print("Status Decoded:")
        for i in range(31,0, -1):
            if statusBin[i] == 1:
                print("               ", np.arange(31, 0,-1)[i])
if __name__ == "__main__":
    Bristol()