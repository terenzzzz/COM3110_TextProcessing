"""
USE: python <PROGNAME> (options) 
OPTIONS:
    -h :      this help message and exit
    -d FILE : use FILE as data to create a new lexicon file
    -t FILE : apply lexicon to test data in FILE
"""
################################################################

import sys, re, getopt

################################################################
# Command line options handling, and help

opts, args = getopt.getopt(sys.argv[1:], 'hd:t:')

opts = dict(opts)

def printHelp():
    progname = sys.argv[0]
    progname = progname.split('/')[-1] # strip out extended path
    help = __doc__.replace('<PROGNAME>', progname, 1)
    print('-' * 60, help, '-' * 60, file=sys.stderr)
    sys.exit()
    
if '-h' in opts:
    printHelp()

if '-d' not in opts:
    print("\n** ERROR: must specify training data file (opt: -d FILE) **", file=sys.stderr)
    printHelp()

if len(args) > 0:
    print("\n** ERROR: unexpected input on commmand line **", file=sys.stderr)
    printHelp()

################################################################
print(opts['-d'])

tokenSent=list()
with open(opts['-d'], 'r') as training:
    for line in training :
        sentence  = line.strip()
        wordList = sentence.split()
        for word in wordList:
            tokenSent.append(word)
      

def toDict(tokenSent):
    dict = {} 
    for token in tokenSent:
        tokenList = token.split("/")
        length = len(tokenList)
        if tokenList[0] not in dict:
            dict[tokenList[0]]={}
        for i in range(1,length):
            if tokenList[i] in dict[tokenList[0]]:
                dict[tokenList[0]][tokenList[i]] = dict[tokenList[0]][tokenList[i]] + 1 
            else:
                dict[tokenList[0]][tokenList[i]] = 1
    return dict

def greatedCount():
    dict = toDict(tokenSent)
    sorted={}
    for outer in dict:
        tag = ""
        value=0
        for inner in dict[outer]:
            if dict[outer][inner] > value:
                value = dict[outer][inner]
                tag = inner
        sorted[outer]={tag:value}

    return sorted
print(greatedCount())



    
        