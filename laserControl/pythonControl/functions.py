def paramRef(dlc, command):
    dlc.write("(param-disp " + command + ")")
    dlc.read()
    return dlc.read().strip()

def paramDisp(dlc, command):
    dlc.write("(param-disp " + command + ")")
    response = dlc.read()
    while response != '0\r\n':
        response=dlc.read()
        print(response, end='')
        
def exec(dlc, command):
    dlc.write("(exec " + command + ")")

if __name__ == "__main__":
    import pyvisa
    rm = pyvisa.ResourceManager()
    dlc = rm.open_resource(rm.list_resources()[2])
    
    paramDisp(dlc, "'laser1")
    
    dlc.close()