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
# in 和 == 的效率？
# set 和 data的效率？


starttime = datetime.datetime.now()


# 字典转set
print("Processing dictionary... ")
dic_set = set()
with open(opts['-d'], encoding = "utf8") as dic_in:
    for line in dic_in:
        dic_set.add(line.strip())


# 数据集转set
print("Processing dataset... ")
word_set = set()
with open(opts['-i'], encoding = "utf8") as words_in:
    for line in words_in:
        word_set.add(line.strip())


# 遍历 (item in set)
def segment(sent, workset):
    result = []
    start = 0
    end = len(sent)
    while end > start:
        if (sent[start:end] in workset):
            result.append(sent[start:end])
            start = end
            end = len(sent)
        else:
            end = end - 1
    return result
        
print("Segmenting... ")
print("Writing result to file: ", opts['-o'])
with open(opts['-i'], encoding = "utf8") as text_in, \
     open(opts['-o'], "w", encoding = "utf8") as text_out:
    for line in text_in:
        words = segment(line.strip(), dic_set)
        print(' '.join(words), file = text_out)
        

            
endtime = datetime.datetime.now()
print ("Program Finished in ", (endtime - starttime).seconds," senconds")