# -*- coding: utf-8 -*-
"""
Created on Mon Nov 24 16:11:14 2014

@author: joseesteves
"""

import core
from nltk.corpus import wordnet as wn


'''
#d = core.Dialog()
defin = core.Definition()


# checking word's synonyms
synonyms = []
keyword = "birthtime"
for i,j in enumerate(wn.synsets(keyword)):
    print "Synonyms of word ",keyword,":", ", ".join(j.lemma_names)
    synonyms += j.lemma_names
    print "Now the list of synonyms looks like: ",synonyms
    if i == 0:
        break
print synonyms

'''

noun = "hi"
nouns = []
nouns.append(noun)
for n in nouns:
    print n
print noun

print "----"
nouns.append("comment")
additionalKeywords = ["ahh"]
combinations = []
for i in nouns:
    for j in additionalKeywords:
        if i==j:
            continue
        combinations.append( i + j )
        combinations.append( j + i )
        
print combinations
nouns = []
nouns.append("birth")
nouns.append("year")
nouns.append("time")
nouns.append("time2")

print nouns
print "birth == ",nouns[0]
nouns=["birth","year","time","time"]
print "len: ",len(nouns)

'''
keywords=["time"]
print "going to method getPropertyName"
listOfProperties = core.Definition._getPropertyName(defin, nouns, keywords)

print listOfProperties


'''




