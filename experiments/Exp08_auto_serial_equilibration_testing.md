## Title: Exp08 Auto serial equilibration testing
## Date: 2024-12-06 (notes date; exps from 2022)
## Goals: To develop and test use of the auto serial equilibration system


Thurs, March 25, 2022

Have been working on the poseidon controller the last couple weeks - 
improving the linear option originally written by Sean Stothers.

Today successfully equilibrated a large ~ 1000 x 300 x 100 microns to 25% glycerol using
this device.

Params.

Crystal from tray alpha-lact.13; transferred to a starting solution of 20% P8K, 50 mM KH2PO4 
in a clear pcr tube cap with starting volume of 40 µL. 

The Linear Concentration Gradient option was used to exchange it to the same buffer with 25% glycerol over 50 minutes. 
Photos were taken before each injection. 
Params: Starting conc: 0; Target conc: 9 M; Syringe conc: 10 M; Ratio: 0.5; Injections: ?

and then, over 5 min: 
Params: Starting conc: 0; Target conc: 9 M; Syringe conc: 10 M; Ratio: 0.5; Injections: ?

(Photos are on the raspberry pi that runs the syringe pumps.)

This crystal was then mounted on the diffractometer using the RH Cube at 75% RH/8 LPM and 
a data set was collected. The data started dying after a few hours. 

The next morning, the crystal looked visibly in good condition, seeming like it hadn't dried out.
I demounted the crystal into the glycerol buffer, and it suffered a couple cracks, but 
nothing dramatic.

Fri, March 26, 2022

Now try a similar experiment using 25% xylose rather than 25% glycerol.
This crystal dissolved fairly quickly - possibly b/c I used 18% PEG/low salr rather than 20% PEG, 
and also maybe b/c the xylose/PEG was very old, so degraded? (I couldn't find any xylose powder, but
found this old solution, that I tried.)

So now try with 25% mpd, using the same starting solution as yesterday. 
This was a fail, because the inject tubing wasn't contacting the solution.

Try dumping xtal into the solution - cracked - image 2022-03-25 11_17-_59.png
Try again as above - 50 minute experiment. 

This again failed - as if the injection pump was pushing a smaller volume than the extraction pump. 
Could this be a viscosity differential? Evaporation?

Mon, March 28, 2022

Tried a couple tests w/o crystals. Didn't see the problem from Friday. 

Tue, March 29, 2022

Try again w/ crystals. It worked this time. Crystals equilibrated nicely in 30 minutes.
Dumping a crystal into this solution (20% P8K, 50 mM salt, 25% mpd) caused lots of cracking.
See photo 2022-03-25 11_01_40, which shows a larger crystal cluster that was slowly equilibrated
vs smaller dumped crystal.

Thu, April 7, 2022

Equil xtal.
aLact.A2 crystal
Start: 20% P8K, 50 mM Salt; 40 µL) -photos on Pi and M205C
Ramp: 30 minutes to 0.9 x (above + 25% mpd). This failed - crystal was cracked after equilibration.

Try again:
aLact.A2 crystal
Start: 20% P8K, 50 mM Salt; 40 µL) -photos on Pi and M205C
Ramp: 50 minutes to 0.9 x (above + 25% mpd). This failed - crystal was cracked after equilibration.

Another try failed b/c the injection syring ran out of solution.

Another try succeeded. 50 minutes to 0.9 x(above + 25% mpd), 5 minutes to 0.99 x (above + 25% mpd). See photos on 
M205C and Pi

Fri, April 8, 2022
Now as above but with 25% glycerol as target. Failed - cracked a lot after a few min.

Try again with 25% glycerol. 50 min to 0.9 x 25%. This worked. Photos on Pi but not M205C.

Tue, April 12, 2022

Try again with 25% glycerol. 50 min to 0.9 x 25%. This worked for one crystal. Photos on Pi and M205C.
There were, however, problems with overflowage - possibly from capillary action between the wall of the 
pcr tube top and the jig used to hold the tubes.

Fri, April 15, 2022
Made a new jig that attempts to get rid of capillary overflowage.
Tried again with glycerol, but lost the crystal in the outflow tube when manually trying 
to reduce the volume after using the wrong pump for the outflow. However, the new jig seems 
to work well in preventing capillary overflowage.

Sat, April 16 2022
Try again with glycerol. 25%. 30 min to 0.9 x 25%. 

Thu, June 9, 2022
Crystals: Hex TLN
Starting solution: 2 M AmSO4/ 40 µL
Target solution: water
30 min to 0.05 M; failed (bread slicing) at about 20 minutes. Try again with slower gradient, 
or maybe with the input at the bottom of the cap, since the density of water is less than 2 M
AmS)4.

Starting solution: 2 M AmSO4/ 40 µL
Crystals: Hex TLN
Target solution: water
30 min to 0.05 M; repeat for 10 min so to ~ pure water.
Input at bottom of well; outflow at mid-height.
This also failed. 
Possibly these crystals aren't stable in water b/c they're so new? Check tomorrow.

Fri, June 10, 2022
Crystals: Hex TLN; Tray 63; well A8
Target solution: water
30 min to 0.05 M; 10 min to 0.01 M
Input at bottom of well; outflow at mid-height.
- Rule of thumb could be to place input height 
This worked! 

Crystals: Tet HEWL; Tray 16; well A6
Target solution: 7% NaCl, 25% Glycerol, 20 mM NaOAc 5.2
15 min to 24%; worked; no photo

Mon, June 12, 2022
Crystals: Tet HEWL; Tray 16, well B6 (6% NaCl)
Target solution: 3% NaCl, 20 mM NaOAc 5.2
30 min (1950 s) to 3%; no internal cracks, but some surface degradation

Crystals: Tet HEWL; Tray 16, well A3 (4.2% NaCl)
Target solution: 3% NaCl, 20 mM NaOAc 5.2
30 min (1950 s) to 3.1%; this worked, but crystals dumped into this solution didn't crack.
So go back to glycerol equilibrations...


Crystals: Tet HEWL; Tray 16; well C6
Target solution: 7% NaCl, 25% Glycerol, 20 mM NaOAc 5.2
30 min to 24% glycerol; worked; no photo, but crystals dumped into this solution didn't crack.
Weird...

Crystals: Tet HEWL; Tray 16, well D6 (6% NaCl)
Target solution: 3% NaCl, 20 mM NaOAc 5.2
30 min (1950 s) to 3.5%;
15 min to 3.05

Tue, June 14, 2022
Crystals: Hex TLN; Tray 63; well C5
Target solution: water
30 min to 0.05 M; 15 min to 0.01 M
Input at bottom of well; outflow at mid-height.
Worked very nice. Many crystal equilibrated to water.

Wed, June 15, 2022
Crystal

Crystals: aLact.15.A4
Start: 20% P8K, 50 mM Salt; 40 µL) -photos on Pi and M205C
Ramp: 50 minutes to above + 24% glycerol). 
Succeded, but xtal was somewhat poor looking from the start.

Crystals: aLact.13.B3
Start: mostly well solution, but some of the above (20% P8K, 50 mM salt), which caused cracking.
Need to start with well solution!!!!  -photos on Pi and M205C
Ramp: 80 minutes to above + 24% glycerol). 
Succeded, but xtal was somewhat poor looking from the start.

Thu, June 16, 2022
Crystals: aLact.13.C4
Start: mwell solution; this worked
Ramp: 50 minutes to above + 24% glycerol). 
One crack, probably caused by initial drop of glycerol from the tube into the well.
Otherwise succeeded. 

Crystals: aLact.13.C4
Start: mwell solution; this worked
Ramp: 50 minutes to above + 24% glycerol). Tried repositioning
This also had a longitudinal crack.

Wed, June 29, 2022 (I think)
Crystals: aLact.16.c3
Start: well solution:
Ramp1: 50 min to 96% of {19.5% P8K, 50 mM salt, 25% glycerol}
Tried the following :
a. Instead of positioning input tube directly above crystal, positioning above and offset
b. Start with a small air pocket in the tube to prevent drop of the higher density liquid
Seems good.
Ramp2: 15 min to 99.6% of {19.5% P8K, 50 mM salt, 25% glycerol}
Still good. 
Photos on Pi & M205C. 

Thu, June 30, 2022
Crystals: aLact.16.c4
Start: well solution:
Ramp1: 50 min to 96% of {19.5% P8K, 50 mM salt, 25% glycerol}
Tried the following :
a. Instead of positioning input tube directly above crystal, positioning above and offset
b. Start with a small air pocket in the tube to prevent drop of the higher density liquid
Seems good; maybe a little dissolved.
Photos on Pi & M205C. 

Fri, July 1, 2022
Crystals: lyz.17.c6
Start: well solution (8% NaCl)
Ramp: 1225 sec to 3.1 % NaCl
This worked, but there was some surface degradation and cracking of some of the crystals.
Possibly try a less steep gradient.

Crystals: lyz.17.D6
Start: well solution (8% NaCl)
Ramp: 2400 sec to 3.1 % NaCl
Worked. Photos on M205C.

Crystals: aLact.16.A4
Start: well solution:
Ramp1: 40 min to 96% of {20% P8K, 50 mM salt, 25% mpd}
Worked. Photos on M205C.

Crystals: aLact.16.B6
Start: well solution:
Ramp1: 40 min to 96% of {20% P8K, 50 mM salt, 25% mpd}
Worked. Photos on M205C

2025-02-11  
Something happened with the SD card on the Raspberry Pi, and I had to restart from the beginning.
1. Install Raspian on SD card. 
2. Install opencv (takes a while):
https://raspberrypi-guide.github.io/programming/install-opencv
3. Make sure calibration.txt is present. Probably should make it possible for it not to be there...\

### Paper revisions. Manuscript was submitted to Acta F. The reviewers have said the following:
Reviewer 1:
4. As mentioned in the discussion, the crystals in the gradient equilibration solution may have defects
not observed by eyes. Could the authors test the crystals with X-ray beam and compare with bad crystals? Could
the authors solve the structure to compare with reported structures?
5. It may be important to keep the humidity while changing crystal solution, could the authors design
and make a small piece of cover to protect the reservoir? And test if it helps to obtain high-quality crystals?
Reviewer 2:
Additional Data: Including X-ray diffraction data for crystals treated using different soaking methods would greatly
strengthen the manuscript. This comparison would provide quantitative evidence of the benefits of the new setup.

So I will do the following:
To address, "Could the authors solve the structure to compare with reported structures?" - 
- collect data and determine structures on long equilibrated crystals 
- compare to data collected on not-equilibrated crystals
To address, "Could the authors test the crystals with X-ray beam and compare with bad crystals?" and "Including X-ray diffraction data for crystals treated using different soaking methods would greatly
strengthen the manuscript. This comparison would provide quantitative evidence of the benefits of the new setup.", I will try a soaking time series, and measure diffraction to get mosaicities and diffraction limit (?)
To address, "It may be important to keep the humidity while changing crystal solution, could the authors design and make a small piece of cover to protect the reservoir? And test if it helps to obtain high-quality crystals?" 


2025-05-02.

Note that all of the crystals here were mounted with micromeshes.

#### Alpha-lactalbumin
1. Alpha-act equilibrated over 45 min
Equilibrating alpha-lactalbumin xtal using auto_equil device with PCR cap
Crystals: aLact.19.D6
Start: well solution (40 μL)
Gradient: 2700 sec to 95% of ML of 20% P8K, 25% glycerol, 50 mM KH2PO4. 
Crystals look ok. Solution withdrawal didn't work great. Final volume greater than 40 μL
Note ML = 20% P8K, 25% glycerol, 50 mM KH2PO4

##### Diffraction exp_2568 (directory lactalbumin)
- using crystal from above equilibration; mounted right after equilibration
- well alact.19.D6
- 600x400x100 μm^3
- ~ 10 μL ML added to cap
- crystal mounted in on mesh in microRT tube against ML
- diffracts to ~ 3.1 A
- collect dataset (orthorhombic - mmm); 0.5 degrees 45 seconds
- the data set went to about 2.5 angstroms
- cell 71.8 104.1 117.7 

2. Alpha-lact not equilibrated

##### Diffraction exp_2574
- well alact.19.D6
- 600x400x100 μm^3
- crystal mounted on mesh in microRT tube against well solution
- diffracts about as well as the above crystal
- collect data set (orthorhombic)
- crystal dies (dries out?) sooner than the above crystal; didn't get a complete data set to 2.5 A.
	- Visible change in diffraction about frame 15
		- before: 68.5 101.4 114.7 (796694)
		- after: 57.8 74.2 89.71 (384620), which is less than half of the above...possibly indicate some drying out
- this reminds me of previous difficulties with alpha-lactalbumin RT data collections, in which the crystal didn't last very long even in a microRT tube. So next time I should probably try to mount against water or in a capillary. Or maybe I already have a RT data set that I can use as comparison. Need to check notebook.
	- After checking notebook, Yes, crystals mounted in microRT tubes usually died or underwent some change about 98% RH.
	- So I try mounting a crystal in a capillary.

##### Diffraction exp_2575
- well alact.19.D6
- 600 x 400 x 100 μm^3
- capillary mount against well solution; fairly wet
- diffracts about as well as the above 2 crystals
- collect ds
- cell 72.0 104.8 117.4

2025-05-04. 
Using RH flow for RT mounts. Estimate 75% glycerol to be 0.92 mol fraction water. So use 92%

##### Diffraction exp_2576
- crystal from 05-02 soak.
- about 600 x 400 x 100
- mounted in micromesh in humid flow at 92%
- diffracts as good or better than exp_2568 crystal
- full ds 0.5 degrees/45 seconds
- cell 72.5 105.4 118.5
2025-05-05. 

##### Diffraction exp_2577
- same xtal as yesterday, was sitting at 92% RH overnight
- still diffracts ok
- pre-exp cell 72.1 104.7 118.1	

##### Diffraction exp_2578
- xtal from alact.19.D6
- about 500 x 400 x 100 
- 1 step into ML - lots of cracking
- mounted in humid flow 92% RH
- poor diffraction 
- pre-exp 2x2 - 8 72 118

##### Diffraction exp_2579 
- same xtal as 2578 but with pre-exp 10x10
- cell 72 10 117 90 90 90
- mosaicity 0.72 0.56 1.17

##### Diffraction exp_2581
- well alact.19.B5
- 500 x 300 x 100
- 15 min gradient equil to ML, then dumped into cryosolution
- 1 crystal cracked (just below the inflow tube); others (not below the inflow tube) didn't crack. this it the one that cracked.
- pre-exp 2x2
- spots beyond 3
- cell 72.4 105.0 118.1
- mos 0.59 0.58 0.85

##### Diffraction exp_2582
- as above but one of the xtals that didn't crack; maybe some cracking when dumping
- 500 x 300 x 100
- pre-exp 2x2
- cell 72.2 105.0 118.1
- mos 0.59 0.59 0.79

##### Diffraction exp_2583
- as exp_2582 - one of the ones that didn't crack (oops mounted directly from gradient solution)
- 400 x 200 x 100
- pre-exp 2x2
- 72.0 104.6 117.7
- mos 0.56 0.56 0.75

##### Diffraction exp_2584
- as above but one of the xtals that didn't crack
- 400x200x100
- pre-exp 2x2
- cell 
- mos 

summary for 15 minute gradient: (these are all from pre-experiments 2x2, 0.5 degrees, 45")
exp # 	| size 			| cell 				| mosaicity 		| res	| visible spots	|
------	|--------------	|------------------	|---------------	|------	|-------------	|
2581	| 500x300x100	| 72.4 105.0 118.1	| 0.59 0.58 0.85	| 3.9	|	2.7			|
2582	| 500x300x100	| 72.2 105.0 118.1	| 0.59 0.59 0.79	| 3.4	|	2.5			|
2583	| 400x200x100	| 72.0 104.6 117.7	| 0.56 0.56 0.75	| 3.9	|	2.8			|
2584	| 400x200x100	| 72.2 104.8 117.9	| 0.50 0.52 0.67	| 5.1	|	2.7			|

Now do a 45 minute gradient equil to ML on crystals from well alact.19.D5. 
exp # 	| size 			| cell 				| mosaicity 		| res	| visible spots	|
------	|--------------	|------------------	|---------------	|------	|---------------|
2585	| 400x200x100	| 72.2 104.9 118.0	| 0.57 0.55 0.80 	| 3.5 	| 2.6   		|
2586	| 400x200x100	| 72.1 105.0 118.1	| 0.57 0.58 0.60 	| 5.0	| 2.8 			|
2587	| 400x200x100	| 72.3 104.8 118.0  | 0.55 0.55 0.73    | 3.6   | 2.5			|	
2588	| 600x200x100	| 72.2 104.8 118.0  | 0.55 0.54 0.70    | 3.7   | 2.7   		|

Now do a 5 minute gradient equil to ML on crystals from well alact.20.B5
exp # 	| size 			| cell 				| mosaicity 		| res	| visible spots	|
------	|--------------	|------------------	|---------------	|------	|---------------|
2589	| 600x400x100	| 72.2 104.9 118.0	| 0.59 0.58 0.83 	| 3.5 	| 2.8  			|
2590	| 600x200x100	| 72.2 105.0 118.0 	| 0.60 0.56 0.67 	| 3.7	| 2.6			|
2591	| 400x200x100	| 72.3 105.0 118.1  | 0.59 0.59 0.82    | 3.8   | 2.7			|	
2592	| 400x100x100	| 72.2 104.9 117.9  | 0.59 0.58 0.90    | 4.9   | 2.8   		|

Now do a dunks into ML on crystals from well alact.20.B5
These all are extremely cracked with very poor diffraction. 

exp # 	| size 			| cell 				| mosaicity 		| res	| visible spots	|
------	|--------------	|------------------	|---------------	|------	|---------------|
2593	| 800x400x100	| 72.2 104.4 117.2	| 0.70 0.65 1.46 	| 5.2 	| 3.3  			|
2594	| 600x200x100	| ?				 	| 0.76 0.57 1.30 	| 4.8	| 3.4			|
2596	| 500x300x100   | 59 73 104			| 0.70 0.55 1.11    | 7.25  | 3.6			|
2600	|

Tried 1 minute soaks, but the gradient software couldn't handle it. 

One curious thing is that the other 45 minute experiments had lower mosaicity. Compare pre-exp mosaicity to actual experiment mosaicity:
exp		|	pre-exp mos		| exp mos			|	comments	|
-------	|-------------------|-------------------|---------------|
2568	| 0.56 0.58 0.79	| 0.59 0.57 0.65	| microRT & ML	|
2574	| 0.56 0.54 0.79 	| ?					| microRT & well|
2575	| ? (1 frame)		| 0.58 0.56 0.60 	| cap & well	|
2576	| ? (3 frames)		| 0.59 0.59 0.60	| RH flow & ML	|

To do when I get back from visiting Dad.
1. Grow crystals of thermolysin
2. Finish the above - more dunks. Possibly 1 minute soaks.
3. Get data on lysozyme and thermolysin

2025-05-12

===============
note all pre-exp exposures are 0.5 degrees 20 seconds
##### Diffraction exp_2595
- crystal dumped into ML w/loop; cracks a lot & breaks into smaller cracked chunks when mounting
- pre-exp 2x2 - got small cell & weird e3 of 0.16; so try more exposures

##### Diffraction exp_2596
- same crystal as above but 5x5 oscillations
- pre-exp analysis: 19%; 60/72/104; 0.70/0.55/1.11
- auto-analysis fails b/c of nobs<3 for one frame

##### Diffraction exp_2597
- same crystal as above but 10x10 oscillations
- pre-exp analysis: 36%; 72/107/118; 0.68/0.60/0.90 (But processing failed midway through the 2nd run)
- full auto warning b/c of nobs<3, but we get 71/107/119; 0.66 0.57 2.12

===============

##### Diffraction exp_2599
- crystal dumped into ML w/ pipettor; cracks a lot...; holds together better than the above when mounting
- very poor diffraction
- 600x500x150 microns
- pre-exp 2x2; poor results...

##### Diffraction exp_2600
- same as above but pre-exp 5x5
- very poor diffraction
- 5%; 7/8/75; 0.69/0.60/0.90

##### Diffraction exp_2601
- same as above but pre-exp 10x10
- pre-exp analysis: 0.57/0.48/0.34
- full auto: 74/102/117 0.77/0.53/3.57

-------------------

#### Lysozyme
ML = 3% NaCl, 20 mM NaOAc pH 5.2.
3% NaCl is about 30/58 = 0.5 M -> 98% RH target

##### Diffraction exp_2602
- DJ.lyz.32.B6 (8% NaCl); RH flow 94%
- 400x400x100
- crystal dumped into ML; small cracks along c-axis
- pre-exp 2x2; 53% 78.8/79.1/38.0; mos 0.57/0.61/0.64
- diff lim 

##### Diffraction exp_2603
Same xtal as above, but 5x5
- 99%; 78.9/78.8/38.0; 0.56/0.60/0.72; diff lim 2.10

##### Diffraction exp_2604
- DJ.lyz.32.B6 (8% NaCl); RH flow 95%
- 400x400x100
- crystal dumped into ML; small cracks along c-axis & 1 larger random crack
- pre-exp 5x5; 84%; 79.0/78.9/38.0; 0.59/0.59/0.63

##### Diffraction exp_2605
- DJ.lyz.32.B6 (8% NaCl); RH flow 95%
- 300x300x100
- crystal dumped into ML; some cracks
- pre-exp 5x5; 97%; 78.9/79.0/38.0; 0.64/0.62/0.83

##### Diffraction exp_2606
- DJ.lyz.32.B6 (8% NaCl); RH flow 95%
- 300x300x100
- crystal dumped into ML; no cracks (?)
- pre-exp 5x5; 98%; 79.0/79.0/38.0; 0.58/0.59/0.70; diff lim > 2.0

======
5 minute gradient equilibration from well solution (8% NaCl) to 95% of 3% NaCl

##### Diffraction exp_2607
- DJ.lyz.32.B6 (8% NaCl); RH flow 96%
- 300x300x100
- 10' gradient equil to ML; no cracks (?)
- pre-exp 5x5; 99%; 79.0/79.0/38.0; 0.58/0.61/0.66; diff lim > 2.0

##### Diffraction exp_2608
- DJ.lyz.32.B6 (8% NaCl); RH flow 96%
- 200x200x150
- 10' gradient equil to ML; no cracks (?)
- pre-exp 5x5; 99%; 79.0/79.0/38.0; 0.58/0.60/0.67; diff lim > 2.0

##### Diffraction exp_2609
- DJ.lyz.32.B6 (8% NaCl); RH flow 96%
- 200x200x150
- 10' gradient equil to ML; no cracks from soak, but possibly a satellite xtal in one quadrant
- pre-exp 5x5; 99%; 79.0/79.0/38.2; 0.59/0.60/0.68; diff lim > 2.0

##### Diffraction exp_2610
- DJ.lyz.32.B6 (8% NaCl); RH flow 96%
- 300x300x100
- 10' gradient equil to ML; no cracks from soak, but possibly a satellite xtal in one quadrant
- pre-exp 5x5; 99%; 79.0/79.0/38.0; 0.59/0.61/0.62; diff lim > 2.0


So we get a slightly smaller mosaicity with the gradient, despite the cracking with dumping. I will try lower NaCl, so see if we get higher mosaicities.

2% NaCl
##### Diffraction exp_2611
- DJ.lyz.32.B6 (8% NaCl); RH flow 96%
- 300x300x100
- dumped into 2% NaCl
- pre-exp 5x5; 99%; 79.0/79.0/38.0; 0.59/0.61/0.61; diff lim > 2.0

Hmmm. Diffracts even better..

I think I made ML incorrectly at 500 mM NaOAc 5.2 rather than 20 mM. This would help to offset the change in salt, and result in less cracking...

Remade ML at 3% NaCl

##### Diffraction exp_2612
- DJ.lyz.32.B6 (8% NaCl); RH flow 96%
- 300x300x100
- dumped into 3% NaCl; lots more cracking than above...
- pre-exp 2x2; 99%; 79.2/79.2/38.0; 0.57/0.61/0.80; diff lim > 2.0
- still diffracts pretty well. No real spot splitting as one might imagine given how damaged the crystal looks.

##### Diffraction exp_2613
- same xtal as exp_2612
- pre-exp 5x5; 99%; 79.2/79.1/38.0; 0.58/0.60/0.67; diff lim > 2.0

##### Diffraction exp_2614
- DJ.lyz.32.B6 (8% NaCl); RH flow 96%
- 300x200x150
- dumped into 3% NaCl; lots of cracking perp to c
- pre-exp 2x2; 99%; 79.1/79.1/37.9; 0.56/0.60/0.76; diff lim > 2.0

##### Diffraction exp_2615
- same xtal as exp_2614
- pre-exp 5x5; 99%; 79.1/79.1/38.0; 0.58/0.60/0.70; diff lim > 2.0

##### Diffraction exp_2616
- DJ.lyz.32.B6 (8% NaCl); RH flow 96%
- 300x200x150
- dumped into 2% NaCl; lots of cracking perp to c
- pre-exp 2x2; 79.1/79.1/38.0 0.57/0.61/0.70 diff lim > 2.0

##### Diffraction exp_2617
- same xtal as exp_2616
- pre-exp 5x5; 96%; 79.1/79.1/38.0 0.58/0.61/0.84; diff lim > 2.0


Interesting that these crystals, even though rather cracked, have relatively low mosaicities. 

I will try to pre-equil to high salt first, to get worse cracking and hopefully higher mosaicity. 

##### Diffraction exp_2616
- DJ.lyz.32.B6 (8% NaCl); RH flow 96%
- 300x200x150
- dumped into 12 % NaCl for 2', then to 3% NaCl for 2'; lots of cracking perp to c when going to 3%
- pre-exp 2x2; 95%; 79.2/79.1/38.0 0.56/0.59/0.69 diff lim > 2.0

2025-05-13. 

Looking at Lopez-Jaramillo et al, they saw modest mosaicity increases, and usually going from lower to higher salt. So I could try that. But I think I'll finish the measurements of 8%->3% and report whatever I find. The story appears to be something like 

"Although lysozyme crystals experience lots of cracking, the mosaicitiy isn't affected enough to have a large impact on the data quality. For alpha-lactalbumin, however, the cracking prevents collection of good data, and even getting a unit cell in some cases."

##### Diffraction exp_2619
- DJ.lyz.32.C6 (8% NaCl); RH flow 97%
- 300x300x100
- dumped into 3% NaCl; lots of cracking perp to c
- pre-exp 2x2; 97%; 79.2/79.2/38.0; 0.56/0.61/0.77; diff lim > 2.0

##### Diffraction exp_2620
- same xtal as 2619
- pre-exp 5x5; 98%; 79.1/79.1/38.0; 0.56/0.56/0.67; diff lim > 2.0

##### Diffraction exp_2621
- DJ.lyz.32.C6 (8% NaCl); RH flow 97%
- 400x400x100
- dumped into 3% NaCl; lots of cracking perp to c
- pre-exp 2x2; 81%; 79.1/79.1/37.9; 0.56/0.58/0.86; diff lim > 2.0

##### Diffraction exp_2622
- same xtal as 2621
- pre-exp 5x5; 97%; 79.2/79.2/38.0; 0.59/0.59/0.81; diff lim > 2.0

##### Diffraction exp_2623
- same xtal as 2621
- pre-exp 5x5; 90%; 79.2/79.2/37.9; 0.56/0.61/0.76; diff lim > 2.0

Dumps into 3% NaCl

exp # 	| size 			| cell 				| 2x2 mosaicity 	| 5x5 mosaicity	 |
------	|--------------	|------------------	|---------------	|----------------|
2612/13	| 300x300x100	| 79.2/79.2/38.0	| 0.57/0.61/0.80 	| 0.58/0.60/0.67 |
2614/15	| 300x300x150	| 79.1/79.1/37.9 	| 0.56/0.60/0.76 	| 0.58/0.60/0.70 |
2619/20	| 300x300x100   | 79.2/79.2/38.0	| 0.56/0.61/0.77    | 0.58/0.60/0.67 |
2621/22	| 400x400x100	| 79.2/79.2/38.0	| 0.56/0.58/0.86	| 0.59/0.59/0.81



Now 15 minute gradient equilibration to 3% NaCl
These crystals don't have the same cracks as dumping, but do look a little ragged.

##### Diffraction exp_2625
- DJ.lyz.32.C6
- 400x300x100
- 15' gradient equil to 3% NaCl
- 96.8% RH 8 LPM
- pre-exp 2x2; 72%; 79.2/79.1/38.0; 0.58/0.58/0.77; diff lim > 2.0

##### Diffraction exp_2626
- DJ.lyz.32.C6
- 300x300x150
- 15' gradient equil to 3% NaCl
- 96.8% RH 8 LPM
- pre-exp 2x2; 98%; 79.1/79.1/38.0; 0.58/0.59/0.79; diff lim > 2.0

##### Diffraction exp_2627
- DJ.lyz.32.C6
- 300x300x200
- 15' gradient equil to 3% NaCl
- 96.8% RH 8 LPM
- pre-exp 2x2; 96%; 79.1/79.1/38.0; 0.58/0.61/0.78; diff lim > 2.0

##### Diffraction exp_2628
- DJ.lyz.32.C6
- 300x300x300
- 15' gradient equil to 3% NaCl
- 96.8% RH 8 LPM
- pre-exp 2x2; 95%; 79.1/79.1/38.0; 0.58/0.60/0.74; diff lim > 2.0

15' gradient equil 3% NaCl

exp # 	| size 			| cell 				| 2x2 mosaicity 	| 
------	|--------------	|------------------	|---------------	|
2625	| 400x300x100	| 79.2/79.1/38.0	| 0.58/0.58/0.77 	| 
2626	| 300x300x150	| 79.1/79.1/37.9 	| 0.56/0.59/0.79 	| 
2627	| 300x300x200   | 79.1/79.1/38.0	| 0.56/0.61/0.78    | 
2628	| 300x400x300	| 79.1/79.1/38.0	| 0.56/0.60/0.74	| 

Now 40 minute gradient equilibration to 3% NaCl
These crystals don't have the same cracks as dumping but are showing some surface degradation.

##### Diffraction exp_2629
- DJ.lyz.32.C6
- 300x300x200
- 40' gradient equil to 3% NaCl
- 96.8% RH 8 LPM
- pre-exp 2x2; 98%; 79.2/79.1/38.0; 0.56/0.59/0.73; diff lim > 2.0

##### Diffraction exp_2630
- DJ.lyz.32.C6
- 300x300x200
- 40' gradient equil to 3% NaCl
- 96.8% RH 8 LPM
- pre-exp 2x2; 98%; 79.2/79.1/38.0; 0.56/0.61/0.75; diff lim > 2.0

##### Diffraction exp_2631
- DJ.lyz.32.C6
- 200x200x100
- 40' gradient equil to 3% NaCl
- 96.8% RH 8 LPM
- pre-exp 2x2; 97%; 79.2/79.1/38.0; 0.56/0.59/0.79; diff lim > 2.0

##### Diffraction exp_2633
- DJ.lyz.32.C6
- 300x300x300
- 40' gradient equil to 3% NaCl
- 96.8% RH 8 LPM
- pre-exp 2x2; 95%; 79.1/79.1/38.0; 0.57/0.61/0.82; diff lim > 2.0


40' gradient equil 3% NaCl

exp # 	| size 			| cell 				| 2x2 mosaicity 	|
------	|--------------	|------------------	|---------------	|
2629	| 300x300x200	| 79.2/79.1/38.0	| 0.56/0.59/0.73 	|
2630	| 300x300x200	| 79.2/79.1/37.9 	| 0.56/0.61/0.75 	|
2631	| 200x200x100   | 79.2/79.1/38.0	| 0.56/0.61/0.79    |
2632	| 300x300x100	| 79.2/79.2/38.0	| 0.56/0.58/0.82	|
2633	| 300x300x100	| 79.2/79.2/38.0	| 0.56/0.61/0.76	|


Now mount some directly from well (8% NaCl)

##### Diffraction exp_2634
- DJ.lyz.32.C6 (8% NaCl)
- 300x300x200
- direct from well
- mount was rather dry from blotting...
- 96.8% RH 8 LPM
- pre-exp 2x2; 95%; 79.2/79.2/38.0; 0.56/0.61/0.80; diff lim > 2.0

##### Diffraction exp_2635
- DJ.lyz.32.C6 (8% NaCl)
- 300x300x200
- direct from well
- 96.8% RH 8 LPM
- pre-exp 2x2; 88%; 79.2/79.2/38.0; 0.56/0.59/0.80; diff lim > 2.0

##### Diffraction exp_2636
- DJ.lyz.32.C6 (8% NaCl)
- 350x350x150
- direct from well
- 96.8% RH 8 LPM
- pre-exp 2x2; 88%; 79.2/79.2/38.0; 0.56/0.61/0.76; diff lim > 2.0

##### Diffraction exp_2637
- DJ.lyz.32.D6 (8% NaCl)
- 250x250x150
- direct from well - from liquid-vapor surface
- 96.8% RH 8 LPM
- pre-exp 2x2; 88%; 79.2/79.2/37.9; 0.56/0.59/0.71; diff lim > 2.0
** Note - all (most) of the other crystals had to be released from the plastic surface of the well. This one was growing on the liquid-vapor interface and was just lifted off - so maybe less trauma.**

##### Diffraction exp_2638
- DJ.lyz.32.D6 (8% NaCl)
- 250x250x150
- direct from well - released from plastic easily
- 96.8% RH 8 LPM
- pre-exp 2x2; 88%; 79.1/79.2/37.9; 0.56/0.60/0.71; diff lim > 2.0

##### Diffraction exp_2639
- DJ.lyz.32.D6 (8% NaCl)
- 300x300x150
- direct from well
- 96.8% RH 8 LPM
- pre-exp 2x2; 88%; 79.2/79.2/37.9; 0.56/0.61/0.78; diff lim > 2.0
** This one was kind of a tough mount. Released from plastic & then chased around.**

##### Diffraction exp_2640
- DJ.lyz.32.D6 (8% NaCl)
- 250x250x150
- direct from well - from liquid-vapor surface
- 96.8% RH 8 LPM
- pre-exp 2x2; 88%; 79.1/79.2/37.9; 0.55/0.59/0.76; diff lim > 2.0


direct from well (8% NaCl)

exp # 	| size 			| cell 				| 2x2 mosaicity 	|
------	|--------------	|------------------	|---------------	|
2634	| 300x300x200	| 79.2/79.2/38.0	| 0.56/0.61/0.80 	|
2635	| 300x300x200	| 79.2/79.2/37.9 	| 0.56/0.59/0.80 	|
2636	| 350x350x150   | 79.2/79.1/37.9	| 0.56/0.61/0.76    |
2637	| 250x250x150	| 79.1/79.2/37.9	| 0.56/0.59/0.71	|
2638	| 250x250x100	| 79.2/79.2/37.9	| 0.56/0.60/0.71	|
2639	| 300x300x150	| 79.2/79.2/37.9	| 0.56/0.61/0.78	|
2640	| 250x250x150	| 79.1/79.2/37.9	| 0.55/0.59/0.76	|

Direct from well (3% NaCl)

##### Diffraction exp_2641
- DJ.lyz.32.A1 (3% NaCl)
- 350x350x350
- direct from well - from liquid-vapor surface
- 96.8% RH 8 LPM
- pre-exp 2x2; 88%; 79.1/79.2/38.0; 0.56/0.62/0.81; diff lim > 2.0

##### Diffraction exp_2642
- DJ.lyz.32.A1 (3% NaCl)
- 350x350x350
- direct from well - from liquid-vapor surface
- 96.8% RH 8 LPM
- pre-exp 2x2; 91%; 79.2/79.1/38.0; 0.64/0.64/1.07; diff lim > 2.0

Whoa. Maybe the humidity is too low? Try heating up the water to get higher humidity. 

2025-05-14.
Now I will collect some full data sets for different soaking protocols.

#### Full data sets for lysozyme

##### Dumped into 3% NaCl
###### Diffraction exp_2643
- DJ.lyz.32.D6 (8% NaCl)
- dumped into 3% NaCl & soak for 3'
- some cracking (there may have already been some cracks...)
- pre 2x2 with target at 2.0 A
- 79.2/79.2/38.0 | 0.67/0.62/0.91

###### Diffraction exp_2644
- same xtal as 2643
- pre 2x2 with target at 1.5 A
- 79.1/79.2/38.0 | 0.64/0.60/0.91
- collect full ds with dphi=0.5, dt=20"
- 79.3/79.3/38.0 | 0.61/0.61/0.91 | I/sigma = 0.9 @ 1.5

##### Diffraction exp_2647
- DJ.lyz.31.B6 (8% NaCl)
- dumped into 3% NaCl
- 300x300x150
- pre 2x2: 97% 79.2/79.2/38.0 | 0.56/0.58/0.66
- collect full ds with dphi=0.5,dt=20"
- 79.19/79.19/37.94 | 0.60/0.60/0.57 | I/sigma=1.6 @ 1.5

##### Direct from well
###### Diffraction exp_2645
- DJ.lyz.32.D6 (8% NaCl)
- direct from well to 97% RH
- pre 2x2: 93% 79.1/79.2/37.9 | 0.56/0.59/0.83
- collect full ds with dphi=0.5,dt=20"
- 79.1/79.2/37.9 | 0.62/0.61/0.80 | I/sigma = 0.8 @ 1.5

###### Diffraction exp_2648
- DJ.lyz.31.B6 (8% NaCl)
- direct from well to 97% RH
- pre 2x2: 98% 79.1/79.2/37.9 | 0.55/0.59/0.80
- collect full ds with dphi=0.5,dt=20"
- 79.2/79.2/38.0 (but distance is large) | 0.59/0.58/0.56 | I/sigma = 1.0 @ 1.5

##### 15' gradient equil
Crystals were equilibrated to 3% NaCl/20 mM NaOAc 5.2/5 mg/mL lysozyme using auto_gradient system

##### Diffraction exp_2646
- DJ.lyz.31.B6 (8% NaCl)
- grad equiled as described above
- 300x300x150
- pre 2x2 95% 79.2/79.1/38.1 | 0.58/0.61/0.85
- collect full ds with dphi=0.5,dt=20"
- 79.1/79.2/38.0 | 0.62/0.61/0.61 | I/sigma=1.2 @ 1.5

#### 40' gradient equil

##### Diffraction exp_2649
- DJ.lyz.31.B6 (8% NaCl)
- grad equiled as described above, but 40'
- 350x350x150; might have a 'bad' quadrant
- pre 2x2 93% 79.2/79.1/38.0 | 0.56/0.61/0.77
- collect full ds with dphi=0.5,dt=20"

2025-05-15.

### alpha-lactalbumin again

direct from well (8% NaCl)

|exp # 	| equil |	size 			| cell 				| mosaicity 	|	2x2 mosaicity	|
|-------|-------|------------------	|------------------	|---------------|-------------------|


| 2653	|	0	|	800x450x200		| 72.0/104.7/117.8	| 0.71/0.58/0.86| 0.59/0.56/0.61	| 
| 2650	| 	5	|	400x400x200		| 72.2/105.0/118.1	| 0.62/0.60/0.80| 0.63/0.61/0.94	|
| 2657 	|	5	|	400x250x100		| 72.2/104.9/117.8	| 0.69/0.55/1.61| 0.74/0.62/1.22	|
| 2658 	|	5	|	350x250x100		| 72.3/105.1/118.0 	| 0.58/0.54/0.93| 0.56/0.58/0.75	|
| 2651	|	15	|	550x350x150		| 72.2/105.0/118.1	| 0.61/0.57/0.65| 0.57/0.58/0.77	|
| 2659	|	15	|	350x350x150		| 72.2/104.9/118.1	| 0.59/0.59/0.64| 0.58/0.59/0.69	|
| 2661	|	15	|	600x300x100		| 72.3/105.0/118.0 	| 0.58/0.55/0.60| 0.59/0.59/0.70	|
| 2652	|	45	|	900x400x200		| 72.3/105.1/118.2	| 0.60/0.59/0.58| 0.60/0.60/0.71	|
| 2662	|	45	|	700x500x200		| 72.3/105.1/118.2  | 0.60/0.60/0.62| 0.61/0.61/0.73	|
| 2664 	|	45	|	450x350x150		| 72.3/105.0/118.1 	| 0.59/0.57/0.61| 0.57/0.59/0.70 	|
| 2654	|	-	|	300x400x100		| 72.3/104.7/117.3	| 0.61/0.57/0.55| 0.59/0.59/0.91	|
| 2656	|	-	|	400x350x150		| 71.5/104.5/117.3	| 0.60/0.59/0.61| 0.59/0.59/0.92	|
 

5 minute gradient equilibration to ML with auto-gradient system
ML as above: 20% P8K, 50 mM KH2PO4, 25% glycerol

##### Diffraction exp_2650
- alact.18.D6
- grad equiled over 5' to ML; resulted in a couple long cracks, roughly perpendicular to each other; in both cases the crack extended through the thickness (200 micron dimension); brief transfer to ML
- 400x400x200
- 92% RH
- pre 2x2 97% 72.3/105.0/118.0 | 0.63/0.61/0.94
- collect full ds with dphi=0.5, dt=30"
	- 72.2/105.0/118.1 | 0.62/0.60/0.80 | I/sigma=0.8 @ 2.16

##### Diffraction exp_2657
- alact.18.D6
- 5 min grad equil to ML; substantial cracking...
- 400x250x100
- 92% RH
- pre 2x2 40% 72.3/105.1/117.9 | 0.74/0.62/1.22
- collect partial ds (2x25) with dphi=0.5, dt=30"
	- 95% 72.2/104.9/117.8 | 0.69/0.55/1.61
	
##### Diffraction exp_2658
- alact.18.D6
- 5 min grad equil to ML; substantial cracking...
- 350x250x100
- 92% RH
- pre 2x2 40% 72.2/104.9/117.9 | 0.56/0.58/0.75
- collect partial ds (2x25) with dphi=0.5, dt=30"
	- 72.3/105.1/118.0	| 0.58/0.54/0.93 (2x25)
	- 71.3/104.6/118.2  | 0.59/0.54/1.05 (1x25)
	
15' gradient equilibration to ML

##### Diffraction exp_2651
- alact.18.D6
- grad equiled over 15' to ML; possibly on small surface crack - although this might have been there from harvesting/breaking off a smaller chunk; brief transfer to ML
- 550x350x150
- 92% RH
- pre 2x2 97% 72.3/105.0/118.2 | 0.57/0.58/0.77
- collect full ds with dphi=0.5, dt=30"
	- 72.2/105.0/118.1 | 0.61/0.57/0.65 | I/sigma=0.8 @ 2.16

##### Diffraction exp_2659
- alact.20.D5
- 15 min grad equil to ML;
- 350x350x150 no cracking
- 92% RH 7 LPM
- pre 2x2 95% 72.3/105.1/118.0 | 0.58/0.59/0.69
- collect partial ds (2x25) with dphi=0.5, dt=30"
	- 98% 72.2/104.9/118.1 | 0.59/0.59/0.64
	
##### Diffraction exp_2661
- alact.20.D5
- 15 min grad equil to ML; no cracks
- 600x300x100 no cracking
- 92% RH
- pre 2x2 96% 72.2/104.9/118.0 | 0.59/0.59/0.70
- collect partial ds (2x25) with dphi=0.5, dt=30"
	- 72.3/105.0/118.0 | 0.58/0.55/0.60


45' gradient equilibration to ML

##### Diffraction exp_2652
- alact.18.D5
- grad equiled over 45' to ML; no cracking; brief transfer to ML
- 900x400x200
- 92% RH 8 LPM
- pre 2x2: 97% 72.3/105.0/118.1 | 0.60/0.60/0.71
- collect full ds with dphi=0.5, dt=30"
	- 72.3/105.1/118.2 | 0.60/0.59/0.58 | I/sigma=1.2 @ 2.16

##### Diffraction exp_2662
- alact.21.D4-6
- grad equiled over 45' to ML; no cracking; brief transfer to ML
- 700x500x200
- 92% RH 8 LPM
- pre 2x2: 97% 72.3/105.0/118.1 0.61/0.61/0.73
- collect partial ds (2x25) with dphi=0.5, dt=30"
	- 72.3/105.1/118.2 | 0.60/0.60/0.62

##### Diffraction exp_2664
- alact.21.D4-6
- grad equiled over 45' to ML; no cracking; brief transfer to ML
- 450x350x150
- 92% RH 8 LPM
- pre 2x2: 96% 72.3/105.0/118.1 | 0.57/0.59/0.70 
- collect partial ds (2x25) with dphi=0.5, dt=30"
	- 72.3/105.0/118.1 | 0.59/0.57/0.61

dumping into ML

##### Diffraction exp_2653
- alact.18.D5
- dump into ML; lots of cracking (photo taken)
- 800x450x200
- 92% RH 8 LPM
- pretty poor diffraction, but can get a cell
- pre 2x2: 62% 72.2/105.0/117.8 | 0.59/0.56/0.61
- collect full ds with dphi=0.5, dt=30"
	- 72.0/104.7/117.8 | 0.71/0.58/0.86 | I/sigma = 0.99 @ 2.55

##### Diffraction exp_2653
- alact.21.D5
- dump into ML; lots of cracking (photo taken)
- 400x250x100
- 92% RH 8 LPM
- pretty poor diffraction, but can get a cell
- pre 2x2: 62% 72.1/105.6/118.1 | 1.06/0.60/1.18
- collect partial ds (2x25) with dphi=0.5, dt=30"
	- 

2025-05-16. 
Negative control - direct from well

##### Diffraction exp_2654
- alact.18.D5
- mount directly from well (micromesh)
- 300x400x100
- 98% RH
- 2x2 pre: 96% 71.8/104.3/117.1 | 0.59/0.59/0.91
- collect full ds with dphi=0.5, dt=30"
	- something happens after a while - around frame 60
	- at end crystal is dry (probably started drying out at fram 60)
	- e3 mosaicity starts rising about frame 40
	- overall: 0.95/0.61/1.86
	- frames 1-40: 72.3/104.7/117.3 | 0.61/0.57/0.55

##### Diffraction exp_2655
- alact.18.D5
- mount directly from well (micromesh) into microRT tube against water
- 500x200x150
- microRT tube against water
- 2x2 pre: 71.9/104.4/117.2 | 0.58/0.58/0.84
- collect full ds with dphi=0.5, dt=30"
	- 99% 71.6/104.4/117.2 | 0.62/0.60/0.79

##### Diffraction exp_2656
- alact.18.D5
- mount directly from well in to RH flow 98.5%
- 400x350x150
- 98.5-99% RH
- 2x2 pre: 97% 71.6/104.2/116.9 | 0.59/0.59/0.92
- collect full ds with dphi=0.5, dt=30"
	- 71.5/104.5/117.3 | 0.60/0.59/0.61		
- added on to this after complete. Still did pretty good --> Waiting for RH to get up there paid off...

2025-05-17. 

Overnight the RH got to 99%, and this morning would go up to 99.1. I had increase the temperature offset of the water to 5.5 degrees. 

Now to get more data points for lactalbumin. Here instead of collecting full datasets, I will collect 2x25 frames.

