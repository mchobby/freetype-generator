#!/usr/bin/env python3
# coding: utf8   

""" Try to reload an ili-fonts/x.py file and explore all the encoded characters """

#from veram_23 import VeraMono_23
#my_font = VeraMono_23

from etypo_42 import *
my_font = Entypo_42

# Generic display
for key in my_font:
   print( '--- %s %s' % (key, '-'*20) )
   print( my_font[key] )
   if type( key ) != int:
      continue
   for value in my_font[key]:
      print( bin(value).replace('1','*').replace('0',' ') )


