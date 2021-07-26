# laserStabilization
An encompassing repository for the 2021 UKY REU Program. We will store and share data related to the Laser Frequency stabilization project here.

# DLC Pro Locking Instructions

Author: Will
Date : 7/26/21

These instructions will guide you through the process of top of fringe locking on a saturated absorption signal using the Toptica DLC Pro. This instruction set was written by Will Bodron and Charlotte Zehnder as a part of the 2021 UKY Summer Physics REU program.

### 1. Construct the Saturated Absorption Experiement

A simple Saturated Absorption layout should be constructed with a portion of the laser light. This layout **minimizes backreflection** into the rest of the experiment (though you can **use backreflection to align the mirror** to for good counterpropogation through the gas cell). 

![Beam Return Trip](https://user-images.githubusercontent.com/42518694/127022739-a42df640-fe1b-452a-abd3-07df6320bdae.PNG)

In order to reduce the power of the probe beam, we propose adding a 30% attenuator (or non-polarizing beamsplitter and endstops) between the gas cell and the left side mirror.

$$I_{probe} = (0.3)(0.3)I_{pump} \approx (10\%)I_{pump}$$

---
### 2. Enable a scan. 
   - Plug the photodiode into one of the Fine In ports on the front of the DLCPro controller.
   - This will cause the laser to sweep through a range of wavelengths by varying the voltage to the piezo. 
   - Press the second button from the top on the left to open the scan window.
   - The virtual button in the top middle will enable a scan, using the scan offset and scan amplitude as a range. *The laser has software to prevent you sending too much voltage to the piezoactuator.*
---
### 3. Find the signal.
  - Your lock-input signal should be chosen. (parameter button is the book on the bottom left)
    
    > Scan > Parameters > Lock Settings > Lock Input Signal <- Fine In 1

  - It is possible that the screen is displaying more or different information.
    > Scan > Parameters > Display Settings > Input Trace Selection <- Lock Input

    > Scan > Parameters > Display Settings > Auxillary Trace Selection <- None
  - Use two-finger zoom and vertical or horizontal swipes to locate this signal.
---

![SaturatedAbsorption](https://user-images.githubusercontent.com/42518694/127036425-a6346557-9d11-498c-95a6-28c039012a3a.PNG)

---
### 4. Use Modulation.
   - Zoom in further on the location you wish to lock. This waveform is from the right side of the one given from part 3.
   > Scan > Parameters > Lock Settings > Lock Type > Top of Fringe
   - Open the *LIR panel* on the scan screen. The middle bottom virtual button opens a dropdown.
   - Set the phase to $~30\degree$, the modulation frequency to $22000 \text{ Hz}$, and the modulation amplitude to $0.04 \text{ mA}$. These values may not be the same for a different layout, but they will likely be close. 
![Modulation](https://user-images.githubusercontent.com/42518694/127036431-1a8ea694-5c03-47b9-90e4-8a505549e167.png)
---
### 5. Visualizing the error.
   - The laser does not support outputting the raw error that is sent to the PID controllers. This value however is valuable for tuning. We achieved locking with only one PID controller, so we used the other to monitor the error outputed by the modulation. This was done by setting all constants to 0 on PID 1 except for P=1. Therefore, the equation for PID1 was:
$$ PID1(t) = 1*error(t) + \int_0^t 0*error(\tau)d\tau + 0*\frac{d}{dt}error(t) = error(t)$$

   - Set the output of PID1 to output channel B.
     > Scan > Parameters > PID1 > Output Channel > Output B
---
### 6. (Optional) Visualize the response function.
   - PID2 will control the piezoactuator. This is the quickest and most precise avenue of control for the laser. The voltage sent to the piezo actuator will be the voltage at the time of the start of the lock plus value of PID2.
   - If you want to visualize the value of PID2, set its output channel to Output A
      > Scan > Parameters > PID2 > Output Channel > Output A
   - Using a BNC splitter, connect output A to fine In 2 and an oscilloscope or multimeter.
   - Set the Piezo actuator to be controlled by Fine In 2
      
      > Scan > Parameters > Analog Remote Control (ARC) > PC > Enable <- 1
      
      > Analog Remote Control (ARC) > Singal Input <- Fine In 2
      
      > Analog Remote Control (ARC) > Factor > 1.0000 V/V
---
### 7. Applying PID Gains. 
   - Ensure the output of PID2 is directed to PC (piezo control)
   - A set of constants we found that worked well was
   
   |||
   |---|---|
   | P | 0.001 V/V |
   | I | 0.003 V/V/ms|
   | D | 0.000 V/V*$\mu$s|
   | Gain | 1.000|
   - PID2 needs to be set as sign positive or sign negative. This depends on the slope of your modulated signal. **If the slope of the modulated signal is negative at the point you wish to lock, set PID2 to sign positive and vise versa.**
     > Scan > Parameters > PID2 > Sign Positive <- 1
   - `1` for sign positve, `0` for sign negative
---
### 8. Activating the Lock
   - On the LIR Scan screen, locate the peak you wish to lock. Simply click it and the now enabled lock button on the left.
--- 
### 9. Monitoring the lock.
   - Certainly, if the error signal becomes large and is not sent back to zero by the PID controller, you may need to reevalute your PID constants or modulation settings.
   - Use a camera to monitor spontaneous emission
   - Finally, use a Fabry-Perot Interferometer. Display the transmission through the device on an oscilloscope and run `python .\Data\oscilloscope\driftMeasurement.py`
     - This code requires a significant amount of libraries and drivers.
     - `pip install pyvisa`
        
- pyvisa needs a suitable usb driver to communicate with the oscilloscope. This can be found on the tektronics website
- `pip install toptica-lasersdk`
- `pip install numpy`
