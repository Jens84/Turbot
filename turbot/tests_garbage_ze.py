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

#sentence = "What is the name of Justin Bieber's associated bands?"
sentence = "What is the year when Justin Bieber was born?"
sTags = core._tokenizeFromStanfordNLP(sentence)
print sTags

# Get the object and verb of the sentence
obj = ' '.join([w[0] for w in sTags if 'NNP' in w[1]])
nouns = [w[0] for w in sTags if w[1]=='NN' or w[1]=='NNS']
adjectives = [w[0] for w in sTags if 'JJ' in w[1]]


print obj
print nouns
print adjectives

string1 = "ola"
string2 = unicode("ola")
print string1, string2

s = []
s.append(string1)
s.append(string2)

print s
aa = s[0]
bb = s[1]
print "<>"
print aa
print bb



