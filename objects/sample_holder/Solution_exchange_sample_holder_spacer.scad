//Spacer for sample holder. Can be used to elevate sample holder, which increases the magniciation of the sample. Useful for smaller crystals. Can also be stacked.  
// Doug Juers 2025.
//
// Can be printed without supports.
//
$fa=1;
$fs=.5;
spacer_length=60-(17+10);
spacer_width=40;
spacer_height=10;
hole_radius=5;
post_radius=4;
post_height=5;
tolerance=0.01;
union(){
difference(){
    translate([tolerance/2,tolerance/2,tolerance/2])cube([spacer_length-tolerance,spacer_width-tolerance,spacer_height-tolerance]);
    translate([0,10,0,])cube([spacer_length-10,spacer_width-20,spacer_height]);// Remove central block
    //Make holes on bottom
    translate([5,5,0])cylinder([post_radius+1,post_height+1]);
    translate([spacer_length-5,5,0])cylinder([post_radius+1,post_height+1]);
    translate([5,spacer_width-5,0])cylinder([post_radius+1,post_height+1]);
    translate([spacer_length-5,spacer_width-5,0])cylinder([post_radius+1,post_height+1]);  
}  
    //Make posts on top
    translate([5,5,spacer_height])cylinder([post_radius,post_height]);
    translate([spacer_length-5,5,spacer_height])cylinder([post_radius,post_height]);
    translate([5,spacer_width-5,spacer_height])cylinder([post_radius,post_height]);
    translate([spacer_length-5,spacer_width-5,spacer_height])cylinder([post_radius,post_height]);
}
