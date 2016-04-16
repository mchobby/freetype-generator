#!/usr/bin/env python3
# coding: utf8                

help = """FreeType View - get a FreeType font file and display it's bitmap representation (for all characters or a single char).
This script is useful to get font sizing (in pixels) and its representation (under bitmap format).  
 
Usage:
  ft-view.py <ttf_file> <ttf_size> [--char=<char>] [--descenders=<comma-separated-list>]
 
Options:
  -h --help          This helps screen
  --descenders       Allow to redefine the descender chars (eg: p,q,j,#35 ).
                     Defining an empty parameter would disable the descender space.

Examples:
  python3 ft-view.py ttf-fonts/Vera.ttf 13           --> Will displays all the characters
  python3 ft-view.py ttf-fonts/Vera.ttf 13 --char=A  --> Display only the char "A"
  python3 ft-view.py tft-fonts/heydings_icons.ttf 23 --char=A --descenders=   --> ignore all descenders

Happy Electronic Hacking. 
MCHobby.be
""" 

# FreeType generator common items
from ftcommon import *
from docopt import docopt
import sys

if __name__ == '__main__':
    arguments = docopt( help )

    char_filter = arguments['--char'] # eg: 'B' or None
    
    print( "Load font %s, set size to %i" % (arguments['<ttf_file>'], int(arguments['<ttf_size>'])) )             
    font_loader = FreeTypeLoader( font_file=arguments['<ttf_file>'], font_size=int(arguments['<ttf_size>']) )
    if arguments['--descenders'] != None: # redefine the default descenders
       font_loader.set_descenders( arguments['--descenders'] ) 

    print( "max size (width,height): %i,%i" %(font_loader.max_width, font_loader.max_height ) )
    print( 'descender size = %i' % font_loader.descender_size )


    for ordinal in font_loader.characters.keys():
        if (char_filter != None) and (ord(char_filter) != ordinal ):
            continue

        # print the bitmap representation of a character
        #   include separator & dimension 
        font_loader.print_character( ordinal )



