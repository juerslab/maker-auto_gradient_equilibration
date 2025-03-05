// Holder for samples for auto_gradient system. Intended to hold a pcr tube cap. 
// Doug Juers 2025 Version 2.0c
// Can be printed without supports.

$fa=1;
$fs=.5;
//
// Main tunable parameters:
tubing_diameter=1.5;// Adjust based on tubing diameter, so tubing can be inserted but is held in place by friction
pcrtube_thickness=.50;// Thickness of the walls of the pcr tube cap - impacts the positioning of the tubing guidance holes
coverslip_diameter=23.0;//Adjust depending on coverslip diameter
post_radius=5;// Adjust these to optimize fitting of the space
post_height=5;
//
// Other parameters
tolerance=0.01; //mm - to handle "z-fighting"
length=60;
width=40;
height=17;
extra_height=3; //Extra height at bottom of plate above surface. 15 is pretty big = ~ 200 µm crystals rather small
total_height=height+extra_height;
tubing_pillar_thickness=3.5;
window_diameter=18.6;
spacer_length=60-(17+10);
spacer_width=40;
spacer_height=17;

module whole(){
union(){
difference(){
    translate([tolerance/2,tolerance/2,tolerance/2])cube([length-tolerance,width-tolerance,total_height-tolerance]);//Overall starting cube
    translate([0,0,5+extra_height])cube([length,(width-tubing_pillar_thickness)/2,height]);//Remove left half top
    translate([0,width/2+tubing_pillar_thickness/2,5+extra_height])cube([length,(width-tubing_pillar_thickness)/2,height]);//Remove right half top
    translate([0,0,extra_height+5])cube([length-24,width,height]);//Remove half of top
    translate([length/2,width/2,0])cylinder(h=extra_height+5,d=window_diameter);//Round window for light from below
    translate([0,width/2-window_diameter/2,0])cube([length/2,window_diameter,extra_height+5]);//Expand window to horseshoe
    translate([length/2,width/2,1+extra_height])cylinder(h=8,d=coverslip_diameter);//For Coverslip
    translate([0,width/2-coverslip_diameter/2,1+extra_height])cube([length/2,coverslip_diameter,extra_height+5]);//Expand coverslip opening to horseshoe (for easy printing without supports)
    translate([length/2,width/2,1+extra_height])cylinder(h=1.5,d=26.0);//Recess to fit lip of pcr tube
    translate([length/2,width/2,1+extra_height+3])cylinder(h=5,d=26.5);//Recess so pcr tube extends above lip (otherwise surface tension can cause liquid to leak)

    translate([length/2+coverslip_diameter/2-tubing_diameter/2-pcrtube_thickness,width/2,extra_height+1])cylinder(h=100,d=tubing_diameter);//Tube holes
    translate([length/2+coverslip_diameter/2-tubing_diameter/2-pcrtube_thickness-2.2,width/2,extra_height+1])cylinder(h=100,d=tubing_diameter);
    difference(){//This removes a section just below the pcr tube to allow for light transmission
        translate([length/2,width/2,0])cylinder(h=extra_height+1+2*tolerance,d=24.0+2*tolerance);
        difference(){
            translate([length/2,width/2,0])cylinder(h=extra_height+1+tolerance,d=24.0+tolerance);
            translate([length-23,width/2-5,0])cube([length,10,extra_height+2]);
        }
    }
    translate([17+5,5,0])cylinder([post_radius+1,post_height+1]);//This creates holes on the bottom for the spacer (another file) to fit into
    translate([17+spacer_length-5,5,0])cylinder([post_radius+1,post_height+1]);
    translate([17+5,spacer_width-5,0])cylinder([post_radius+1,post_height+1]);
    translate([17+spacer_length-5,spacer_width-5,0])cylinder([post_radius+1,post_height+1]);  

cube([length/2-13,width,total_height]); //Reduce the overall length
translate([length-10,0,0])cube([length,width,total_height]);
//translate([0.7*length,0.25*width,0])cylinder(h=total_height,d=5);

    }

}
}
translate([0,0,length-10])rotate([0,90,0])whole();
