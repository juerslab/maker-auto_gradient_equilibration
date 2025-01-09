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

