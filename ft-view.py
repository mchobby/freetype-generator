#!/usr/bin/env python3
# coding: utf8

"""
FreeType View - display the bitmap representation of a FreeType font file.

This script is useful for obtaining font sizing (in pixels) and its bitmap representation.

Usage:
  ft-view.py <ttf_file> <ttf_size> [--char=<char>] [--descenders=<descenders>] [--special-align=<special_align>]
  ft-view.py -h | --help

Options:
  -h --help                     Show this help message and exit
  --char=<char>                 Display only the specified character
  --descenders=<descenders>     Define custom descenders (comma-separated list)
  --special-align=<special_align> Define special alignment instructions (comma-separated list)
"""

# FreeType generator common items
from ftcommon import *
from docopt import docopt

def main():
    # Parse command line arguments
    arguments = docopt(__doc__)

    char_filter = arguments['--char']  # e.g., 'B' or None

    # Load font and set size
    print("Load font %s, set size to %i" % (arguments['<ttf_file>'], int(arguments['<ttf_size>'])))
    font_loader = FreeTypeLoader(font_file=arguments['<ttf_file>'], font_size=int(arguments['<ttf_size>']))
    
    # Set custom descenders
    if arguments['--descenders'] is not None:
        font_loader.set_descenders(arguments['--descenders'].split(','))

    # Set special alignments
    if arguments['--special-align'] is not None:
        font_loader.set_special_align(arguments['--special-align'].split(','))

    print("Max size (width,height): %i,%i" % (font_loader.max_width, font_loader.max_height))
    print('Descender size = %i' % font_loader.descender_size)

    # Print the bitmap representation of each character
    for ordinal in font_loader.char_ordinals:
        if char_filter is not None and ord(char_filter) != ordinal:
            continue
        font_loader.print_character(ordinal)

if __name__ == '__main__':
    main()

