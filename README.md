![Cover Image](https://raw.githubusercontent.com/ai03-2725/MX_V2/master/Resources/Cover.jpg) 
# MX_V2
Second generation KiCad Libraries of keyboard switch footprints  

<!-- ![Footprint Image](https://raw.githubusercontent.com/ai03-2725/MX_Alps_Hybrid.pretty/master/Screenshots/Footprint.png)   -->
6 years after the creation of [the original MX_Alps_Hybrid library](https://github.com/ai03-2725/MX_Alps_Hybrid), this library has been created as a successor and replacement.


## Features
* Designed from scratch using official datasheets and accurate measurements
* Almost every switch size in existence
* Topside soldermask to prevent solder overflow and improve appearance
* Various keysizes for all occasions
* Keysizes are generated via the script generate.py from a single footprint, making the library extensible and maintainable
* (Will be) used for production PCBs and battle-tested in the real world

## Included Footprint Libraries
* **MX_Solderable.pretty** - For Cherry MX type switches.
* **MX_Hotswap.pretty** - For Cherry MX type switches via hotswap sockets.
* **Alps_Solderable.pretty** - For alps SKCM/SKCL, SKBM/SKBL, and clones with same pin structure.  
* **MX_Alps_Hybrid.pretty** - Hybrid MX/Alps compatible solderable footprints.
* **Switch_Misc.pretty** - Misc footprints such as LED footprints.
* Template.pretty - The template footprints that the script uses to generate footprints automatically. Do not use in production.

### Footprint Variants
* -ReversedStabilizers - Reversed stabilizer direction (north- vs south-facing).

### Misc Parts Variants
* -LED - LEDs that align to each switch footprint. Prefix denotes which type of switch they are applicable to.
* -Reversed - Inverts pin 1 order (left vs right square pad).
* -PolarityMarked - Marks pin 1 with a + icon to denote positive polarity (only useful if pin 1 is the higher voltage).


## Contributing
Verbal "Please create this" will usually be declined due to lack of time available for maintenance.  
Massive overhauls that completely change the structure of the library or code will be declined if made without prior discussion.  
When creating PRs, please verify the following:  
* A template footprint is created in Template.pretty if creating a new family type, with the file modified to have "Template" for all script-replaced unit/variant text.  
* Code modifications are done in a sane, clean manner.
* Footprints are made from datasheets, empirical testing, and/or reasonable expectations.
* All footprints in a switch library (i.e. not a one-off LED footprint or similar) are generated from the script and are not manually modified.

### Todo
* Script: Make ISO outlines scale by unit width/height parameters
* Add screenshots of 3D model, footprint
* Create useful schema symbols