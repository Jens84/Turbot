# -*- coding: utf-8 -*-
"""
Created on Mon Nov 24 16:11:14 2014

@author: joseesteves
"""

import core
from nltk.corpus import wordnet as wn

#d = core.Dialog()
defin = core.Definition()

'''
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
nouns=["birth","year"]
keywords=["time"]
print "going to method getPropertyName"
listOfProperties = core.Definition._getPropertyName(defin, nouns, keywords)

print listOfProperties







