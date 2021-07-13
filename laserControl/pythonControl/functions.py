def paramRef(dlc, command):
    dlc.write("(param-disp " + command + ")")
    dlc.read()
    return dlc.read().strip()

def paramDisp(dlc, command):
    dlc.write("(param-disp " + command + ")")
    response = dlc.read()
    while response != 0:
        print(response, end='')
        response=dlc.read()

def exec(dlc, command):
    dlc.write("(exec " + command + ")")