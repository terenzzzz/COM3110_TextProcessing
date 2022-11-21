"""
USE: python <PROGNAME> (options) csv_datafile
OPTIONS:
    -h : print this help message and exit
    -e : process pictographic emojis (default: False)
"""
# Author: Tomas Goldsack
################################################################
import sys, re, getopt, csv, nltk

opts, args = getopt.getopt(sys.argv[1:], 'he')
opts = dict(opts)
process_emojis = False

def printHelp():
    progname = sys.argv[0]
    progname = progname.split('/')[-1] # strip out extended path
    help = __doc__.replace('<PROGNAME>', progname, 1)
    print('-' * 60, help, '-' * 60, file = sys.stderr)
    sys.exit()

if '-h' in opts:
    printHelp()

if '-e' in opts:
    process_emojis = True

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

with open(filename, 'r', encoding='UTF-8' ) as in_file:
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
# 1.1 Tokenisation + lowercase with python regex 

def tokenise_regex(text):
    ''' Tokenenise a string using a Regular Expression '''
    pattern = r"\w+(?:'\w+)?|[^\w\s]"
    return re.findall(pattern, text)

def lowercase_regex(text):
    ''' Lowercase a string using a Regular Expression '''
    return re.sub(r"[A-Z]", lambda x: x.group(0).lower(), text)

print("***\n### Text tweets (my regex): ###")
for tweet in test_tweets:
    print(tokenise_regex(lowercase_regex(tweet)))

################################################################
# 1.2 Tokenisation with NLTK regex

pattern = r'''(?x)          # set flag to allow verbose regexps
        (?:[A-Z]\.)+        # abbreviations, e.g. U.S.A.
      | \w+(?:-\w+)*        # words with optional internal hyphens
      | \$?\d+(?:\.\d+)?%?  # currency and percentages, e.g. $12.40, 82%
      | \.\.\.              # ellipsis
      | [][.,;"'?():_`-]    # these are separate tokens; includes ], [
    '''

print("***\n### Text tweets (nltk regex): ###")
for tweet in test_tweets:
    print(nltk.regexp_tokenize(tweet, pattern))

################################################################
# 1.3 Tokenisation with NLTK directly 

print("***\n### Text tweets (nltk built-in function): ###")
for tweet in test_tweets:
    print(nltk.word_tokenize(tweet))

################################################################
# 1.4 Additional tweet preprocessing 

def preprocess_tweet(text, include_emojis=False):
    ''' Replace tweet elements with normalised tags '''

    mention_pattern = r"@[a-zA-Z0-9_]{0,15}"
    hashtag_pattern =  r"#(\w+)"
    emoticon_pattern = r"(\:\w+\:|\<[\/\\]?3|[\(\)\\\D|\*\$][\-\^]?[\:\;\=]|[\:\;\=B8][\-\^]?[3DOPp\@\$\*\\\)\(\/\|])(?=\s|[\!\.\?]|$)"
    # ^source: https://stackoverflow.com/questions/28077049/regex-matching-emoticons


    emoji_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # Emoticons
        u"\U0001F300-\U0001F5FF"  # Symbols & pictographs
        u"\U0001FAC0-\U0001FaFF"  # Symbols & pictographs extended A
        u"\U00012600-\U000126FF"  # Miscellaneous Symbols
        u"\U00002700-\U000027BF"  # Dingbats
        u"\U0001F100-\U0001F1FF"  # Enclosed Alphanumeric Supplement
        u"\U0001F680-\U0001F6FF"  # Transport & Map symbols
        u"\U0001F1E0-\U0001F1FF"  # Flags
        u"\U00002190-\U000021FF"  # Arrows
                           "]+", flags = re.UNICODE) 

    processed_tweet = re.sub(emoticon_pattern, "<EMOTICONS>", \
                      re.sub(hashtag_pattern, "<HASHTAGS>", \
                      re.sub(mention_pattern, "<MENTIONS>", text))) 

    if include_emojis:
        processed_tweet = emoji_pattern.sub("<EMOJIS>", processed_tweet)
    
    return processed_tweet


print("***\n### Text tweets (tweet preprocessed): ###")
for tweet in test_tweets:
    print(preprocess_tweet(tweet))

################################################################
# 1.4 Counting words
  
def count_types_and_tokens(tweets_list):
    '''
    Counts and returns the number of type and tokens 
    (excluding punctuation + special characters
    '''
    types = set() 
    tokens = []

    for tweet in tweets_list:
        for token in tweet:

            # Check string is not special character/punctuation
            if re.search("[a-zA-Z0-9]+", token): 
                types.add(token)
                tokens.append(token)

    return len(types), len(tokens)


def print_config_ttr(config_string, processed_tweets):
    '''Calculates and prints the TTR for a given configuration of processed tweets'''
    num_types, num_tokens = count_types_and_tokens(processed_tweets)
    ttr = round(num_types/num_tokens, 3)
    print(f"{config_string}: {ttr} ({num_types} types, {num_tokens} tokens)")


print("***\n### TTR Calculation: ###")

# No preprocessing
print_config_ttr("No preprocessing", [tweet.split(" ") for tweet in tweets])

# Tokenised
print_config_ttr("Tokenised", [nltk.word_tokenize(tweet) for tweet in tweets])

# Tokenised + lowercased
print_config_ttr("Tokenised + lowercased", \
    [nltk.word_tokenize(lowercase_regex(tweet)) for tweet in tweets])

# Tokenised + lowercased + preprocessed
print_config_ttr("Tokenised + lowercased + preprocessed", \
    [nltk.word_tokenize(preprocess_tweet(lowercase_regex(tweet), process_emojis)) for tweet in tweets])

'''
*** Questions ***  
Q1: How does the TTR change in each configuration? 
A1: The TTR decreases with each additional preprocessing step.

Q2: Why does it happen and what is the impact on downstream tasks (e.g. sentiment analysis)?  
A2: This happens as each preprocessing step results in less unique tokens (a.k.a types) being 
    present in the dataset (i.e. the vocabulary is reduced).  
    For downstream tasks, having less types which appear more frequently can allow for patterns to 
    be recognised more easily from the same amount of data.

''' 