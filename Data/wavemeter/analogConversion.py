def analogConversion(voltage, setPoint=780.000, analogRes=0.001):
    '''
    This function should take an averaged analog output, collected via pyvisa, and convert it into the displayed wavelength on the front panel.
    See manual section 5.2.3
    @param voltage
    @param setpoint: nanometers Inputted into the front of the Burleigh WA1000
    @param analogRes: nanometers Inputted into the front of the Burleigh WA1000
    '''
    # The manual gives an equation $(Analog Output Voltage) =  0.0049*(Deviation in nm)/(Analog Res) + Offset$
    # Offset will need to be calculated via the difference in reading through this program and on the face of the wavemeter

    offset = 0 
    deviation = (voltage - offset)/0.0049 * analogRes
    return(setPoint - deviation)