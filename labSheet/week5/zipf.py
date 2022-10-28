# -*- coding: utf-8 -*-
import re


# Read word
wordList=[]
with open('mobydick.txt', encoding=("utf-8"),) as f:
    for line in f:
        lower = line.lower()
        list = re.findall(r'[A-Za-z]+',lower)
        for i in list:
            wordList.append(i)

# Count word
wordDict={}
for w in wordList: 
    if w in wordDict:
        wordDict[w] +=1
    else:
        wordDict[w] = 1

# Sort Word
wordSorted = sorted(wordDict.items(), key=lambda x: x[1], reverse=True)

sum=0
distictWord = {}
for wc in wordSorted:
    sum += wc[1]
    if wc[0] in distictWord:
        distictWord[wc[0]] += 1
    else:
        distictWord[wc[0]] = 1
disticCount = len(distictWord)
top20 = wordSorted[:20]

    
    
    
print('Total number of word occurrences: ',sum)
print('The number of distinct words found: ',disticCount)
print('Top 20 words with their frequencies:')
printCount = 0
for t in top20:
    printCount +=1
    print(printCount,t[0],'\t:', t[1])
# print(wordSorted)


import pylab as p

x=[]
y=[]
index = 0
for i in top20:
    index += 1
    x.append(index)
    y.append(i[1])
print('\tX:',x)
print('\tY:',y)

p.plot(x,y)
p.xticks(x)
p.show()


cumulative = 0
cumulativeY = []
for i in top20:
    cumulative += i[1]
    cumulativeY.append(cumulative)
print('\tcumulativeY:',cumulativeY)
p.plot(x,cumulativeY)
p.xticks(x)
p.show()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    