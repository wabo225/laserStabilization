import os
os.system('color')

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
        print(oscil.query('*IDN?'), end='')


    def setChannel(self, channel):
        self.channel = channel
        if channel < 1 or channel > 4:
            raise ValueError("Channel must be between 0 and 4")
        self.color =  list(self.cols.values())[channel]

    def VerticalParams(self, option=None, set=False):
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
        
    def HorizontalParams(self, option=None, set=False):
        options = {
            "SCA": "SCAle",
            "POS":"POSition",
            "RECO":"RECOrdlength"
        }
        if option==None:
            return self.osc.query("HOR?")
        if options[option]:
            if set:
                return self.osc.write(f'HOR:{option} {set}')
            return self.osc.query(f'HOR:{option}?')

    def curvInit(self):
        self.osc.write("DAT INIT")
        self.osc.write(f"DAT:SOU CH{self.channel}")
        self.osc.write("DAT:WID 1")
        self.osc.write("DAT:ENC RPB")
        pass

    def CURV(self):
        return self.osc.query_binary_values("CURV?",'B')

    def print(self, name, value):
        if self.channel:
            print(f'{self.color}{name}:\033[0m {value}')
        else:
            raise NameError("Channel is undefined")

    def __del__(self):
        self.osc.close()
        print('Connection to oscilloscope closed')
    
if __name__ == "__main__":
    import pyvisa
    rm = pyvisa.ResourceManager()
    o = Oscilloscope(rm.open_resource(rm.list_resources()[0]))

    o.setChannel(1)
    o.HorizontalParams("SCA", 1E-2)
    print("HOR:SCA:", o.HorizontalParams("SCA"))