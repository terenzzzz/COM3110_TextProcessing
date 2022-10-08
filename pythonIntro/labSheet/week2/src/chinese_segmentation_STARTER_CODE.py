"""
USE: python <PROGNAME> (options)
OPTIONS:
    -h : print this help message and exit
    -d FILE : use dictionary file FILE
    -i FILE : process text from input file FILE
    -o FILE : write results to output file FILE
"""
################################################################

import sys, getopt,datetime

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

starttime = datetime.datetime.now()
chineseList = []
dicList = []
result = []
# 字典转数组
with open(opts['-d'], 'rb') as f:
    dictionary = f.read()
dicSplit = dictionary.split()
for i in dicSplit:
    decode=i.decode('utf8')
    dicList.append(decode)


# 数据集转数组
with open(opts['-i'], 'rb') as f:
    filecontent = f.read()
splited = filecontent.split()
for i in splited:
    decoded = i.decode('utf8')
    chineseList.append(decoded)


# 对比
def compare(word):
    for d in dicList:
        if word == d:
            return True
    return False


# 遍历
for i in chineseList: 
    start = 0
    end = len(i)
    while end > start:
        if compare(i[start:end]):
            result.append(i[start:end])
            start = end
            end = len(i)
        else:
            end = end - 1
    result.append('\n')
          

with open(opts['-o'],'w+',encoding='utf-8') as f:
    for i in result:
        if i == '\n':
            f.write(i)
        else:
            f.write(i + ' ')
            
endtime = datetime.datetime.now()
print ("Program Finished in ", (endtime - starttime).seconds," senconds")



































