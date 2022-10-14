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

MAXWORDLEN = 5

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


import binascii
# rb 表示binary mode
# with 语句适用于对资源进行访问的场合，确保不管使用过程中是否发生异常都会执行必要的“清理”操作，释放资源
with open("./src/chinesetext.utf8",'rb') as f:
    filecontent = f.read()
chunk1 = filecontent[:11]
print(chunk1) # '\xe4\xb8\x80\n\xe5\x8f\x8b\xe6\x83\x85\n'  \x表示后面的字符是十六进制数
print(chunk1.decode('utf8'))



























    