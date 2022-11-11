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

with open(filename, 'r') as in_file:
    reader = csv.reader(in_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for row in reader:
        tweets.append(row[2]) 

print(f"Loaded {len(tweets)} tweets.")

test_tweets = [
    "He says I'm depressed most of the time. #sad",
    "For the first time I get to see @username actually being hateful! it was beautiful:)",
    '''"The San Francisco-based restaurant" they said, "doesn't charge $10.5"'''
]

################################################################

