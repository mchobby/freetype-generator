#!/usr/bin/env python3
# coding: utf8                

help = """FreeType View - get a FreeType font file and display it's bitmap representation (for all characters or a single char).
This script is useful to get font sizing (in pixels) and its representation (under bitmap format).  
 
Usage:
  ft-view.py <ttf_file> <ttf_size> [--char=<char>]
 
Options:
  -h --help          This helps screen

Examples:
  python3 ft-view.py ttf-fonts/Vera.ttf 13           --> Will displays all the characters
  python3 ft-view.py ttf-fonts/Vera.ttf 13 --char=A  --> Display only the char "A"


Happy Electronic Hacking. 
MCHobby.be
""" 

# FreeType generator common items
from ftcommon import *
from docopt import docopt
import sys

if __name__ == '__main__':
    arguments = docopt( help )

    font_file = 'heydings_icons.ttf' # 'Vera.ttf' # 'VeraMono.ttf' #'Vera.ttf' #  'heydings_icons.ttf' #
    font_size = 23 # 20
    char_filter = arguments['--char'] # eg: 'B' or None
    
    print( "Load font %s, set size to %i" % (arguments['<ttf_file>'], int(arguments['<ttf_size>'])) )             
    font_loader = FreeTypeLoader( font_file=arguments['<ttf_file>'], font_size=int(arguments['<ttf_size>']) )
    print( "max size (width,height): %i,%i" %(font_loader.max_width, font_loader.max_height ) )

    for ordinal in font_loader.characters.keys():
        if (char_filter != None) and (ord(char_filter) != ordinal ):
            continue

        # print the bitmap representation of a character
        #   include separator & dimension 
        font_loader.print_character( ordinal )



