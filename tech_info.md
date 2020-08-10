
# Font filename

The software can generate any size (in pixel) font. The original screen (ILI9431) was limited to 23bits/pixels height font.

Due to the initial ILI9341 font coding, all fonts reaching a multiple of 8 pixels height (8 bits) are upsized of 8 bits.
* a 7 pixels height font is encoded inside a byte (8 bits) per column.
* a 8 pixels height font will be encoded on 16 bits per column (upsizing).  
* Fonts from 9 to 15 pixels height are encoded with 16 bits per column.    
* Fonts from 16 to 23 pixels hight are encoded with 24 bits per column.

When generating the values, the numeric values are masked with 0b1111111111 (mask having font_height_in_pixels+1 bits length).

# Binary File format

Here is the format of the `bin` file.

## Header Section
* Magic key - 3 bytes - !FD (0x21, 0x46, 0x44)
* Version - 1 byte - current is 0x01
* Width - 1 byte - NON PROPORTIONNEL font width (so max width) in pixels up to 0xFF
* Height - 1 byte - font height in pixels up to 0xFF
* DataSize - 1 byte - number of bytes per data entry (1,2,3 bytes so 8,16,24 pixels)
* Entries - 1 byte - number of entries in the data section

## Data Section

The data section contains <Entries> records of data.

Each record entry is composed as following:
* Char Code - 1 byte - ASCII code of the data
* Length - 1 bytes nombre of data of <DataSize> bytes enclosed within the entry
* DATA - <length>*<DataSize> bytes containing the pixels of the character.
