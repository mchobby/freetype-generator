#!/bin/bash

# Script for generating MicroPython font files from TrueType fonts using ft-generate.py

# Define the full and minimal character sets
FULL_CHARSET="#32-#125,#160-#255"
MINIMAL_CHARSET="#32-#125,#160-#163,#166-#169,#171,#173,#175,#176-#177,#180,#187,#224,#231-#234"

# Function to generate MicroPython font files
generate_font() {
    python3 ft-generate.py "$1" "$2" "$3" "$4" --descender="$5" --special-align="$6" --chars="$7"
}

# Generate MicroPython font files for Heydings Icons font
generate_font "ttf-fonts/heydings_icons.ttf" 23 "upy-fonts/heyd_23.py" "Heydings_23" "" "" "#33,#42-#43,#45,#49-#54,#56,#64-#90,#97-#105,#107-#119,#121"

# Generate MicroPython font files for Entypo font
generate_font "ttf-fonts/Entypo.otf" 23 "upy-fonts/etypo_13.py" "Entypo_13" "" "" "#33-#126,#174,#196-#197,#199,#201,#209,#214,#220,#224-#229,#231-#239,#241-#244,#246"
generate_font "ttf-fonts/Entypo.otf" 42 "upy-fonts/etypo_23.py" "Entypo_23" "" "" "#33-#126,#174,#196-#197,#199,#201,#209,#214,#220,#224-#229,#231-#239,#241-#244,#246"

# Generate MicroPython font files for Arrows font
generate_font "ttf-fonts/Arrows.ttf" 24 "upy-fonts/arrows_15.py" "Arrows_15" "" "#65:M,#66:M,#73:M,#74:M,#81:M,#82:M,#83:M,#84:M,#85:M,#86:M,#87:M,#88:M,#97:M,#98:M" "#65-#90,#97-#122"
generate_font "ttf-fonts/Arrows.ttf" 36 "upy-fonts/arrows_23.py" "Arrows_23" "" "#65:M,#66:M,#73:M,#74:M,#81:M,#82:M,#83:M,#84:M,#85:M,#86:M,#87:M,#88:M,#97:M,#98:M" "#65-#90,#97-#122"

# Generate MicroPython font files for Vera font
for size in 8 9 10 14 23; do
    generate_font "ttf-fonts/Vera.ttf" "$size" "upy-fonts/vera_$size.py" "Vera_$size" "" "" "$FULL_CHARSET"
done

# Generate MicroPython font files for minimal Vera font
for size in 8 9 10 14 23; do
    generate_font "ttf-fonts/Vera.ttf" "$size" "upy-fonts/vera_m$size.py" "Vera_m$size" "" "" "$MINIMAL_CHARSET"
done

# Generate MicroPython font files for VeraMono font
for size in 9 10 15 23; do
    generate_font "ttf-fonts/VeraMono.ttf" "$size" "upy-fonts/veram_$size.py" "VeraMono_$size" "" "" "$FULL_CHARSET"
done

# Generate MicroPython font files for minimal VeraMono font
for size in 9 10 15 23; do
    generate_font "ttf-fonts/VeraMono.ttf" "$size" "upy-fonts/veram_m$size.py" "VeraMono_m$size" "" "" "$MINIMAL_CHARSET"
done

# Generate MicroPython font files for Roboto-Light font
for size in 8 10 12 15 20; do
    generate_font "ttf-fonts/Roboto-Light.ttf" "$size" "upy-fonts/robotl_m$size.py" "RobotoLight_m$size" "" "" "$MINIMAL_CHARSET"
done

# Generate MicroPython font files for DejaVuSansMono font
for size in 8 10 12 15 20; do
    generate_font "ttf-fonts/DejaVuSansMono.ttf" "$size" "upy-fonts/dejav_m$size.py" "dejav_m$size" "" "" "$MINIMAL_CHARSET"
done

# Generate MicroPython font files for FreeSerif font
for size in 10 12 15 20; do
    generate_font "ttf-fonts/FreeSerif-4aeK.ttf" "$size" "upy-fonts/fserif_m$size.py" "fserif_m$size" "" "" "$MINIMAL_CHARSET"
done

# Generate MicroPython font files for PitchDisplayRegularDemo font
generate_font "ttf-fonts/PitchDisplayRegularDemo.ttf" 14 "upy-fonts/pitch_15.py" "Pitch_15" "" "" "$FULL_CHARSET"
generate_font "ttf-fonts/PitchDisplayRegularDemo.ttf" 22 "upy-fonts/pitch_23.py" "Pitch_23" "" "" "$FULL_CHARSET"

# Generate MicroPython font files for minimal PitchDisplayRegularDemo font
generate_font "ttf-fonts/PitchDisplayRegularDemo.ttf" 14 "upy-fonts/pitch_m15.py" "Pitch_m15" "" "" "$MINIMAL_CHARSET"
generate_font "ttf-fonts/PitchDisplayRegularDemo.ttf" 22 "upy-fonts/pitch_m23.py" "Pitch_m23" "" "" "$MINIMAL_CHARSET"

