#!/usr/bin/env python3
# coding: utf8                

help = help = """FreeType View Encoded - get a FreeType font file and display it's bitmap AND python encoded format for the Pyboard's ILI9341 driver.
This script is quite useful for advanced debugging. 
 
Usage:
  ft-view.py <ttf_file> <ttf_size> --char=<char>
 
Options:
  -h --help          This helps screen

Examples:
  python3 ft-view-encoded.py ttf-fonts/Vera.ttf 13 --char=A  --> Display only the char "A"


Happy Electronic Hacking. 
MCHobby.be
""" 

# FreeType generator common items
from ftcommon import *
from docopt import docopt

if __name__ == '__main__':
    arguments = docopt( help )
    char_filter = arguments['--char'] # MANDATORY PARAMETER, eg: N  
    
    print( "Load font %s, set size to %i" % (arguments['<ttf_file>'], int(arguments['<ttf_size>'])) )             
    font_exporter = FreeTypeExporter( font_file=arguments['<ttf_file>'], font_size=int(arguments['<ttf_size>']) )
    print( "max size (width,height): %i,%i" %(font_exporter.max_width, font_exporter.max_height ) )

    for ordinal in font_exporter.characters.keys():
        if (char_filter != None) and (ord(char_filter) != ordinal ):
            continue

        # print the bitmap representation of a character
        #   include separator & dimension 
        font_exporter.print_character( ordinal )

        encoded_list=font_exporter.encode_this( ordinal )
        print( 'Encoded char: %s ' % encoded_list )
        print( '--- Binary representation for %s ---' % chr(ordinal) )
        for value in encoded_list:
            print( bin(value) ) 

        print( '--- user friendly binary representation for %s ---' % chr(ordinal) )
        for value in encoded_list:
            s = bin(value)
            print( s.replace('0b','').replace( '0', '.').replace( '1', '*' ) )
 



