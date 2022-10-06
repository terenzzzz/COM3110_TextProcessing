"""
USE: python <PROGNAME> (options)
OPTIONS:
-h : print this help message and exit
-d FILE : use dictionary file FILE
-i FILE : process text from input file FILE
-o FILE : write results to output file FILE
"""

import sys, getopt

opts, args = getopt.getopt(sys.argv[1:], 'hd:i:o:')

# print(f"Options: {opts}") # Do this to check variable content while debugging.
# print(f"Other Arguments: {args}")

opts = dict(opts) # Options converted to a dictionary object
# print(f"Options dictionary: {opts}")

def printHelp():
    progname = sys.argv[0]
    progname = progname.split('\\')[-1] # strip out extended path if running the program from Spyder
    help = __doc__.replace('<PROGNAME>', progname, 1) # replace the placeholder <PROGNAME> with the script filename
    print('-' * 60, help, '-' * 60, file=sys.stderr)
    # print(f"{'-' * 60} {help} {'-' * 60}", file=sys.stderr)
    sys.exit()
     
if '-h' in opts:
 	printHelp()

if len(args) > 0:
 	print("\n** ERROR: no arg files - only options! **", file=sys.stderr)
 	printHelp()
 
if '-d' not in opts:
 	print("\n** ERROR: must specify dictionary (opt: -d)! **", file=sys.stderr)
 	printHelp()

if '-i' not in opts:
 	print("\n** ERROR: must specify input text file (opt: -i)! **", file=sys.stderr)
 	printHelp()

if '-o' not in opts:
 	print("\n** ERROR: must specify output text file (opt: -o)! **", file=sys.stderr)
 	printHelp()
