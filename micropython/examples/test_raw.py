""" Raw testing code drawing texte from a .py python FONT FILE on SSD1307 OLED screen.

	*** DO NOT USE THIS CODE AS DEVELOPPMEN REFERENCE ***
	***   This is for DEMONSTRATION PURPOSE ONLY.     ***

	REQUIRES the file "vera_m15.py" to be present on the Pyboard

See: https://github.com/mchobby/freetype-generator
See: https://github.com/mchobby/freetype-generator/tree/master/micropython/

domeu, 07 Aug 2020, Initial Writing (shop.mchobby.be) """

import vera_m15  # Python based font.
from machine import I2C
from SSD1306 import SSD1306_I2C

class FontDrawer:
	def __init__(self, fb, font  ):
		self.fb = fb
		self._fontscale = 1
		self._fontcolor = (1) # Font color
		self._bgcolor   = (0) # Background color
		self._portrait  = True
		self._font = font

	@property
	def scale( self ):
		return self._fontscale

	@scale.setter
	def scale( self, value ):
		assert 1 <= value <= 4
		self._fontscale = value

	def _get_bgcolor(self, x, y):
		""" Extract the Background color at position x,y """
		return self._bgcolor

	def _fill_bicolor(self, data, x, y, width, height, scale=1 ):
		bgcolor = self._bgcolor if self._bgcolor else self._get_bgcolor(x, y)

		xpix=0
		for col in data:
			ypix = (height-1) * scale
			for _y in range( height-1, -1, -1 ):
				c = self._fontcolor if ((col & (1<<_y)) > 0) else bgcolor
				for i in range( scale-1, -1, -1):
					self.fb.hline(x+xpix,y+ypix+scale+i,scale,c)
				ypix -= scale
			xpix+=scale

		#xpix=0
		#for col in data:
		#	ypix=0
		#	for _y in range( height-1, -1, -1 ):
		#		c = self._fontcolor if ((col & (1<<_y)) > 0) else bgcolor
		#		for scale_line in range( scale ):
		#			self.fb.hline(x+xpix,y+ypix+scale_line,scale,c) # width = scale
		#		ypix += scale
		#	xpix+=scale



	def print_char(self, char, x, y ):
		scale = self._fontscale
		font = self._font

		index = ord(char)
		height = font['height']
		try:
			chrwidth = len(font[index]) * scale
			data = font[index]
		except KeyError:
			data = None
			chrwidth = font['width'] * scale
		#X = self.fb.height - y - (height * scale) + scale
		#Y = x

		#self._char_orientation()
		# Garbage collection
		if data is None:
			#self._graph_orientation()
			self.rect(x, y, height*scale, chrwidth*scale, self._fontcolor)
		else:
			print( data, x, y, chrwidth, height, scale )
			self._fill_bicolor(data, x, y, chrwidth, height, scale=scale)

		# char_width_proportionnal, char_width_NON_proportionnal
		return chrwidth, font['width'] * scale

	def print_str( self, text, x, y ):
		xpos = x
		for ch in text:
			widths = self.print_char( ch, xpos, y )
			xpos += widths[0] # add proportional_witdth of characters
			xpos += 2*self._fontscale # Space between chars



i2c = I2C( 1, freq=2000000 )
lcd = SSD1306_I2C( width=128, height=64, i2c=i2c, addr=0x3c, external_vcc=True )

lcd.rect( 0, 0, 128, 64, 1 )
lcd.show()

fd = FontDrawer( fb=lcd, font = vera_m15.Vera_m15 )
fd.print_char( "a", 2, 2 )
fd.print_str( "création", 2, 18 )
lcd.show()
