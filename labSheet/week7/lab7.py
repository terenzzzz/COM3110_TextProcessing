"""
USE: python <PROGNAME> (options) csv_datafile
OPTIONS:
    -h : print this help message and exit
    -e : process pictographic emojis (default: False)
"""
################################################################
import sys, re, getopt, csv, nltk

opts, args = getopt.getopt(sys.argv[1:], 'he')
opts = dict(opts)

def printHelp():
    progname = sys.argv[0]
    progname = progname.split('/')[-1] # strip out extended path
    help = __doc__.replace('<PROGNAME>', progname, 1)
    print('-' * 60, help, '-' * 60, file = sys.stderr)
    sys.exit()

if '-h' in opts:
    printHelp()

if len(args) < 1:
    print("\n** ERROR: no arg files provided **", file=sys.stderr)
    printHelp()

if len(args) > 1:
    print("\n** ERROR: too many arg files provided **", file=sys.stderr)
    printHelp()

if not args[0].endswith(".csv"):
    print("\n** ERROR: arg file should be in csv format **", file=sys.stderr)
    printHelp()

filename = args[0]

################################################################
# Read in text column from csv file

tweets = []

with open(filename, 'r', encoding='UTF-8') as in_file:
    reader = csv.reader(in_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for row in reader:
        tweets.append(row[2]) 

print(f"Loaded {len(tweets)} tweets.")
################################################################

test_tweets = [
    "That U.S.A. poster-print costs $12.40... :)",
    "He says I'm depressed most of the time. #sad ",
    "For the first time I get to see @username actually being hateful! it was beautiful:)",
    '''"The San Francisco-based restaurant" they said, "doesn't charge $10.5"'''
]

# for t in test_tweets:
#     list = re.findall(r'''(?x)(?:[A-Z]\.)+ | \w+(?:-\w+)* | \$?\d+(?:\.\d+)?%? | \.\.\. |  [][.,;"'?():_`-]''',t)
#     print (list)
    
################################################################
# TTR: Number of Types / Number of Words

def calcTTR(tweet):
    dict = {}
    numOfWords = 0
    for s in tweet:
        for w in s:
            if w in dict:
                dict[w]+=1
            else:
                dict[w]=1
            numOfWords += 1
    
    TTR = len(dict)/numOfWords
    print("TTR: ",TTR)

# Without preprocess
nothing = []
for t in tweets:
    list = t.split(" ")
    nothing.append(list)
calcTTR(nothing)

# Tokenised
tokenised = []
for t in tweets:
    list = re.findall(r'''(?x)(?:[A-Z]\.)+ | \w+(?:-\w+)* | \$?\d+(?:\.\d+)?%? | \.\.\. |  [][.,;"'?():_`-]''',t)
    tokenised.append(list)
calcTTR(tokenised)

# Tokenisation + lowercase
tokenised_lower = []
for t in tweets:
    list = []
    res = re.findall(r'''(?x)(?:[A-Z]\.)+ | \w+(?:-\w+)* | \$?\d+(?:\.\d+)?%? | \.\.\. |  [][.,;"'?():_`-]''',t)
    for x in res:
        list.append(x.lower())
    tokenised_lower.append(list)               
calcTTR(tokenised_lower)

# Tokenisation + lowercase + tweets preprocessing
tokenised_lower_pre = []
for t in tweets:
    list = []
    res = re.sub(r"@\w+", "<MENTIONS>", t)
    res = re.sub(r"#\w+", "<HASHTAGS>", res)
    res = re.findall(r'''(?x)(?:[A-Z]\.)+ | \w+(?:-\w+)* | \$?\d+(?:\.\d+)?%? | \.\.\. |  [][.,;"'?():_`-]''',res)
    # res_emoticon = re.sub(r"","EMOTICON",res_hashtags)
    # res_emojis = re.sub(r"","EMOJIS",res_hashtags)
    for x in res:
        list.append(x.lower())
    tokenised_lower_pre.append(list)               
calcTTR(tokenised_lower_pre)





# for t in tweets:
#     res = re.sub(r"@\w+", "<MENTIONS>", t)
#     res = re.sub(r"#\w+", "<HASHTAGS>", res)
#     # res_emoticon = re.sub(r"","EMOTICON",res_hashtags)
#     # res_emojis = re.sub(r"","EMOJIS",res_hashtags)
#     list = res.split()
#     print(list)





















