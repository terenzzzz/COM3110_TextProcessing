# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 19:42:05 2022

@author: pc
"""

# -*- coding: utf-8 -*-

'''
USE: python <PROGNAME> (options)
OPTIONS:
-h : print this help message and exit
-d FILE : use dictionary file FILE
-i FILE : process text from input file FILE
-o FILE : write results to output file FILE
'''

import sys, getopt

opts, args = getopt.getopt(sys.argv[1:],'hd:i:o:')
opts = dict(opts) # Options converted to a dictionary object

def printHelps():
     progname = sys.argv[0]
     progname = progname.split('\\')[-1] # strip out extended path if running the program from Spyder
     help = __doc__.replace('<PROGNAME>', progname, 1) # replace the placeholder <PROGNAME> with the script filen
     print('-' * 60, help, '-' * 60, file=sys.stderr)
     sys.exit()

if '-h' in opts:
    printHelps()
if len(args) > 0:
    print("\n** ERROR: noarg files - only options! **", file=sys.stderr)
    printHelps()
if '-d' not in opts:
    print("\n** ERROR: must speify dictionary (opt:-d)! **", file=sys.stderr)
    printHelps()
if '-i' not in opts:
    print("\n** ERROR: must speify dictionary (opt:-i)! **", file=sys.stderr)
    printHelps()
if '-o' not in opts:
    print("\n** ERROR: must speify dictionary (opt:-o)! **", file=sys.stderr)
    printHelps()
