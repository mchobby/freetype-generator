""" Demonstration of the basic functionnality of the FrontDrawer.
    Load a given binary font file (.bin) and draw texte on SSD1307 OLED screen.

	REQUIRES the binary file "vera_m15.bin" to be present on the Pyboard

See: https://github.com/mchobby/freetype-generator
See: https://github.com/mchobby/freetype-generator/tree/master/micropython/

domeu, 07 Aug 2020, Initial Writing (shop.mchobby.be) """

from machine import I2C
from SSD1306 import SSD1306_I2C
from fdrawer import FontDrawer


i2c = I2C( 1, freq=2000000 )
lcd = SSD1306_I2C( width=128, height=64, i2c=i2c, addr=0x3c, external_vcc=True )

lcd.rect( 0, 0, 128, 64, 1 )
lcd.show()

fd = FontDrawer( frame_buffer=lcd, font_name = 'vera_m15' )
fd.print_str( "Font Demo", 2, 2 )
fd.print_char( "#", 100, 2 )
fd.print_str( fd.font_name, 2, 18 )
lcd.show()
