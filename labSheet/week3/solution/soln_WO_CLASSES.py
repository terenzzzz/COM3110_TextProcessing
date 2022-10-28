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

class CommandLine:
    def __init__(self):
        opts, args = getopt.getopt(sys.argv[1:], 'hs:bI:')
        opts = dict(opts)
        self.argfiles = args
        self.stops = set()
        self.binary_weights = False

        if '-h' in opts:
            self.printHelp()

        if '-b' in opts:
            self.binary_weights = True
        
        if '-s' in opts:
            self.readStopList(opts['-s'])

        if '-I' in opts:
            self.argfiles = glob.glob(opts['-I'])

    def printHelp(self):
        progname = sys.argv[0]
        progname = progname.split('/')[-1]
        help = __doc__.replace('<PROGNAME>', progname, 1)
        print(help, file=sys.stderr)
        sys.exit()

    def readStopList(self, file):
        f = open(file, 'r')
        for line in f:
            self.stops.add(line.strip())

class Document:
    def __init__(self, file, stops):
        self.name = file
        self.counts = {}
        word = re.compile(r'[A-Za-z]+')
        f = open(file, 'r')
        for line in f:
            for wd in word.findall(line.lower()):
                if wd not in stops:
                    if wd in self.counts:
                        self.counts[wd] += 1
                    else:
                        self.counts[wd] = 1
    
    def getCount(self, wd):
        return self.counts.get(wd, 0)

class CompareDocs:
    def __init__(self, config):
        self.argfiles = config.argfiles
        self.stops = config.stops
        self.binary_weights = config.binary_weights
        self.results = {}

    def jaccard(self, d1, d2):
        wds1 = set(d1.counts)
        wds2 = set(d2.counts)
        if self.binary_weights:
            over  = len(wds1 & wds2)
            under = len(wds1 | wds2)
        else:
            over = under = 0
            for w in (wds1 | wds2):
                over  += min(d1.getCount(w), d2.getCount(w))
                under += max(d1.getCount(w), d2.getCount(w))
        if under > 0:
            return over / under
        else:
            return 0.0

    def compareAll(self):
        docs = []
        for infile in self.argfiles:
            newdoc = Document(infile, self.stops)
            docs.append(newdoc)
        for i in range(len(docs)-1):
            d1 = docs[i]
            for j in range(i+1, len(docs)):
                d2 = docs[j]
                pair_name = '%s <> %s' % (d1.name, d2.name)
                self.results[pair_name] = self.jaccard(d1, d2)

    def printResults(self, stream=sys.stdout, topN=10):
        pairs = sorted(self.results, key=lambda v:self.results[v], reverse=True)
        if topN > 0:
            pairs = pairs[:topN]
        c = 0
        for k in pairs:
            c += 1
            print('(%d) %s = %.3f' % (c, k, self.results[k]), file=stream)

if __name__ == '__main__':
    config = CommandLine()
    compare = CompareDocs(config)
    compare.compareAll()
    compare.printResults()

