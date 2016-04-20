#!/bin/bash

# Arguments are:
#   * FreeType font file to load (eg: Vera.ttf)
#   * FreeType font size to use  (eg: 23)
#   * Python filename to create  (eg: heyd_23.py) 
#   * Name of the object inside the created python filename (eg: Heydings_23)

python3 ft-generate.py ttf-fonts/heydings_icons.ttf 23 ili-fonts/heyd_23.py Heydings_23 --descender= --special-align=
python3 ft-generate.py ttf-fonts/Entypo.otf 23 ili-fonts/etypo_13.py Entypo_13 --descenders= --special-align=
python3 ft-generate.py ttf-fonts/Entypo.otf 42 ili-fonts/etypo_23.py Entypo_23 --descenders= --special-align=

python3 ft-generate.py ttf-fonts/Vera.ttf 10 ili-fonts/vera_10.py Vera_10
python3 ft-generate.py ttf-fonts/Vera.ttf 14 ili-fonts/vera_15.py Vera_15
python3 ft-generate.py ttf-fonts/Vera.ttf 23 ili-fonts/vera_23.py Vera_23

python3 ft-generate.py ttf-fonts/VeraMono.ttf 14 ili-fonts/veram_15.py VeraMono_15
python3 ft-generate.py ttf-fonts/VeraMono.ttf 23 ili-fonts/veram_23.py VeraMono_23

python3 ft-generate.py ttf-fonts/PitchDisplayRegularDemo.ttf 14 ili-fonts/pitch_15.py Pitch_15
python3 ft-generate.py ttf-fonts/PitchDisplayRegularDemo.ttf 22 ili-fonts/pitch_23.py Pitch_23

