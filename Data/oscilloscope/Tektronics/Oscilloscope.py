# from Channel import Channel
import os
from enum import Enum, auto
from typing import List, Tuple
from dataclasses import dataclass
import numpy as np
# from Channel import Channel

os.system('color')

class AcquisitionOptions: 
    MOD = auto()
    NUMAC = auto()
    NUMAV = auto()
    STATE = auto()
    STOPA = auto()

@dataclass
class Acquisition:
    Options: AcquisitionOptions
    MOD: str
    NUMAC: int
    NUMAV: int
    STATE: int
    STOPA: int

class HorizontalOptions(Enum):
    VIEW = auto()
    RECO = auto()
    POS = auto()
    SCA = auto()
    DEL = auto()

@dataclass
class Horizontal:
    HorizontalOptions = HorizontalOptions
    VIEW: str  = None
    RECO: int  = None
    POS: float = None
    SCA: float = None

class VerticalOptions(Enum):
    BAN = auto()
    COUP = auto()
    CURRENTPRO = auto()
    INV = auto()
    POS = auto()
    PRO = auto()
    SCA = auto()
    YUN = auto()

@dataclass
class Vertical:
    VerticalOptions: VerticalOptions
    COUP: str
    CURRENTPRO: float
    INV: float
    POS: float
    PRO: float
    SCA: float
    YUN: str

class MeasurementOptions(Enum):
    pass

@dataclass
class Measurement:
    MeasurementOptions = MeasurementOptions

class Oscilloscope:
    '''
        This class will be responsible for shared communication between
        channels and picking the channel allowed to CURV
    '''
    cols = {
        'DEFAULT': '\033[0m',
        'YELLOW' : '\033[93m',
        'BLUE'   : '\033[36m',
        'PINK'   : '\033[95m',
        'GREEN'  : '\033[92m',
        'RED'    : '\033[91m'
    }

    Aquire = Acquisition
    Horizontal = Horizontal
    Vertical = Vertical
    # CH1: Channel
    # CH2: Channel
    # CH3: Channel
    # CH4: Channel

    def __init__(self, oscil):
        self.osc = oscil
        # should call setChannel on the channel associated with DAT:SOU
        self.setChannel(int(self.osc.query("DAT:SOU?").strip()[-1]))

        print(oscil.query('*IDN?'), end='')
        print(self.HorizontalParams())


    def setChannel(self, channel):
        self.activeChannel = channel
        if channel < 1 or channel > 4:
            raise ValueError("Channel must be between 0 and 4") # refactor into custom error class
        self.color =  list(self.cols.values())[channel]
        # there could be implementation to make the oscilloscope "select" the channel or save the channel settings here.

    def getAcquisitionParams(self, set=False):
        '''
        Use Osc.AcquisitionOptions
        '''
        pass    

    def VerticalParams(self, option: VerticalOptions, set=False): # Move into Channel subclass
        '''
            Use VerticalOptions
        '''
        if option == None:
            return self.osc.query(f'CH{self.activeChannel}?').strip().split(';')
        if set:
            self.osc.write(f'CH{self.activeChannel}:{option.name} {set}')
        return self.osc.query(f'CH{self.activeChannel}:{option.name}?')
        
    def HorizontalParams(self, option: HorizontalOptions = None, set=False):
        '''
        use OSC.HorizontalOptions.SCA
        
        SCA  SCAle -> float
        POS  POSition -> float
        RECO RECOrdlength -> int
        '''
        if option==None:
            return self.osc.query("HOR?")
        if set:
            self.osc.write(f'HOR:{option.name} {set}')
        return getattr(self.Horizontal, option.name) or self.osc.query(f'HOR:{option.name}?')

    def curvInit(self):
        self.osc.write("DAT INIT")
        self.osc.write(f"DAT:SOU CH{self.activeChannel}")
        self.osc.write("DAT:WID 1")
        self.osc.write("DAT:ENC RPB")

    def CURV(self) -> List:
        return self.osc.query_binary_values("CURV?",'B')

    def write(self, command):
        '''
        a function for writing directly to the oscilloscope.
        internal use
        '''
        self.osc.write(command)
    
    def query(self, command):
        '''
        a function for querying direct to the oscilloscope.
        internal use
        '''
        self.osc.query(command+'?')
    
    def print(self, value, name: str = ''):
        if not name:
            print(f'{self.color}Channel {self.activeChannel} info:\033[0m {value}')
        else:
            print(f'{self.color}{name}:\033[0m {value}')
        
    def __del__(self):
        self.osc.close()
        print('Connection to oscilloscope closed')

# Sweep Expansion
def findSweep(o: Oscilloscope, channel:int = 4) -> int:
    '''
    Given an oscilloscope object, returns a tuple with 
    (sweep expansion, volts per pixel, and seconds per pixel)
    '''
    divsPerScreen = 10
    o.setChannel(3)
    o.curvInit()
    o.CURV()
    voltsPerPix= float(o.VerticalParams(VerticalOptions.SCA))*8/255 # 255 depends on WIDTH 1
    secondsPerPix=float(o.HorizontalParams(HorizontalOptions.SCA))/float(o.HorizontalParams(HorizontalOptions.RECO))*divsPerScreen
    
    #Slope in Pix
    sweepCurv = o.CURV()
    sweepCurv = [sum(sweepCurv[0+10*i:10+10*i])/10 for i in range(len(sweepCurv)//10)]

    slopeSweep = np.gradient(sweepCurv)/10
    slopeSweep= slopeSweep[slopeSweep>0]
    sweepAvg=np.mean(slopeSweep)
    #slope in Volts per Second
    sweep=sweepAvg*voltsPerPix/secondsPerPix
    # o.print("VOLTS per SECOND", sweep)
    # o.print("SECONDS per 15V sweep", 15/sweep)
    expansions = [1,2,5,10,20,50,100]
    o.HorizontalParams(HorizontalOptions.POS)
    # o.print("hScale", float(o.HorizontalParams(Osc.HorizontalOptions.SCA)))
    # print(0.01*np.array(expansions)-np.array([15/sweep for i in range(len(expansions))]) )
    expansion = expansions[np.argmin(np.abs( # index of minimum value of absolute value of difference in risetime options and calculated risetime
            0.01*np.array(expansions)-np.array([15/sweep for i in range(len(expansions))]) 
        ))]
    # o.print("SweepExpansion", expansion)
    return expansion

def main():
    import pyvisa
    rm = pyvisa.ResourceManager()
    o = Oscilloscope(rm.open_resource(rm.list_resources()[0]))

    o.setChannel(1)
    # o.HorizontalParams(HorOptions.SCA, 1E-2)
    # print(o.HorizontalParams())

if __name__ == "__main__":
    pass
