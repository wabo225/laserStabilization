import Oscilloscope
from enum import Enum, auto

class COUPling(Enum):
    AC = auto()
    DC = auto()
    GROUND = auto()

class VerticalOptions(Enum):
    BAN = auto()
    COUP = auto()
    CURRENTPRO = auto()
    INV = auto()
    POS = auto()
    PRO = auto()
    SCA = auto()
    YUN = auto()

VerticalOptionTypes = {
    "BAN" : Oscilloscope.ONOFF,
    "COUP" : str,
    "CURRENTPRO" : float,
    "INV" : float,
    "POS" : float,
    "PRO" : float,
    "SCA" : float,
    "YUN" : str
}

class Channel(Oscilloscope):
    channels = {
        1: "YELLOW",
        # 'math': 'RED',
        2: "BLUE",
        3: "PINK",
        4: "GREEN",
    }

    def __init__(self, channel):
        self.color = self.channels[channel]
        self.channel = channel
        
        self.osc = super().osc

    def print(self, value, name: str = ''):
        super().print(value, name)

    query = lambda self, param, set_param: super().print(
            (self.osc.write if set_param else self.osc.query)(
                f'CH{self.channel}{":"+param if param else ""}{" " + set_param if set_param else "?"}'
            )
        )

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
        # This function is similar to Osc.HorizontalParams Consider making a higher order function
        # Decided against it since the formatted strings are significantly different
        if option == None:
            return self.osc.query(f'CH{self.channel}?')
        if set:
            self.osc.write(f'CH{self.channel}:{option.name} {set}')
        return VerticalOptionTypes.get(option)(
            self.osc.query(f'CH{self.channel}:{option.name}?')
        )


if __name__ == "__main__":
    from Oscilloscope import Oscilloscope
    import pyvisa
    rm = pyvisa.ResourceManager()
    o = Oscilloscope(rm.open_resource(rm.list_resources()[0]))
    ch1 = Channel(1)
