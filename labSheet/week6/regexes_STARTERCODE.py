
# COM3110/4115: Text Processing
# Regular Expressions Lab Class

import sys, re

#------------------------------

testRE = re.compile('(logic|sicstus)', re.I)

#------------------------------

with open('RGX_DATA.html') as infs: 
    linenum = 0
    for line in infs:
        linenum += 1
        if line.strip() == '':
            continue
        print('  ', '-' * 100, '[%d]' % linenum, '\n   TEXT:', line, end='')
    
        # search only return the first
        # m = testRE.search(line)
        # if m:
        #     print('** TEST-RE:', m.group(1))
            
            
         #finditer method is an all matches method 
        # mm = testRE.finditer(line)
        # for m in mm:
        #     print('** TEST-RE:', m.group(1))
        
        # Task 1: Recognising HTML tags
        # htmlTagRe = re.compile('</?[A-Za-z0-9]+>',re.I)
        # rr = htmlTagRe.finditer(line)
        # for r in rr:
        #     # print(r)
        #     print('** TAG: ', r.group())

        # Task 2: distinguishes opening and closing tags
        # htmlTagRe = re.compile('(</[A-Za-z0-9]+>)|(<[A-Za-z0-9]+>)',re.I)
        # rr = htmlTagRe.finditer(line)
        # for r in rr:
        #     # print(r)
        #     if r.group(1):
        #         print('** Closing TAG: ', r.group(1))
        #     else:
        #         print('** Opening TAG: ', r.group(2))
        
        # Task 3: opening tags with params
        htmlTagRe = re.compile('(</[A-Za-z0-9]+>)|(<(([A-Za-z0-9]+))|(([a-z]+=[0-9]+))>)',re.I)
        rr = htmlTagRe.findall(line)
        print(rr)
            # if r.group(1):
            #     print('** Closing TAG: ', r.group(1))
            # else:
            #     print('** Opening TAG: ', r.group(3))
                
                
                
                