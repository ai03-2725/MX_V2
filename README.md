![Cover Image](https://github.com/ai03-2725/MX_V2/raw/main/Resources/Cover.jpg) 
# MX_V2
Second generation KiCad Libraries of keyboard switch footprints  
  
  
<!-- ![Footprint Image](https://raw.githubusercontent.com/ai03-2725/MX_Alps_Hybrid.pretty/master/Screenshots/Footprint.png)   -->
Designed as the successor to [the original MX_Alps_Hybrid library](https://github.com/ai03-2725/MX_Alps_Hybrid), with significantly improved sustainability and modularity.  
Unlike the original monolithic library, this new library separates switch types and components (LEDs and similar) as much as possible for simpler schematics, and is intended to be used with default KiCad symbols (such as `SW_Push`).


## Features
* Designed from scratch using official datasheets and accurate measurements
* Almost every switch size in existence
* Topside soldermask to prevent solder overflow and improve appearance
* Various keysizes for all occasions
* Keysizes are generated via the script generate.py from a single footprint, making the library extensible and maintainable
* Intended for production use

## Included Footprint Libraries
* **MX_Solderable.pretty** - For Cherry MX type switches via soldered pads.
* **MX_Hotswap.pretty** - For Cherry MX type switches via hotswap sockets.
* **Alps_Solderable.pretty** - For alps SKCM/SKCL, SKBM/SKBL, and clones with same pin structure.  
* **MX_Alps_Hybrid.pretty** - Hybrid MX/Alps compatible solderable footprints.
* **Gateron_KS33_Solderable.pretty** - For Gateron Low Profile (V1.0 or V2.0, KS-27 or KS-33) switches via soldered pads.
* **Gateron_KS33_Hotswap.pretty** - For Gateron Low Profile (V1.0 or V2.0, KS-27 or KS-33) switches via hotswap sockets.
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
* Once everything is tested functional, add the line to generate the library folder for the footprint family automatically in `Generator/generate-all.sh`.


### Todo
* Script todos
  * Make ISO outlines scale by unit width/height parameters
  * Add stabilizer clearance keepout zones for Gateron KS33 footprints
* Ease of use
  * Add screenshots of 3D model, footprint



## Credits
* All authors and contributors to the [original V1 switch library](https://github.com/ai03-2725/MX_Alps_Hybrid)