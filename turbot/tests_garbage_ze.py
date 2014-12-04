# -*- coding: utf-8 -*-
"""
Created on Mon Nov 24 16:11:14 2014

@author: joseesteves
"""

import core
from nltk.corpus import wordnet as wn
import nltk.classify.util


def dialogue_act_features(post):
    """Return a feature from an object of type nltk.util.LazySubsequence.

    Arguments:
    post -- object of type nltk.util.LazySubsequence

    Return values:
    Dictionary that represents a feature
    """

    features = {}
    for word in nltk.word_tokenize(post):
        features['contains(%s)' % word.lower()] = True
    features['first_word'] = nltk.word_tokenize(post)[0].lower()
    return features


posts = nltk.corpus.nps_chat.xml_posts()[:100]

haveBeQuestions = ['Have you been here?', 'Are you okay?',
                   'Are you alive?', 'Am I a dragon?',
                   'Have you any idea?', 'Has she a cat?',
                   'Are we greedy?', 'Is he tired?', 'Is she good?',
                   'Are you sure?', 'Have you already done it?',
                   'Has he eaten it?', 'Is tomato red?']


featuresets = [(dialogue_act_features(post.text),
                post.get('class'))for post in posts]
print type(featuresets)


g = dialogue_act_features(post.text)

print type(g)
print type(featuresets[0])
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

'''

