import Oscilloscope

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
        global osc
        self.osc = osc

    def query(self, command, param):
        print(
            osc.query(f'CH{self.channel}?')
        )



if __name__ == "__main__":
    from Oscilloscope import Oscilloscope
    import pyvisa
    rm = pyvisa.ResourceManager()
    o = Oscilloscope(rm.open_resource(rm.list_resources()[0]))
    ch1 = Channel(1)
