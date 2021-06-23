import pyvisa

rm = pyvisa.ResourceManager()
print(rm.list_resources())

oscilloscope = rm.open_resource(rm.list_resources()[0])

SCPI = ''
while True:
    print('> ', end='')
    SCPI = input()
    if SCPI.endswith('?'):
        print(oscilloscope.query(SCPI), end='')
    else:
        oscilloscope.write(SCPI)