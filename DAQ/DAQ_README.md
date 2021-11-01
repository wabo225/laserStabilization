# Laser Stabilization Lab 2021
## Data Aquisition Usage Guide

Author: Will Bodron
Mentor: Dr. Wolfgang Korsch

This file contains information on the usage of this package. The goal of the project was to accelerate access to data collection, laser control, and enabling automation of both.

The packages are made to be reused as well as model future projects of this lab automation form.

Thus far, there are three instruments with communication wrappers (communication with a particular machine is nontrivial, but abstract that away, and you can communicate safely with similar syntax)
1. Tektronics Oscilloscope (./oscilloscope)
2. Bristol Wavemeter (./wavemeter)
3. Toptica Diode Laser Controller (./DLC)

### Requirements

1. `python 2.7`
2. `pip install toptica-lasersdk`
3. `pip install numpy`
4. `pip install scipy`
5. `pip install matplotlib`

You also need to enable telnet communication. This is machine specific and not too difficult. Communication with the bristol works through a 'server' hosted by the instrument, and communication is through telnet protocol.



