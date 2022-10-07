"""
USE: python <PROGNAME> (options)
OPTIONS:
    -h : print this help message and exit
    -d FILE : use dictionary file FILE
    -i FILE : process text from input file FILE
    -o FILE : write results to output file FILE
"""
################################################################

import sys, getopt

################################################################

MAXWORDLEN = 5

################################################################
# Command line options handling, and help

opts, args = getopt.getopt(sys.argv[1:], 'hd:i:o:')
opts = dict(opts)

def printHelp():
    progname = sys.argv[0]
    progname = progname.split('/')[-1] # strip out extended path
    help = __doc__.replace('<PROGNAME>', progname, 1)
    print('-' * 60, help, '-' * 60, file=sys.stderr)
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

################################################################
'''
with open("result.utf8",'rb') as f:
    filecontent = f.read()
print(filecontent) 
print(filecontent.decode('utf8'))

with open("result.utf8",'w') as f:
    f.write('芜湖')
'''

chineseList = []
dicList = []
result = []
# 字典转数组
with open("chinesetrad_wordlist.utf8", 'rb') as f:
    dictionary = f.read()
dicSplit = dictionary.split()
for i in dicSplit:
    decode=i.decode('utf8')
    dicList.append(decode)


# 数据集转数组
with open("chinesetext.utf8", 'rb') as f:
    filecontent = f.read()
splited = filecontent.split()
for i in splited:
    decoded = i.decode('utf8')
    chineseList.append(decoded)




for i in chineseList: 
    if len(i) < MAXWORDLEN:
        for d in dicList:
            if i == d:
                result.append(i)
    
        
print(result)
    




























