"""
USE: python <PROGNAME> (options) GOLD-FILE OUTPUT-FILE
OPTIONS:
    -h : print this help message and exit
"""
################################################################

import sys, re, getopt

################################################################
# Command line options handling, and help

opts, args = getopt.getopt(sys.argv[1:], 'h')
opts = dict(opts)

def printHelp():
    progname = sys.argv[0]
    progname = progname.split('/')[-1] # strip out extended path
    help = __doc__.replace('<PROGNAME>', progname, 1)
    print('-' * 60, help, '-' * 60, file=sys.stderr)
    sys.exit()
    
if '-h' in opts:
    printHelp()

if 0 and len(args) != 2:
    print("\n** ERROR: must specify precisely two input files! **", file=sys.stderr)
    printHelp()

################################################################
# Read in all lines of gold-standard and system results

with open(args[0], encoding = "utf8") as gold_in:
    gold_lines = gold_in.readlines()
    
with open(args[1], encoding = "utf8") as result_in:
    result_lines = result_in.readlines()
    
if len(result_lines) != len(gold_lines):
    print("\n** ERROR: gold-std and results files differ in num of lines **",\
          file=sys.stderr)
    printHelp()

################################################################
# Converts segmented sentence to set of tokens, each marked with 
# character offset position

def get_words_sequenced(line):
    words = set()
    posn = 0
    for word in line.split():
        words.add((posn, word))
        posn += len(word)
    return words

################################################################
# Score all lines

gold_word_count = 0
correct_words = 0
correct_sentences = 0

for i in range(len(gold_lines)):
    gold_words = get_words_sequenced(gold_lines[i])
    result_words = get_words_sequenced(result_lines[i])
    gold_word_count += len(gold_words)
    correct_words += len(gold_words & result_words)
    if gold_words == result_words:
        correct_sentences += 1

################################################################
# Print results

print()
print("Total correct words:", correct_words)
print("Total gold-std words:", gold_word_count)
word_acc = 100 * correct_words / gold_word_count
print("Word-level accuracy: %.2f%%" % word_acc)
sent_acc = 100 * correct_sentences / len(gold_lines)
print("Sentence-level accuracy: %.2f%%" % sent_acc)

################################################################

