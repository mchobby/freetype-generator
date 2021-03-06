#!/usr/bin/env python3
# coding: utf8

""" Common items for FreeType generator """
from freetype import *
from math import ceil

class CharBitmap(object):
  """
  A 2D bitmap image represented as a list of byte values. Each byte indicates
  the state of a single pixel in the bitmap. A value of 0 indicates that
  the pixel is `off` and any other value indicates that it is `on`.

  See https://dbader.org/blog/monochrome-font-rendering-with-freetype-and-python
  """
  def __init__(self, width, height, pixels=None):
    self.width = width
    self.height = height
    self.pixels = pixels or bytearray(width * height)

  def __repr__(self):
    """Return a string representation of the bitmap's pixels."""
    rows = ''
    for y in range(self.height):
        for x in range(self.width):
            rows += '*' if self.pixels[y * self.width + x] else ' '
        rows += '\n'
    return rows

  @property
  def rows( self ):
    return self.height;

  @property
  def columns( self ):
    return self.width

  def pixel_at( self, column, row ):
    """Return the pixel value at a given column, row position"""
    if not( 0 <= row <= self.height):
      raise EValueError( 'row not in expected range' )
    if not( 0 <= column <= self.width ):
      raise EValueError( 'column not in expected range' )
    return self.pixels[row * self.width + column]

  @property
  def is_blank( self ):
    """ Check if the bitmap is completely blank """
    for bit in self.pixels:
      if bit:
        return False
    # if we got here, all bits are False
    return True

  def is_black( self, font_max_width, font_max_height ):
    """ Check if the bitmap is fully black (total height and width) """
    if (self.width != font_max_width) or (self.height != font_max_height):
      return False
    for bit in self.pixels:
      if not(bit):
        return False
    return True

class GlyphDecoder(object):
  """ GlyphDecoder accept a glyph slot and decode its data to provide a bit readable CharBitmap()

      The CharBitmap object will be exposed throught the "bitmap" attribute

  See https://dbader.org/blog/monochrome-font-rendering-with-freetype-and-python """
  def __init__(self, pixels, width, height):
    self.bitmap = CharBitmap(width, height, pixels)

  @staticmethod
  def from_glyphslot(slot):
    """Construct and return a Glyph object from a FreeType GlyphSlot."""
    pixels = GlyphDecoder.unpack_mono_bitmap(slot.bitmap)
    width, height = slot.bitmap.width, slot.bitmap.rows
    return GlyphDecoder(pixels, width, height)

  @staticmethod
  def unpack_mono_bitmap(bitmap):
    """
    Unpack a freetype FT_LOAD_TARGET_MONO glyph bitmap into a bytearray where
    each pixel is represented by a single byte.
    """
    # Allocate a bytearray of sufficient size to hold the glyph bitmap.
    data = bytearray(bitmap.rows * bitmap.width)

    # Iterate over every byte in the glyph bitmap. Note that we're not
    # iterating over every pixel in the resulting unpacked bitmap --
    # we're iterating over the packed bytes in the input bitmap.
    for y in range(bitmap.rows):
      for byte_index in range(bitmap.pitch):

        # Read the byte that contains the packed pixel data.
        byte_value = bitmap.buffer[y * bitmap.pitch + byte_index]

        # We've processed this many bits (=pixels) so far. This determines
        # where we'll read the next batch of pixels from.
        num_bits_done = byte_index * 8

        # Pre-compute where to write the pixels that we're going
        # to unpack from the current byte in the glyph bitmap.
        rowstart = y * bitmap.width + byte_index * 8

        # Iterate over every bit (=pixel) that's still a part of the
        # output bitmap. Sometimes we're only unpacking a fraction of a byte
        # because glyphs may not always fit on a byte boundary. So we make sure
        # to stop if we unpack past the current row of pixels.
        for bit_index in range(min(8, bitmap.width - num_bits_done)):

          # Unpack the next pixel from the current glyph byte.
          bit = byte_value & (1 << (7 - bit_index))

          # Write the pixel to the output bytearray. We ensure that `off`
          # pixels have a value of 0 and `on` pixels have a value of 1.
          data[rowstart + bit_index] = 1 if bit else 0

    return data

class FreeTypeLoader(object):
    """ Load a freetype font and render IN-MEMORY all the characters from char(0) to char(255) """
    face = None
    font_file = None

    # list of the characters having a descender
    descender_ordinals = [ ord('p'), ord('q'), ord('g'), ord('j'), ord('y')] # ord('z') is commonly not an descender
    # list of special character alignment
    #    T : on the top (eg: ',",^,` )
    #    M : centered between the baseline and top (eg: =, ~)
    #    B : on the bottom (eg: comma )
    special_align_ordinals = { 34 :'T', 39:'T', 42:'M', 43:'M', 44:'B', 45:'M', 59:'B', 60:'M', 61:'M', 62:'M', 94:'T', 96:'T', 126:'M', 176:'T', 178:'T', 179:'T', 185:'T' }
    # List of the characters (ordinal value) to generate
    char_ordinals = []

    def __init__( self, font_file, font_size ):
        self.font_file = font_file
        self.font_size = font_size
        self.face = Face( font_file )
        self.face.set_pixel_sizes( 0, font_size )
        self.characters = {} # a dict of all the chars, key is the character's ordinal
        self.glyphs     = {} # a dict glyph slots for all the characters

        # Load the characters representation
        self.init_characters()

        # Set a list of character (eg: for further export tasks)
        self.set_char_ordinals( '#32-#255' )


    def init_characters( self ):
        """ generate all the CharBitmap object (for each characters) and store it into
            the 'characters' dictionnary """
        self.characters = {}
        for i in range( 0, 255+1 ):
            self.face.load_char( chr(i), FT_LOAD_RENDER | FT_LOAD_TARGET_MONO )
            glyphslot = self.face.glyph
            self.glyphs[i] = glyphslot # keep reference to the glyphslot
            self.characters[ i ] = GlyphDecoder.from_glyphslot( glyphslot ).bitmap

    def char_has_descender( self, ordinal ):
        """ Check if the character is one of the characters which have a descender """
        return (ordinal in self.descender_ordinals)

    def str_to_ord( self, s ):
        """ Transform a string representing a character to its ordinal value.
            a -> return 97 ( which is ord('a') )
            #90 -> return 90 (which is ord('z') )"""
        if len(s) == 0:
            raise EValueError( 'empty string!' )
        if s[0] == '#':
            if len(s)<1:
                raise EValueError( '# must be followed by a number' )
        elif len(s)>1:
            raise EValueError( 'Allow ONLY one alphabetical character' )

        if s[0] == '#':
            return int( s[1:] )
        else:
            return ord( s )


    def set_char_ordinals( self, comma_str ):
        """ Initialise a list of characters (for further export purpose).
            Can use the following syntax:

            #32-#57 : from ordinal 32 to ordinal 57 (included)
            a-z,A,B,#123 : from a to z + A + B + ordinal 123 """
        self.char_ordinals.clear()
        items = comma_str.split(',')
        for item in items:
            # Has Range
            if '-' in item:
                for ordinal in range( self.str_to_ord( item.split('-')[0] ), self.str_to_ord( item.split('-')[1] )+1 ):
                    self.char_ordinals.append( ordinal )
            else:
                self.char_ordinals.append( self.str_to_ord( item ) )


    def set_descenders( self, comma_str ):
        """ Change the default descender list with with thoses contained within the comma_separated str.

            Example:
                set_descenders('')
                set_descenders('p,q,y,#106')
                set_descenders('#35') to define the '#' character. """
        self.descender_ordinals = []
        if len(comma_str)==0:
            return

        for value in comma_str.split(','):
            if value[0]=='#':
                self.descender_ordinals.append( int(value[1:]) )
            else:
                self.descender_ordinals.append( value[0] )

    def set_special_align( self, comma_str ):
        """ Change the default special alignment dictionnaly with with thoses contained within the comma_separated str.

            Example:
                set_special_align('')
                set_special_align('p:T,q:M,#106:B')  char:Align with align Top, Middle, Bottom
                set_special_align('#35:B') to define the '#' character. """
        self.special_align_ordinals = {}
        if len(comma_str)==0:
            return

        for key_value in comma_str.split(','):
            key,value = key_value.split(':')
            if key[0]=='#':
                self.special_align_ordinals[ int(key[1:]) ] = value
            else:
                self.special_align_ordinals[ ord(key[0]) ] = value

    @property
    def max_width( self ):
        if self.face==None:
            return 0
        iMax = 0
        for key, bitmap in self.characters.items():
            if bitmap.width > iMax:
                iMax = bitmap.width
        return iMax

    @property
    def max_height( self ):
        if self.face==None:
            return 0
        iMax = 0
        for key, bitmap in self.characters.items():
            if bitmap.height > iMax:
                iMax = bitmap.height
        return iMax

    @property
    def storage_size( self ):
        """ Number of bytes needed to store the a row of pixels """
        if self.max_height+1 <= 8:
            return 1
        elif self.max_height+1 <= 16:
        	return 2
        else:
            return 3 # Max 24 pixels height


    @property
    def descender_size( self ):
        """ Size (in pixels) of the descender which applies to pqyjg (maybe f).
            This size is calculated (rounded) based on FreeType font property """
        if self.face.descender == 0:
            return 0

        _desc_pixels = self.max_height * ( abs(self.face.descender) / self.face.height )
        return round( _desc_pixels ) # over 2.4 -> 2 ; 2.5 -> 2 ; 2.51 -> 3

    def ajusted_descender_size( self, ordinal ):
       """ Return the descender size BUT ensure that descender size (rounded calcul) + bitmap char's height STAYS UNDER the bitmap max-size. If not, the descender_size is adjuster at a lower value """
       return self.descender_size if self.descender_size + self.characters[ordinal].height < self.max_height else self.max_height - self.characters[ordinal].height


    def print_character( self, ordinal ):
        """ Just print the bits representation of a character (with space and star for 0 and 1) """
        print( '--- %s ----------------' % chr(ordinal) )
        if not( ordinal in self.characters ):
            print( '%s (%i) is not present in characters' % (chr(ordinal), ordinal) )
        print( 'Ordinal: %i' % ordinal )
        print( 'Char has descender: %s' % self.char_has_descender( ordinal ) )
        print( 'width, height = %i, %i' % (self.characters[ordinal].width, self.characters[ordinal].height) )
        # print( 'bitmap_top from base = %i' % self.glyphs[ordinal].bitmap_top )

        if self.char_has_descender( ordinal ):
            print( 'width, height = %i, %i (with %i px descender already included)' % (self.characters[ordinal].width, self.characters[ordinal].height, self.descender_size ) )
        else:
            # Sometime, Char-Size + Descender Size GOES OVER the font size --> reduce the descender
            _descender = self.ajusted_descender_size( ordinal )
            print( 'width, height = %i, %i (with %i px ajusted_descender added)' % (self.characters[ordinal].width, self.characters[ordinal].height + _descender, _descender ) )

        print( self.characters[ordinal] )


class FreeTypeExporter( FreeTypeLoader ):
    """ Export the FreeType font loaded to a Python file which can be load by the ILI9341
        driver developed by ropod7 on https://github.com/ropod7/pyboard_drive """

    def __init__( self, **kw ):
        FreeTypeLoader.__init__( self, **kw )

    def export_to_file( self, export_filename, objectName ):
        """ :params export_filename: name of the generated python file (eg: Arial_14.py)
            :param objectName: name of the font Object in the generated file (eg: Arial_14) """
        _file = open( export_filename, 'w')

        _file.write( '# Created from %s with freetype-generator.\n' % (self.font_file)  )
        _file.write( '# freetype-generator created by Meurisse D ( MCHobby.be ).\n' )
        _file.write( '\n' )
        _file.write( '%s = {\n' % objectName )
        _file.write( "'width' : %s, \n" % str(hex(self.max_width)) )
        _file.write( "'height' : %s, \n" % str(hex(self.max_height)) ) # Warning, this value may be higher that font size (due to some chars)

        # Keep the height+1 right bits when encoding for the font gen1 for the Pyboard.
        _mask = 0
        for i in range( self.max_height+1 ):
            _mask = _mask + (1<<i)

        # keys (int) : ordinal value of character (ascii code)
        #keys = list(self.characters.keys())
        #for key in keys:

        # keys (int) : ordinal value of character (ascii code)
        # char_ordinals contains the characters to exports.
        for key in self.char_ordinals:
            # Do not include:
            #   - the first 31 chars
            #   - the empty chars (not having a single pixel) EXPCEPT the space charaters
            #   - the fully black chars (having all the pixels lighted on total width and height
            if (self.characters[key].is_blank or self.characters[key].is_black(self.max_width, self.max_height) and not(key==32) ):
                continue
            # Encode the character bitmap (the bits) as value
            try:
                # print( 'encode character %i' % key )
                values = self.encode_this( key )
            except:
                print( 'Catch exception while encoding char %i' % key )
                raise

            _file.write( "%i:(" % key ) # Key entry in the dictionnary
            for iValue in range(len(values)):
               _file.write( " %s" % str(hex(values[iValue] & _mask) ) )
               if ( iValue < (len(values)-1) ) or (iValue==0): # force minimal tuple representation with coma! eg: (12345,)
                  _file.write( "," )
            _file.write( ")")
            if key != self.char_ordinals[-1]: # Append a comma between each character definition
                _file.write( ',' )
            _file.write( '\n' )
        _file.write( '}\n') # Close the dictionnary
        _file.close()

    def export_to_bin( self, export_filename, objectName ):
        """ :params export_filename: name of the generated binary file (eg: Arial_14.bin)
            :param objectName: name of the font Object in the generated file (eg: Arial_14) """
        _file = open( export_filename, 'wb')

        _file.write( bytes([0x21,0x46,0x44]) ) # Magic Key
        _file.write( bytes([0x01]) ) # Version
        _storage_size = self.storage_size
        _file.write( bytes([self.max_width,self.max_height, _storage_size ]) ) # Wifth, Height, DataSize
        _entries = 0
        for key in self.char_ordinals:
            # Do not include:
            #   - the first 31 chars
            #   - the empty chars (not having a single pixel) EXPCEPT the space charaters
            #   - the fully black chars (having all the pixels lighted on total width and height
            if (self.characters[key].is_blank or self.characters[key].is_black(self.max_width, self.max_height) and not(key==32) ):
                continue
            _entries += 1
        _file.write( bytes([_entries]) )

        # Keep the height+1 right bits when encoding for the font gen1 for the Pyboard.
        _mask = 0
        for i in range( self.max_height+1 ):
            _mask = _mask + (1<<i)

        # keys (int) : ordinal value of character (ascii code)
        # char_ordinals contains the characters to exports.
        for key in self.char_ordinals:
            # Do not include:
            #   - the first 31 chars
            #   - the empty chars (not having a single pixel) EXPCEPT the space charaters
            #   - the fully black chars (having all the pixels lighted on total width and height
            if (self.characters[key].is_blank or self.characters[key].is_black(self.max_width, self.max_height) and not(key==32) ):
                continue
            # Encode the character bitmap (the bits) as value
            try:
                # print( 'encode character %i' % key )
                values = self.encode_this( key )
            except:
                print( 'Catch exception while encoding char %i' % key )
                raise

            # Write the character entry
            _file.write( bytes([key]) ) # Key entry = ASCII char
            _file.write( bytes([len(values)]) ) # Number of  values for that entry
            # write the values
            for iValue in range(len(values)):
               _value = values[iValue] & _mask
               if self.storage_size >= 3:
                   _file.write( bytes( [(_value & 0xFF0000)>>16] ) )
               if self.storage_size >= 2:
                    _file.write( bytes( [(_value & 0x00FF00)>>8] ) )
               if self.storage_size >= 1:
                    _file.write( bytes( [(_value & 0x0000FF)] ) )

        _file.close()

    def encode_this( self, charCode ):
        """ Encode a given char so it follows the ILI Driver font definition
            (in the dictionnary)

            :params charCode: ascii code from 0 to 255 (the ordinal value)
            :returns: a list of numeric values respecting the char design

            The output result for a character would be:

            '65' : (0x4c00, 0x4300, 0x41c0, 0x4138, 0x4104, 0x4138,
                    0x41c0, 0x4300, 0x4c00),                           # 65 A

            Result that can be decoded as

            for line in Arial_14['65']:
            . . . print(bin(line))
            . . .
            '0b100110000000000'
            '0b100001100000000'
            '0b100000111000000'
            '0b100000100111000'
            '0b100000100000100'
            '0b100000100111000'
            '0b100000111000000'
            '0b100001100000000'
            '0b100110000000000'

          The first bit (left most one) in '0b1' is to 1 because we don't
          care it's value since the font has 14 pixels height.
          So we only care about the 14 bits on the right.
        """
        values = []
        # Character Bitmap
        bmp = self.characters[charCode]
        # Nbre of entry in the dictionnary = Character width
        nbr_entry = bmp.width
        # Number of bytes per entry (=font height / 8bits.)
        # Vera_19 = 19 point height => 19/8 = 2.375 => must be coded on 3 bytes
        nbr_bytes = ceil(self.max_height / 8)
        if ((self.max_height%8) == 0): # Encoded font must always starts with 0b1, so if the font has 8 points height (or a multiple)
            nbr_bytes += 1             # we have to create more room to receive that bit.
        nbr_bits  = nbr_bytes * 8

        # If we are coding 19 bits on X bytes, we will have to pad the left most
        # bits with 1
        pad_bits  = nbr_bits - self.max_height
        pad_value = 0
        for i in range( pad_bits ):
            # debug: print( 'shift by %i' % (nbr_bits-1-i) )
            pad_value = pad_value + ( 1<<(nbr_bits-1-i))

        # Building the values
        for iw in range( bmp.width ):
            value = pad_value
            # Debug: print( '---------------------------' )
            for ih in range( bmp.height ):
               _ih = bmp.height-1-ih # Must start by the "bottom" of the character

               # Align on the BottomLine
               _height_extra_shift = self.max_height-bmp.height # The character may have 10 pixels height on a 19 point height font --> shift properly to the left!

               # Align on the BaseLine (if it applies)
               # check if we do need to insert a descender space (in pixel) under the character
               if ( len(self.descender_ordinals)>0 ) and not( self.char_has_descender( charCode ) ):
                   # move up the normal character baseline
                   _height_extra_shift = _height_extra_shift - self.ajusted_descender_size( charCode )

               # SPECIAL ALIGNMENT
               # check for special alignment instruction (~,comma,", etc)
               _align = self.special_align_ordinals.get( charCode, None )
               if _align == 'T':
                   # special alignment ON TOP -> reset shifting
                   _height_extra_shift = 0
               elif _align == 'M':
                   # Special alignment IN MIDLLE of baseline and top
                   _height_extra_shift = _height_extra_shift - ( self.max_height-bmp.height-self.ajusted_descender_size( charCode ))//2
               elif _align == 'B':
                   # Specoam alignment TO BOTTOM (so re-reset the _height_extra_shift on the BottomLine)
                   _height_extra_shift = self.max_height-bmp.height

               # TODO: replacing the descender feature by glyph.bitmap_top does not work properly
               #       for every characters
               # _height_extra_shift = self.max_height - self.glyphs[ charCode ].bitmap_top

               # print( 'coding bit %i, extra shift of %i FOR VALUE %s' % (_ih, _height_extra_shift, bmp.pixel_at( iw, _ih )) )
               if bmp.pixel_at( iw, _ih ):
                   value = value + (1 << (_ih+_height_extra_shift))
            values.append( value )


        return values
