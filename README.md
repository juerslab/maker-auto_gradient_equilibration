# Auto Gradient Equilibration
This project aims to simplify the equilibration of macromolecular crystals to new solutions, by minimizing the pipetting required. Crystals are placed into a small (~40 µL) reservoir and the reservoir solution is automatically changed over time at a user-defined rate. Crystals can be left for slow, gentle solution exchange while other work is being done in the laboratory.

<img src="Schematic-detail.tiff" alt="drawing" width="700">

Schematic (left) and detail (right) of the general strategy used here for crystal solution exchange.


<img src="System_overview.tiff"  width="700">

Overview of system. The crystals sit in a pot located on the blue housing. Two syringes are used to pump new solution into the pot while simultaneously removing solution from the pot. The system is controlled with a python based gui to set up gradient parameters. As shown, there is a Raspberry Pi computer (mounted beneath the screen) sending commands to an Arduino microcontroller with stepper motor drivers (beneath the red housing), which control the stepper motors (lower right). The stepper motors are coupled to threaded rods that move the white housing up and down to move the syringe plunger. Also beneath the red housing on the left  is a microscope used to visualize the sample.  

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

a. Flash the Arduino with arduino_serialCOM_v0.x.y.ino  (0.1.1 as of Feb2025)
b. If not present, install python3. Also install opencv (the codes depends on cv2).  
c. Copy poseidon_gf_main_v0.x.y.py and poseidon_controller_gf_gui.py to the same directory on the computer that will run the system. (0.1.1 as of Feb2025)

## Running instructions

1. Power up the stepper motor controllers by pluggin in.
2. Connect the Arduino to the USB port of the computer you are using 
3. Run the python program poseidon_main_gf_v0.x.y.py. The program poseidon_controller_gf_gui.py needs to be in the same directory as the main program.
4. Once booted up, there is some help available from the gui.


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
   	c. 
