"""\
------------------------------------------------------------
USE: python <PROGNAME> (options) file1...fileN
Purpose: omputing the level of word overlap between documents as an indicator of
document similarity
OPTIONS:
    -h : print this help message
    -b : use BINARY weights (default: non-weighting)
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

if '-b' in opts:
    print('Running in Weighted Algorithm...')
else:
    print('Running in Non-Weighted Algorithm...')

##############################
# STOPLIST option
stops = set()
if '-s' in opts:
    with open(opts['-s'], 'r') as stop_fs:
        for line in stop_fs :
            stops.add(line.strip())

##############################

def tokenisations(file):
    tokens = []
    with open(file, encoding=("utf-8"),) as f:
        for line in f:
            lower = line.lower()
            list = re.findall(r'[A-Za-z]+',lower)
            for i in list:
                tokens.append(i)
    return tokens

def removeStop(file):
    nonStop = []
    for i in tokenisations(file):
        if(i not in stops):
            nonStop.append(i)
    return nonStop
            

def count_words(file):
    dictionary = {}
    for i in removeStop(file):
        if (i not in dictionary):
            dictionary[i] = 1
        else:
            dictionary[i] = dictionary[i] + 1
    return dictionary

def compare(file1, file2):
    rate = 0
    dic1 = count_words(file1)
    dic2 = count_words(file2)
    # -b: Weighted mode
    if '-b' in opts:
        wordsAll = set()
        minSum = 0
        maxSum =0
        for i in dic1:
            wordsAll.add(i)
        for i in dic2:
            wordsAll.add(i)
        # Min(wa,wb), Max(wa,wb)
        for w in wordsAll:
            # get count in dic1
            if dic1.get(w):
                a = dic1.get(w)
            else:
                a = 0
            # get count in dic2
            if dic2.get(w):
                b = dic2.get(w)
            else:
                b = 0
            minimum = min(a,b)
            maximum = max(a,b)
            minSum = minSum + minimum
            maxSum = maxSum + maximum
        rate = minSum/maxSum
        return rate
    else:
        overlab = set()
        # set which word overlab
        for i in dic1:
            if i in dic2:
                overlab.add(i)
        overlabLen = len(overlab)
        # Length for all
        wordsLen = len(dic1) + len(dic2)
        rate = overlabLen/wordsLen
    return rate

# Main
if '-b' in opts:
    output = "weightedResult.txt"
else:
    output = "simpResult.txt"

# Result dictionary for rank
result = {}
for index,file in enumerate(filenames):
    current = index+1
    while current < len(filenames):
        result[filenames[index]+" <> "+ filenames[current]] = '%.3f' % compare(filenames[index],filenames[current])
        current += 1
        
# ranking
sort = sorted(result.items(),key=lambda x:-float(x[1]))[:10]
# Prink top 10
print("Top 10 overlab file:")
index=1
for i in sort:
    print("["+ str(index) + "] " + i[0] + ' : ' + i[1])
    index +=1
    
# write file
with open(output,'w') as result_out:
    for file in result:
        result_out.write(file + result[file] + '\n')

