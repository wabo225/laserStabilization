06/30/2021
Goals:
Set up Fabry Perot 
Attatch to Oscillisope

7/22/2021
PID Observations


Observing PID 2 output

Set-up
Analog Remote Control-> PC remote Control -> Signal Input --> Fine in 2(set PC to output through I/O board [PID2 settings->output channel A] Split output A back to fine in 2 and to oscilloscope to watch PID 2 output changes )

PID seems 

Observations:

Increasing laser Temp without lock knocks off resonance as seen with infrared camera and fabry perot extreme movement

With lock, brightness of camera does not seem to vary as much 


7/23/2021
Decreasing the current corresponds to left movement of pixels 

** need to check that sign is correct for pixel change and frequency change.
Left movement for the fabry perot should mean an increase in frequency and decrease in wavelength 

Test: 
Move current left --left fabry perot-- How does wavelength change-- increased 780.44nm to 780.053 

fabry moves right - increasing wavelenth decreases piezo 

7/26/21

Added linear polarizer after half wave plate to reduce power without changing current
minimum 78 um -- doppler free spectrum dissapears-- may work with 90/10 method
attempting lock at lower power


Tried to maximize signal -- reduced power until peak was less prominent-- adjusted mirror to maximize peak

TOF locking with reduced power



![No Locking Graph](https://user-images.githubusercontent.com/69656527/127023960-f4bd2807-a6ad-4a58-99fc-1ffc81927f4a.png)

**y=-8.70015*10^-6 x-0.00171916 Slope Error:5.70054 E-7**

TOF Trial2 Low Power -- ~2mV
![Low Power TOF](https://user-images.githubusercontent.com/69656527/127025435-8c24de6f-6e77-49c7-859b-d0aa2613322f.png)

**y=-1.74068 E-7 x- 0.0227541 Slope Error:3.03402 E-6**


TOF 3 Trial Low Power~ 2.5 mV  50 C locked to Fg=2 87Rb Transition 
![Low Power TOF](https://user-images.githubusercontent.com/69656527/127167099-8f1e583e-f0dd-4927-8b09-3eb8b7f0c8f9.png)

**Unlocked : y= - 0.0000158461x -0.0118368 Slope Error:4.49543 E^-7**
**Locked : y= 6.27708 E-6 x + 0.0122903 Slope Error:5.05484 E^-7**



7/27

Realigned saturated absorption 
check for back reflection: first at quarter wave plate then half wave plate the 

Coupled into Bristol wavemeter 
comparing fabry perot with wavemeter--
Both seemed to have a larger spread than friday measurements
![Fabry VS WAVEMETER VS BEST](https://user-images.githubusercontent.com/69656527/127355520-f5ea255f-99ca-49e9-898d-2364f80a2b2d.png)


Measuring Doppler Broadening as cell is heated 
1.5Gz= 3.158805 V (piezo)
![Saturated Absorption Room Temp](https://user-images.githubusercontent.com/69656527/127486718-20463fca-100d-4560-88e1-706c113bb77f.png)

![Saturated Absorption 50 deg](https://user-images.githubusercontent.com/69656527/127486903-1dec0434-7cfe-45b0-8a1f-116d4da4a934.png)