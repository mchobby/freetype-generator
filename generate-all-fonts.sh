#!/bin/bash

# Arguments are:
#   * FreeType font file to load (eg: Vera.ttf)
#   * FreeType font size to use  (eg: 23)
#   * Python filename to create  (eg: heyd_23.py) 
#   * Name of the object inside the created python filename (eg: Heydings_23)

FULL_CHARSET=#32-#125,#160-#255
MINIMAL_CHARSET=#32-#125,#160-#163,#166-#169,#171,#173,#175,#176-#177,#180,#187,#224,#231-#234

python3 ft-generate.py ttf-fonts/heydings_icons.ttf 23 ili-fonts/heyd_23.py Heydings_23 --descender= --special-align= --chars=#33,#42-#43,#45,#49-#54,#56,#64-#90,#97-#105,#107-#119,#121
python3 ft-generate.py ttf-fonts/Entypo.otf 23 ili-fonts/etypo_13.py Entypo_13 --descenders= --special-align= --chars=#33-#126,#174,#196-#197,#199,#201,#209,#214,#220,#224-#229,#231-#239,#241-#244,#246
python3 ft-generate.py ttf-fonts/Entypo.otf 42 ili-fonts/etypo_23.py Entypo_23 --descenders= --special-align= --chars=#33-#126,#174,#196-#197,#199,#201,#209,#214,#220,#224-#229,#231-#239,#241-#244,#246

python3 ft-generate.py ttf-fonts/Vera.ttf 10 ili-fonts/vera_10.py Vera_10 --chars=$FULL_CHARSET
python3 ft-generate.py ttf-fonts/Vera.ttf 14 ili-fonts/vera_15.py Vera_15 --chars=$FULL_CHARSET
python3 ft-generate.py ttf-fonts/Vera.ttf 23 ili-fonts/vera_23.py Vera_23 --chars=$FULL_CHARSET

python3 ft-generate.py ttf-fonts/Vera.ttf 10 ili-fonts/vera_m10.py Vera_m10 --chars=$MINIMAL_CHARSET
python3 ft-generate.py ttf-fonts/Vera.ttf 14 ili-fonts/vera_m15.py Vera_m15 --chars=$MINIMAL_CHARSET
python3 ft-generate.py ttf-fonts/Vera.ttf 23 ili-fonts/vera_m23.py Vera_m23 --chars=$MINIMAL_CHARSET

python3 ft-generate.py ttf-fonts/VeraMono.ttf 14 ili-fonts/veram_15.py VeraMono_15 --chars=$FULL_CHARSET
python3 ft-generate.py ttf-fonts/VeraMono.ttf 23 ili-fonts/veram_23.py VeraMono_23 --chars=$FULL_CHARSET

python3 ft-generate.py ttf-fonts/VeraMono.ttf 14 ili-fonts/veram_m15.py VeraMono_m15 --chars=$MINIMAL_CHARSET
python3 ft-generate.py ttf-fonts/VeraMono.ttf 23 ili-fonts/veram_m23.py VeraMono_m23 --chars=$MINIMAL_CHARSET

python3 ft-generate.py ttf-fonts/PitchDisplayRegularDemo.ttf 14 ili-fonts/pitch_15.py Pitch_15 --chars=$FULL_CHARSET
python3 ft-generate.py ttf-fonts/PitchDisplayRegularDemo.ttf 22 ili-fonts/pitch_23.py Pitch_23 --chars=$FULL_CHARSET

python3 ft-generate.py ttf-fonts/PitchDisplayRegularDemo.ttf 14 ili-fonts/pitch_15.py Pitch_m15 --chars=$MINIMAL_CHARSET
python3 ft-generate.py ttf-fonts/PitchDisplayRegularDemo.ttf 22 ili-fonts/pitch_23.py Pitch_m23 --chars=$MINIMAL_CHARSET

