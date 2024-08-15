#!/bin/bash

# MX
python ./Generator/generate.py -i ./Template.pretty/MX-Hotswap-Template.kicad_mod -o ./MX_Hotswap.pretty -t mx -n MX-Hotswap
python ./Generator/generate.py -i ./Template.pretty/MX-Solderable-Template.kicad_mod -o ./MX_Solderable.pretty -t mx -n MX-Solderable

# Alps SKCM/SKCL
python ./Generator/generate.py -i ./Template.pretty/Alps-Solderable.kicad_mod -o ./Alps_Solderable.pretty -t alps -n Alps-Solderable
python ./Generator/generate.py -i ./Template.pretty/Alps-Solderable.kicad_mod -o ./Alps_MX_Stabilizers.pretty -t alps_mx_stabilizers -n Alps-MX-Stabilizers

# MX-Alps Hybrid
python ./Generator/generate.py -i ./Template.pretty/MX-Alps-Hybrid-Template.kicad_mod -o ./MX_Alps_Hybrid.pretty -t mx_alps -n MX-Alps-Hybrid

# Gateron KS33 (Low Profile 2.0)
python ./Generator/generate.py -i ./Template.pretty/Gateron-KS33-Hotswap-Template.kicad_mod -o ./Gateron_KS33_Hotswap.pretty -t gateron_ks33 -n Gateron-KS33-Hotswap
python ./Generator/generate.py -i ./Template.pretty/Gateron-KS33-Solderable-Template.kicad_mod -o ./Gateron_KS33_Solderable.pretty -t gateron_ks33 -n Gateron-KS33-Solderable

# Kailh PG1353 (Choc V2)
python ./Generator/generate.py -i ./Template.pretty/Kailh-PG1353-Hotswap-Template.kicad_mod -o ./Kailh_PG1353_Hotswap.pretty -t kailh_pg1353 -n Kailh-PG1353-Hotswap
python ./Generator/generate.py -i ./Template.pretty/Kailh-PG1353-Solderable-Template.kicad_mod -o ./Kailh_PG1353_Solderable.pretty -t kailh_pg1353 -n Kailh-PG1353-Solderable
