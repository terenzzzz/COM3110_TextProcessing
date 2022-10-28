"""\
------------------------------------------------------------
USE: python <PROGNAME> (options) file1...fileN
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
    progname = progname.split('/')[-1]
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

def count_words(filename, stops):
    wordRE = re.compile(r'[A-Za-z]+')
    counts = {}
    with open(filename, 'r') as infile:
        for line in infile:
            for word in wordRE.findall(line.lower()):
                if word not in stops: 
                    if word not in counts:
                        counts[word] = 0
                    counts[word] += 1
    return counts

##############################
# Compute counts for individual documents

docs = [ ]

for infile in filenames:
    docs.append(count_words(infile, stops))

##############################
# Compute similarity score for document pair

def jaccard(d1, d2):
    wds1 = set(d1)
    wds2 = set(d2)
    if '-b' in opts:
        over  = len(wds1 & wds2) # where '&' is set intersection op
        under = len(wds1 | wds2) # where '|' is set union op
    else:
        over = under = 0
        for w in (wds1 | wds2):

            if w in d1 and w in d2:
                over += min(d1[w], d2[w])

            wmax = 0
            if w in d1:
                wmax = d1[w]
            if w in d2:
                wmax = max(d2[w], wmax)
            under += wmax

    if under > 0:
        return over / under
    else:
        return 0.0

##############################
# Compute scores for all document pairs

results = {}
for i in range(len(docs)-1):
    for j in range(i+1, len(docs)):        
        pair_name = '%s <> %s' % (filenames[i], filenames[j])
        results[pair_name] = jaccard(docs[i], docs[j])

##############################
# Sort, and print top N results

topN = 10
pairs = sorted(results, key=lambda v:results[v], reverse=True)
if topN > 0:
    pairs = pairs[:topN]
c = 0
for k in pairs:
    c += 1
    print('[%d] %s = %.3f' % (c, k, results[k]), file=sys.stdout)

