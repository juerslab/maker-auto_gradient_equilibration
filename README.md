# Auto Gradient Equilibration
This project aims to simplify the equilibration of macromolecular crystals to new solutions, by minimizing the pipetting required. Crystals are placed into a small (~40 µL) reservoir and the reservoir solution is automatically changed over time at a user-defined rate. Crystals can be left for slow, gentle solution exchange while other work is being done in the laboratory.

The project uses an open source syringe pumping system located here:  https://github.com/pachterlab/poseidon

## Build instructions

### 1. Build and assemble the auto gradient equilibration hardware

The syringe pumping system uses stepper motors to move the plungers on standard disposable syringes with precise displacements. The stepper motors are controlled via an Arduino microcontroller with stepper motor drivers. A Python program issues commands to the microcontroller to move the syringes and communicates with a simple microscope for visualization of the sample. The Python program can be set up to run on any laptop or desktop computer. As described here, a Raspberry Pi computer is used. 

Detailed instructions on how to make the syringe pumping system are located here: https://pachterlab.github.io/poseidon/

A brief summary is here:
- Purchase the required parts.
- Download and 3D print parts (this repository includes copies of all 3D print files):
	- Syringe pump pieces
	- Raspberry pi/microscope framework
	- Crystal pot holder
- Assemble the syringe pumps. See build videos linked above.
- Assemble the Arduino & stepper motor controllers
- Assemble the Raspberry Pi with screen (if using)

### 2. Install software. 

The syringe pumping software was modified for auto serial dilution applications. To install the software:

a. Flash the Arduino with arduino_serialCOM_v0.1.ino (unmodified from the original version).   
b. If not present, install python3.   
c. Copy poseidon_gf_main.py and poseidon_controller_gf.py to the same directory on the computer that will run the system.

## Running instructions

1. Power up the stepper motor controllers. 
2. Run the python program poseidon_main_gf.py. The program poseidon_controller_gf_gui.py needs to be in the same directory as poseidon_main_gf.py. 


## Manuscripts


## Presentations
This work was presented in a poster at the ACA Meeting in Portland, OR in summer 2023.

## Other tidbits

### Raspberry Pi and Touch Screen
It is possible to use the touch screen only on a Raspberry Pi (or just the mouse with onscreen keyboard) to run the system. To do so:
1. Install an on-screen keyboard: https://pimylifeup.com/raspberry-pi-on-screen-keyboard/
2. Turn the poseidon_main_gf.py into a clickable executable:
   	a. Add #!/usr/bin/python3 to the first line of poseidon_main_gf.py
    	b. chmod +x poseidon_main_gf.py
   	c. .....
