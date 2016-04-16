#!/usr/bin/env python3
# coding: utf8                

help = """FreeType Generator - get a FreeType font file and generates a python font file for the Pyboard's ILI9341 driver 
 
Usage:
  ft-generate.py <ttf_file> <ttf_size> <out_python_file> <object_name>
 
Options:
  -h --help          This helps screen

Happy Electronic Hacking. 
MCHobby.be
"""

# FreeType generator common items
from ftcommon import *

from docopt import docopt
import sys
       
if __name__ == '__main__':
    arguments = docopt( help )
    # print( arguments )
    print( '-'*20 )

    # Eg: font_file = 'heydings_icons.ttf' , font_size = 23 
    print( "Load font %s, set size to %i" % (arguments['<ttf_file>'], int(arguments['<ttf_size>']) ) )             
    font_loader = FreeTypeExporter( font_file=arguments['<ttf_file>'], font_size=int(arguments['<ttf_size>']) )

    print( "max size (width,height): %i,%i" %(font_loader.max_width, font_loader.max_height ) )
    
    # Create the Python file for the ILI9341 PyBoard driver
    # Eg: export_filename='heyd_23.py', objectName='Heydings_23'
    font_loader.export_to_file( export_filename=arguments['<out_python_file>'], objectName=arguments['<object_name>'] )
    print( '%s written in file %s' % (arguments['<object_name>'],arguments['<out_python_file>']) )
