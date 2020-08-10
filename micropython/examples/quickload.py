""" Quick Load the first .bin font file available on the filesystem and
    display its name on the SSD1307 OLED screen.

	This script is quite convenient to check a font rendering on the screen

	REQUIRES a binary file present on the file system

See: https://github.com/mchobby/freetype-generator
See: https://github.com/mchobby/freetype-generator/tree/master/micropython/

domeu, 09 Aug 2020, Initial Writing (shop.mchobby.be) """

from machine import I2C
from SSD1306 import SSD1306_I2C
from fdrawer import FontDrawer
import os
import gc
import time


i2c = I2C( 1, freq=2000000 )
lcd = SSD1306_I2C( width=128, height=64, i2c=i2c, addr=0x3c, external_vcc=True )

# locate a bin file on the filesystem
r = [ name for name in os.listdir() if '.bin' in name ]
if len(r) <= 0:
	print( "No .bin font file available on the FileSystem" )
else:
	while True:
		for name in r:
			print( "Loading font %s" % name )
			font_name = name.replace('.bin','')
			lcd.fill(0)
			fd = FontDrawer( frame_buffer=lcd, font_name = font_name )
			fd.print_str( fd.font_name, 2, 2 )
			lcd.show()
			del( fd ) # release the FontDrawer object
			gc.collect()
			print("   waiting 5 sec")
			time.sleep( 5 )
print("That's all folks")
