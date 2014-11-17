"""

"""

__version__ = '0.0.1'
__author__ = 'JBO, JES, JRG'
__author_email__ = 'jeremy.rombourg@gmail.com'

import nltk
import random
import aiml
import urllib2
import json

import learn
from learn import *

from SPARQLWrapper import SPARQLWrapper, JSON


class Dialog():
    _classifierTypeQ = None

    def __init__(self):
        self._classifierTypeQ = learn.dialog.trainTypeQuestion()

    def answer(self, question):
        type = self._classifierTypeQ.classify(
            learn.dialog.dialogue_act_features(question))

        if type == "ynQuestion":
            tokens = nltk.word_tokenize(question.lower())
            q = nltk.Text(tokens)
            qTags = nltk.pos_tag(q)
            print qTags
            verbs = [word for word, tag in qTags if tag == 'VB']
            print verbs
            yesNo = ['Yes', 'No']
            if len(verbs) == 1:
                return random.choice(yesNo) + ", I do !"
        else:
            return "I don't know what you mean."

    def chat(self):
		k = aiml.Kernel()
		k.learn("./turbot/standard-aiml/std-startup.xml")
		while True:
			k.respond(raw_input(">"))


class Definition():

	def __init__(self):
		self._sparql = SPARQLWrapper("http://dbpedia.org/sparql")
		self._sparql.setReturnFormat(JSON)
		req = urllib2.Request("http://dbpedia.org/ontology/data/definitions.jsonld")
		f = urllib2.urlopen(req)
		response = f.read()
		f.close()
		data = json.loads(response)
		result = [row["http://open.vocab.org/terms/defines"]
				for row in data["@graph"]
				if row["@id"] == "http://dbpedia.org/ontology/"][0]
		self._properties = [p[28:] for p in result]

	def nounify(verb_word):
		""" Transform a verb to the closest noun: die -> death """
		verb_synsets = wn.synsets(verb_word, pos="v")

		# Word not found
		if not verb_synsets:
			return []

		# Get all verb lemmas of the word
		verb_lemmas = [l for s in verb_synsets for l in s.lemmas
				if s.name.split('.')[1] == 'v']

		# Get related forms
		derivationally_related_forms = [(l, l.derivationally_related_forms())
				for l in verb_lemmas]

		# filter only the nouns
		related_noun_lemmas = [l for drf in derivationally_related_forms
				for l in drf[1] if l.synset.name.split('.')[1] == 'n']

		# Extract the words from the lemmas
		words = [l.name for l in related_noun_lemmas]
		len_words = len(words)

		# Build the result in the form of a list containing tuples (word, probability)
		result = [(w, float(words.count(w))/len_words) for w in set(words)]
		result.sort(key=lambda w: -w[1])

		# return all the possibilities sorted by probability
		return result

	def answer(self, sentence):
		'''
		self._sparql.setQuery("""
			PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
			SELECT ?birthPlace
			WHERE { <http://dbpedia.org/resource/Claude_Monet> <http://dbpedia.org/property/birthPlace> ?birthPlace }
			""")

		results = self._sparql.query().convert()

		return results["results"]["bindings"]
		'''
		tokens = nltk.word_tokenize(sentence.lower())
		s = nltk.Text(tokens)
		sTags = nltk.pos_tag(s)

