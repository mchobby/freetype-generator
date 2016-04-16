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
    
    def __init__( self, font_file, font_size ):
        self.font_file = font_file
        self.font_size = font_size
        self.face = Face( font_file )
        self.face.set_pixel_sizes( 0, font_size )
        self.characters = {} # a dict of all the chars, key is the character's ordinal
        
        self.init_characters()
        
    def init_characters( self ):
        """ generate all the CharBitmap object (for each characters) and store it into 
            the 'characters' dictionnary """
        self.characters = {}
        for i in range( 0, 255+1 ):
            self.face.load_char( chr(i), FT_LOAD_RENDER | FT_LOAD_TARGET_MONO )
            glyphslot = self.face.glyph
            self.characters[ i ] = GlyphDecoder.from_glyphslot( glyphslot ).bitmap
            
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
        
    def print_character( self, ordinal ):
        """ Just print the bits representation of a character (with space and star for 0 and 1) """
        print( '--- %s ----------------' % chr(ordinal) )
        if not( ordinal in self.characters ):
            print( '%s (%i) is not present in characters' % (chr(ordinal), ordinal) )
        print( 'Ordinal: %i' % ordinal )
        print( 'width, height = %i, %i' % (self.characters[ordinal].width, self.characters[ordinal].height) )
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

        # keys (int) : ordinal value of character (ascii code) 
        keys = list(self.characters.keys())
        for key in keys:
            # Do not include:
            #   - the first 31 chars
            #   - the empty chars (not having a single pixel) EXPCEPT the space charaters
            #   - the fully black chars (having all the pixels lighted on total width and height
            if( (self.characters[key].is_blank or self.characters[key].is_black(self.max_width, self.max_height) or (key <= 31) ) and not(key==32) ):
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
               _file.write( " %s" % str(hex(values[iValue]) ) )
               if ( iValue < (len(values)-1) ) or (iValue==0): # force minimal tuple representation with coma! eg: (12345,)
                  _file.write( "," )
            _file.write( ")")
            if key != keys[-1]: # Append a comma between each character definition
                _file.write( ',' )
            _file.write( '\n' )
        _file.write( '}\n') # Close the dictionnary
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
               _height_extra_shift = self.max_height-bmp.height # The character may have 10 pixels height on a 19 point height font --> shift properly to the left!
               # print( 'coding bit %i, extra shift of %i FOR VALUE %s' % (_ih, _height_extra_shift, bmp.pixel_at( iw, _ih )) )
               if bmp.pixel_at( iw, _ih ): 
                   value = value + (1 << (_ih+_height_extra_shift))
            values.append( value ) 
        
        
        return values     
