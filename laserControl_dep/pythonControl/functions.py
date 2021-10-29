def paramRef(dlc, param_name):
    dlc.write("(param-disp " + param_name + ")")
    dlc.read()
    return dlc.read().strip()

def paramDisp(dlc, param_name):
    dlc.write("(param-disp " + param_name + ")")
    response = dlc.read()
    while response != '0\r\n':
        response=dlc.read()
        print(response, end='')
        
def exec(dlc, param_name):
    dlc.write("(exec " + param_name + ")")

def addListener(dlc, param_name: str, period: int, threshold: float):
    dlc.write(f"(add '{param_name} {period} {threshold})")

def removeListener(dlc, param_name:str):
    dlc.write(f"(remove '{param_name}")

if __name__ == "__main__":
    import pyvisa
    rm = pyvisa.ResourceManager()
    dlc = rm.open_resource(rm.list_resources()[2])
    
    paramDisp(dlc, "'laser1")
    
    dlc.close()