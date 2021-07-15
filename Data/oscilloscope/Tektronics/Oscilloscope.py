# from Channel import Channel
import os
from enum import Enum, auto

os.system('color')

class AcquisitionOptions(Enum):
    MOD = auto()
    NUMAC = auto()
    NUMAV = auto()
    STATE = auto()
    STOPA = auto()

AcquisitionOptionTypes = {
    AcquisitionOptions.MOD: auto(),
    AcquisitionOptions.NUMAC: auto(),
    AcquisitionOptions.NUMAV: auto(),
    AcquisitionOptions.STATE: auto(),
    AcquisitionOptions.STOPA: auto(),
}

class HorizontalOptions(Enum):
    VIEW = auto()
    RECO = auto()
    POS = auto()
    SCA = auto()
    DEL = auto()

HorizontalOptionsTypes = {
    HorOptions.VIEW: str,
    HorOptions.RECO: int,
    HorOptions.POS: float,
    HorOptions.SCA: float,
}

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

    def AcquisitionParams(self, option : AcquisitionOptions =None, set=False):
        '''
        Use
        '''
        
        pass    

    def VerticalParams(self, option=None, set=False): # Move into Channel subclass
        '''
        Put None, for all parameters
        options = {
            "BAN": "BANdwidth",
            "COUP":"COUPling",
            "CURRENTPRO":"CURRENTPRObe",
            "INV":"INVert",
            "POS":"POSition",
            "SCA":"SCAle",
            "YUN":"YUNit"
            }
        '''
        options = {
            "BAN": "BANdwidth",
            "COUP":"COUPling",
            "CURRENTPRO":"CURRENTPRObe",
            "INV":"INVert",
            "POS":"POSition",
            "SCA":"SCAle",
            "YUN":"YUNit"
            }
        if option == None:
            return self.osc.query(f'CH{self.channel}?').strip().split(';')
        if options[option]:
            if set:
                self.osc.write(f'CH{self.channel}:{option} {set}')
            return self.osc.query(f'CH{self.channel}:{option}?')
        
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
            return self.osc.write(f'HOR:{option.name} {set}')
        return HorizontalOptionsTypes.get(option)(
            self.osc.query(f'HOR:{option.name}?')
            )

    def curvInit(self):
        self.osc.write("DAT INIT")
        self.osc.write(f"DAT:SOU CH{self.channel}")
        self.osc.write("DAT:WID 1")
        self.osc.write("DAT:ENC RPB")

    def CURV(self):
        return self.osc.query_binary_values("CURV?",'B')

    def print(self, value, name: str = ''):
        if not name:
            print(f'{self.color}Channel {self.Channel} info:\033[0m {value}')
        else:
            print(f'{self.color}{name}:\033[0m {value}')
        
    def __del__(self):
        self.osc.close()
        print('Connection to oscilloscope closed')
    
if __name__ == "__main__":
    import pyvisa
    rm = pyvisa.ResourceManager()
    o = Oscilloscope(rm.open_resource(rm.list_resources()[0]))

    o.setChannel(1)
    # o.HorizontalParams(HorOptions.SCA, 1E-2)
    # print(o.HorizontalParams())