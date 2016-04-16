# Files 

This folder contains the generated font files. Files that can be loaded by the MicroPython Pyboard and used by the IL9341 Pyboard driver written by Ropod7 (see the project's readme.md for more details). 

## ili-fonts - Generation 1

Generation 1 of the driver use python file that can be loaded and parsed by the MicroPython Pyboard interpreter.
 
A font python file (eg: ```vera_14.py``) follows the following rules:
* Filename in lowercase, less than 8 caracters len. Using the .py extension.
* Filname ends with ```_<font_height_in_pixels>```. Allows you to identify the characters size on your TFT.
* File contains an objet "CamelCase" named also containing the font size in its name (eg: for the ```vera_14.py``` the object name declared in the file is ```Vera_14```) 

## ili-fonts - Generation 2

Generation 2 of the driver will work with binary data to spare RAM on the Pyboard.

__*-* Under construction *-*__

# Testing ili-fonts (generation 1)

Fonts are designed to run on micropython pyboard but you can test and evaluate then on your computer by using Python 3.

You can use the file ```ft-test.py``` which perform the routine as described here under.

Here a sample script that shows you how to do it:

```
>>> from vera_14 import Vera_14
>>> print( Vera_14[ ord('A')] )
(49152, 47104, 36608, 35008, 34848, 35008, 36608, 47104, 49152)

>>> for value in Vera_14[ ord('A') ]:
...     print( bin( value ) )
... 
0b1100000000000000
0b1011100000000000
0b1000111100000000
0b1000100011000000
0b1000100000100000
0b1000100011000000
0b1000111100000000
0b1011100000000000
0b1100000000000000

>>> for value in Vera_14[ ord('A') ]:
...     print( bin( value ).replace( '0b1', '   ').replace('1','*').replace('0',' ' ) )
... 
   *              
    ***           
      ****        
      *   **      
      *     *     
      *   **      
      ****        
    ***           
   *               

```

Notes:
* for encoding reason, the first bit (most significant one) must always be be set to 1. 
* All non used bits (on the left) are set to 1.
