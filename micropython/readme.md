# MicroPython libraries and example to draw font characters on screen

The font drawer is designed the write text on a MicroPython FrameBuffer.

As FrameBuffer ar the recommanded ancestor for TFT Display. As such this front drawer should work with any of the TFT Screen display for MicroPython (as such as they are build on the top of FrameBuffer).

# Test

The `fdrawer.py` library and desired font (.bin files, EG: `vera.m15.bin`) must be copied to the MicroPython board.

The following [`test_basic.py`](examples/test_basic) example shows how to draw a character and a string.

``` python
from machine import I2C
from SSD1306 import SSD1306_I2C
from fdrawer import FontDrawer


i2c = I2C( 1, freq=2000000 )
lcd = SSD1306_I2C( width=128, height=64, i2c=i2c, addr=0x3c, external_vcc=True )

# Normal FrameBuffer operation
lcd.rect( 0, 0, 128, 64, 1 )
lcd.show()

# Use a font drawer to draw font to FrameBuffer
fd = FontDrawer( frame_buffer=lcd, font_name = 'vera_m15' )
fd.print_str( "Font Demo", 2, 2 )
fd.print_char( "#", 100, 2 )
fd.print_str( fd.font_name, 2, 18 )

# Send the FrameBuffer content to the LCD
lcd.show()
```
Which produce the following results:

![Vera_m15](docs/_static/vera_m15.jpg)

Note:
* the "m" in front of "m15" means that the .bin file only contains a part of the character set.
* An uncoded character is replaced by a squared rectangle (like the space in this example)

# Where are the fonts?

Look at the `upy-fonts` folder in the [freetype-generator github](https://github.com/mchobby/freetype-generator) repository.
