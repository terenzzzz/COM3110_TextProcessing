"""\
------------------------------------------------------------
USE: python <PROGNAME> (options) file1...fileN
Purpose: omputing the level of word overlap between documents as an indicator of
document similarity
OPTIONS:
    -h : print this help message
    -b : use BINARY weights (default: count weighting)
    -s FILE : use stoplist file FILE
    -I PATT : identify input files using pattern PATT, 
              (otherwise uses files listed on command line)
------------------------------------------------------------
"""

import sys, re, getopt, glob

opts, args = getopt.getopt(sys.argv[1:], 'hs:bI:')
opts = dict(opts)
filenames = args

##############################
# HELP option

if '-h' in opts:
    progname = sys.argv[0]
    progname = progname.split('/')[-1] # strip out extended path
    help = __doc__.replace('<PROGNAME>', progname, 1)
    print(help, file=sys.stderr)
    sys.exit()

##############################
# Identify input files, when "-I" option used

if '-I' in opts:
    filenames = glob.glob(opts['-I'])

print('INPUT-FILES:', ' '.join(filenames))

##############################
# STOPLIST option
stops = set()
if '-s' in opts:
    with open(opts['-s'], 'r') as stop_fs:
        for line in stop_fs :
            stops.add(line.strip())

##############################
import re

def tokenisations():
    tokens = []
    with open("NEWS/news01.txt", encoding=("utf-8"),) as f:
        for line in f:
            lower = line.lower()
            list = re.findall(r'[A-Za-z]+',lower)
            for i in list:
                tokens.append(i)
    return tokens

def removeStop():
    nonStop = []
    for i in tokenisations():
        if(i not in stops):
            nonStop.append(i)
    return nonStop
            

def count_words():
    dictionary = {}
    for i in removeStop():
        if (i not in dictionary):
            dictionary[i] = 1
        else:
            dictionary[i] = dictionary[i] + 1
    return dictionary

def compare():
    print('1')
            

    
print(count_words())


