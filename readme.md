# FreeType generator

FreeType generator is Python 3 Font generator for ILI9341 TFT LCD Driver for MicroPython driver.

This project will load .ttf files and generates .py files that could be loaded on a MicroPython Pyboard.

The ILI9341 driver is developed by Roman Podgaiski (ropod7) and is available here at [https://github.com/ropod7/pyboard_drive](https://github.com/ropod7/pyboard_drive)

Some French technical information and wiring are available at MCHobby [http://wiki.mchobby.be/index.php?title=MicroPython-ILI9341](http://wiki.mchobby.be/index.php?title=MicroPython-ILI9341)

Notices:
* This software can generate any size (in pixel) font. The ILI9431 is limited to 23bits/pixels height font.
* Due to ILI9341 font coding, all fonts reaching a multiple of 8 pixels height (8 bits) are upsized of 8 bits.
** a 7 pixels height font is encoded inside a byte (8 bits) per column.
** a 8 pixels height font will be encoded on 16 bits per column (upsizing).  
** Fonts from 9 to 15 pixels height are encoded with 16 bits per column.    
** Fonts from 16 to 23 pixels hight are encoded with 24 bits per column.

When generating the values, the numeric values are masked with 0b1111111111 (mask having font_height_in_pixels+1 bits length). 

# Files

* __ttf-fonts/__ - This folder contains source font that will be transformed 
* __ili-fonts/__ - This folder contains the microPython font file generated for the ILI9341 driver 
* __generate-all-font.sh__ - Use the ```ft-generate.py``` to generates all the ILI9341 inside ```ili-fonts/``` from FreeType font available in ```ttf-font/```
* __ft-generator.py__ - script with arguments generating ILI-driver fonts (see the .sh file for sample, please read the ili-fonts.md for more information on applicable naming conventions).
* __ft-view.py__ - debugging tool. Allow to view a character bitmap encoding (or the whole font set). __calculate the max size (height,width) of the font__.
* __ft-view-encoded.py__ - same as ft-view.py but also showing the encoded data (useful for bug tracking)


# Install instructions

If you want to run the ft-generator.py then you will need the following dependencies.

```
pip3 install freetype-py
pip3 install docopt
```

## FreeType library installation
FreeType library should be available aout-of-the box on most of the Linux systems (As Linux Mint, Ubuntu and Debian).

For windows, you will certainly run into a '''dll nightmare'''. Finding the good DLL version properly compiled for win32/win64 was a lonnnnnnggggg path to go. 

Here some path to find the good Windows DLL. Better use Linux!

```
*** DLL Nightmare on Windows ***
    
http://www.freetype.org/

Win32 installation can be found here
http://gnuwin32.sourceforge.net/packages/freetype.htm
```

# Resources

## FreeType
  
* [Monochrome font rendering with FreeType and Python](https://dbader.org/blog/monochrome-font-rendering-with-freetype-and-python)
* [FreeType GitHub project] (https://github.com/rougier/freetype-py)

## DocOpt - argument parser

La plus belle manière de parser les arguments de script en python

* [docopt.org](http://docopt.org)
* [La plus belle maniere de parser les arguments de script en python](http://sametmax.com/la-plus-belle-maniere-de-parser-les-arguments-de-script-en-python/) sur Sam-et-Max (attention, gros écarts de langage).

## About font 
* [A Crash Course in Typography: The Basics of Type](http://www.noupe.com/essentials/icons-fonts/a-crash-course-in-typography-the-basics-of-type.html) noupe.com
* [Font Kerning](https://en.wikipedia.org/wiki/Kerning) Wikipedia
* [Glyph Metrics](http://www.freetype.org/freetype2/docs/tutorial/step2.html) Freetype.org

