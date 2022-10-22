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

# -- Read Sentent in the file
tokenSent=list()
with open(opts['-d'], 'r') as training:
    for line in training :
        sentence  = line.strip()
        wordList = sentence.split()
        for word in wordList:
            tokenSent.append(word)
################################################################


# -- make sentent into Dictionary
# -- Maping in the form {'then-market': {'JJ': 1}}

def toDict(tokenSent):
    dict = {}
    for token in tokenSent:
        tokenList = token.split("/")
        length = len(tokenList)
        if tokenList[0] not in dict:
            dict[tokenList[0]]={}
        for i in range(1,length):
            if tokenList[i] in dict[tokenList[0]]:
                dict[tokenList[0]][tokenList[i]] += 1 
            else:
                dict[tokenList[0]][tokenList[i]] = 1
    return dict


################################################################


# -- proportion of types that have more than one tag(ambiguous)  ambiguousTypes/allTypes
# -- accuracy naive tagger would have on the training data  ambiguousTokens/allTokens
# -- most common tags globally  greateToken/allTokens,
wordTagCounts = toDict(tokenSent)
ambiguousTypes = 0 # have more than one tag
allTypes = len(wordTagCounts)
ambiguousTokens = 0
allTokens = 0
greateToken = 0
tagCount={}
for w in wordTagCounts:
    tagsCount = wordTagCounts[w].values()
    if  len(tagsCount) > 1:
        ambiguousTypes += 1
        ambiguousTokens += sum(tagsCount)
    greateToken += max(tagsCount)
    allTokens += sum(tagsCount)
    for t,c in wordTagCounts[w].items():
        if t in tagCount:
            tagCount[t] += c
        else:
            tagCount[t] = c
    
typeRate = format(100*ambiguousTypes/allTypes, '.2f')
print('Proportion of types ambiguous: {a}% ({at}/{all}) '.format(a=typeRate,at=ambiguousTypes,all=allTypes))

tokenRate = format(100*ambiguousTokens/allTokens, '.2f')
print('Proportion of tokens ambiguous: {a}% ({at}/{all}) '.format(a=tokenRate,at=ambiguousTokens,all=allTokens))

greatRate = format(100*greateToken/allTokens, '.2f')
print('Accuracy of naive tagger on training data: {a}% ({at}/{all}) '.format(a=greatRate,at=greateToken,all=allTokens))

# Sort in order
sort = sorted(tagCount.items(),key=lambda x:-float(x[1]))[:10]
print('Top Ten Tags by count:')
for t,c in sort:
    rate=format(100*c/allTokens, '.2f')
    print('{t}  {rate}% ({c}/{all})'.format(t=t, rate=rate,c=c,all=allTokens))


################################################################
def greatedCount(dict):
    sorted={}
    for outer in dict:
        tag = ""
        value=0
        for inner in dict[outer]:
            if dict[outer][inner] > value:
                value = dict[outer][inner]
                tag = inner
        sorted[outer]=tag

    return sorted
maxTags = greatedCount(wordTagCounts)
with open(opts['-t'], 'r') as test:
    allTest = 0
    correct = 0
    for line in test:
        sentence  = line.strip()
        wordList = sentence.split()
        for wt in wordList:
            wordTag = wt.split('/')
            if wordTag[0] in maxTags:
                if wordTag[1] == maxTags[wordTag[0]]:
                    correct += 1
            allTest += 1
            
    score = format(100*correct/allTest, '.2f')
    print('Score on test data： {score} ({correct}/{allTest})'.format(score=score, correct=correct,allTest=allTest))
################################################################        





    
        