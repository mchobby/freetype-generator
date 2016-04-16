#!/usr/bin/env python3
# coding: utf8                

help = help = """FreeType View Encoded - get a FreeType font file and display it's bitmap AND python encoded format for the Pyboard's ILI9341 driver.
This script is quite useful for advanced debugging. 
 
Usage:
  ft-view.py <ttf_file> <ttf_size> [--char=<char>] [--descenders=<comma-separated-list>] [--special-align=<comma-separated-list>]
 
Options:
  -h --help          This helps screen

Examples:
  python3 ft-view-encoded.py ttf-fonts/Vera.ttf 13 --char=A  --> Display only the char "A"
  python3 ft-view-encoded.py ttf-fonts/Vera.ttf 13 --char=#34  --> Display only the char " , using default descender and special-align config
  python3  ft-view-encoded.py ttf-fonts/Vera.ttf 13 --descenders=p,q,j,#34 --> change the descenders
  python3  ft-view-encoded.py ttf-fonts/Vera.ttf 13 --descenders=          --> No descenders so baseline = bottomline! 
  python3  ft-view-encoded.py ttf-fonts/Vera.ttf 13 --special-align=a:T,=:B,#126:M --> change the special alignment instruction. a on TOP, = on Bottom, ~(#126) in middle (between the baseline and top)
  python3  ft-view-encoded.py ttf-fonts/Vera.ttf 13 --special-align=       --> delete special alignments. All chars on Bottom line (ideal for Wingdings chars).

Happy Electronic Hacking. 
MCHobby.be
""" 

# FreeType generator common items
from ftcommon import *
from docopt import docopt

if __name__ == '__main__':
    arguments = docopt( help )
    char_filter = arguments['--char'] # MANDATORY PARAMETER, eg: N 
    if (char_filter!= None) and len(char_filter)>0 and char_filter[0]=='#':
        char_filter = chr( int( char_filter[1:] ) )
    
    print( "Load font %s, set size to %i" % (arguments['<ttf_file>'], int(arguments['<ttf_size>'])) )             
    font_exporter = FreeTypeExporter( font_file=arguments['<ttf_file>'], font_size=int(arguments['<ttf_size>']) )
    if arguments['--descenders'] != None: # redefine the default descenders
       font_exporter.set_descenders( arguments['--descenders'] )
    if arguments['--special-align' ] != None: # redefine the default special alignments
       font_exporter.set_special_align( arguments['--special-align' ] ) 


    print( "max size (width,height): %i,%i" %(font_exporter.max_width, font_exporter.max_height ) )
    print( 'descender size = %i' % font_exporter.descender_size ) 

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
 



