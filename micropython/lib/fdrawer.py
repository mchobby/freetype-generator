
""" Font Drawer Class managing text drawing based on font files compiled with
    freetype-generator project

See: https://github.com/mchobby/freetype-generator
See: https://github.com/mchobby/freetype-generator/tree/master/micropython/

domeu, 07 Aug 2020, Initial Writing (shop.mchobby.be)
----------------------------------------------------------------------------
MCHobby invest time and ressource in developping project and libraries.
It is a long and tedious work developed with Open-Source mind and freely available.
IF you like our work THEN help us by buying your product at MCHobby (shop.mchobby.be).
----------------------------------------------------------------------------
Copyright (C) 2020  - Meurisse D. (shop.mchobby.be)
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>
"""
__version__ = '0.0.3'

import os

class FontLoaderError( Exception ):
	pass

class FontLoader:
	def __init__( self, font_name ):
		# Extract filesize
		fname = "%s.bin" % font_name
		fsize = [ items[3] for items in os.ilistdir() if items[0].upper() == fname.upper() ]
		if len(fsize) < 1:
			raise Exception( "missing %s file" % fname )
		f = open( '%s.bin' % font_name, 'rb' )
		data = f.read( 4 )
		if data != bytes([0x21,0x46,0x44,0x01]):
			raise Exception( "Invalid Magic Key!" )

		# Read information
		self.width  = f.read(1)[0] # Typical width
		self.height = f.read(1)[0]
		self.datasize = f.read(1)[0]
		self.entries  = f.read(1)[0]
		self.data = f.read() # read the remain of the file
		self.mv = memoryview(self.data)
		self.descender = self.get_descender() # Additional height for descender

	def get_width( self, word ):
		return len(word)*self.width

	def _extract_char_data( self, cursor, count ):
		# Extract the character data from the cursor position (composed of count items)
		r = []
		for i in range(count):
			_d = 0
			for _datasize in range(self.datasize):
				_d += self.mv[cursor] # self.data[cursor]
				if _datasize < (self.datasize-1):
					_d = _d << 8
				cursor += 1
			r.append( _d )
		return r

	def get_descender( self ):
		""" Explore the font for additional height needed to draw descenders """
		_max_height = 0
		_cursor = 0
		_ch  = self.mv[_cursor] #self.data[_cursor]
		_size = self.mv[_cursor+1] #self.data[_cursor+1]
		while _ch != None:
			__d = self._extract_char_data( _cursor, _size )
			for __val in __d:
				_max_height = max( _max_height, len(bin(__val))-3 )
			# New cursor Index
			_cursor += 2 + (_size*self.datasize)
			if _cursor >= len(self.data):
				_ch = None
			else:
				_ch = self.mv[_cursor] #self.data[_cursor]
				_size = self.mv[_cursor+1] #self.data[_cursor+1]
		return max(0,_max_height-self.height)

	def __getitem__( self, char_code ):
		""" Retreive the data for a given ascii caracter.
		    Will raise an exception if character is not available in the list """
		assert 0 <= char_code <= 255
		_cursor = 0
		_ch  = self.mv[_cursor] #self.data[_cursor]
		_size = self.mv[_cursor+1] #self.data[_cursor+1]
		while _ch != None:
			if _ch==char_code:
				# Char char_code found!
				return self._extract_char_data(_cursor+2,_size)
			else:
				# New cursor Index
				_cursor += 2 + (_size*self.datasize)
				if _cursor >= len(self.data):
					_ch = None
				else:
					_ch = self.mv[_cursor] #self.data[_cursor]
					_size = self.mv[_cursor+1] #self.data[_cursor+1]
		raise KeyError( "Missing char_code %i in font data" % char_code )


class FontDrawer:
	def __init__(self, frame_buffer, font_name  ):
		self.fb = frame_buffer
		self.font_name = font_name
		self._fontscale = 1
		self._fontcolor = (1) # Font color
		self._bgcolor   = (0) # Background color
		self._font = FontLoader( font_name )
		self._space   = len(self._font[73]) # space char width = idem to capital I width
		self._spacing = 2 #  space between chars

	@property
	def font( self ):
		return self._font

	@property
	def color( self ):
		""" FrameBuffer color value for drawing font """
		return self._fontcolor

	@color.setter
	def color( self, value ):
		""" FrameBuffer color value used to draw font """
		self._fontcolor = value

	@property
	def bgcolor( self ):
		""" FrameBuffer color value for drawing background """
		return self._bgcolor

	@bgcolor.setter
	def bgcolor( self, value ):
		""" FrameBuffer color value used to drawing background.
		 	(TODO) None will use the pixel background color for the drawed pixel """
		self._bgcolor = value

	@property
	def spacing( self ):
		""" Additional space between characters (in pixels) """
		return self._spacing

	@spacing.setter
	def spacing( self, value ):
		assert 0 <= spacing <= 10
		self._spacing = value

	@property
	def scale( self ):
		return self._fontscale

	@scale.setter
	def scale( self, value ):
		assert 1 <= value <= 4
		self._fontscale = value

	def _get_bgcolor(self, x, y):
		""" Extract the Background color at position x,y """
		if self._bgcolor == None:
			raise NotImplementedError('TODO')
		else:
			return self._bgcolor

	def _fill_bicolor(self, data, x, y, width, height, scale=1 ):
		bgcolor = self._get_bgcolor(x, y)

		xpix=0
		for col in data:
			ypix = (height-1) * scale
			for _y in range( height-1, -1, -1 ):
				c = self._fontcolor if ((col & (1<<_y)) > 0) else bgcolor
				for i in range( scale-1, -1, -1):
					self.fb.hline(x+xpix,y+ypix+scale+i,scale,c)
				ypix -= scale
			xpix+=scale


	def print_char(self, char, x, y ):
		""" Print a single char on a screen (a single characters or an ASCII code) """
		if type(char) is str:
			assert len(char) == 1
			index = ord(char)
		elif type(char) is int:
			assert char <= 255
			index = char

		if index==32: # space
			return self._space*self._fontscale, self._space*self._fontscale

		try:
			chrwidth = len(self._font[index]) * self._fontscale
			data = self._font[index]
		except KeyError:
			data = None
			chrwidth = self._font.width * self._fontscale

		if data is None:
			self.fb.rect(x, y, self._font.height*self._fontscale, chrwidth*self._fontscale, self._fontcolor)
		else:
			# Debug: print( data, x, y, chrwidth, self._font.height, self._fontscale )
			self._fill_bicolor(data, x, y, chrwidth, self._font.height, scale=self._fontscale)

		# char_width_proportionnal, char_width_NON_proportionnal
		return chrwidth, self._font.width * self._fontscale

	def print_str( self, text, x, y ):
		xpos = x
		for ch in text:
			widths = self.print_char( ch, xpos, y )
			xpos += widths[0] # add proportional_witdth of characters
			xpos += self._spacing*self._fontscale # 2 pixels spacing between chars
