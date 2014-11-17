"""

"""

__version__ = '0.0.1'
__author__ = 'JBO, JES, JRG'
__author_email__ = 'jeremy.rombourg@gmail.com'

import nltk
#import aiml
import urllib
import urllib2
import bs4
import json
import en
import wikipedia
import learn
import re
from SPARQLWrapper import SPARQLWrapper, JSON
from nltk.corpus import wordnet as wn


def _getSubject(question):
    subject = ""
    qTags = nltk.pos_tag(question)
    if question[1].lower() == 'you':
        subject = "I "
    elif question[1].lower() == 'i':
        subject = "you "
    elif qTags[1][1] == 'DT':
        subject = question[1] + " " + question[2] + " "
    elif qTags[1][1] in ['NNP', 'NNPS']:
        i = 1
        while (qTags[i][1] in ['NNP', 'NNPS']):
            subject += question[i] + " "
            i += 1
    else:
        subject = question[1] + " "

    return subject


def _getObject(question, subject):
    object = ""
    qTags = nltk.pos_tag(question)
    # Find the sentence's object
    for word, tag in qTags:
        # This is the subject
        if(word in subject):
            continue
        if(tag in ['DT', 'IN', 'JJ', 'NN', 'NNS', 'NNP', 'NNPS']):
            object += ' ' + word
        else:
            if(object != ""):
                break

    return object


def _getVerbs(question):
    qTags = nltk.pos_tag(question)
    verbs = [word for word, tag in qTags
             if tag in ['VB', 'VBD', 'VBP', 'VBN', 'VBG', 'VBZ', 'MD']]
    if verbs[0].lower() == 'are':
        verbs[0] = 'am'

    return verbs


class Dialog():
    _classifierTypeQ = None
    _classifierWhQ = None
    _posNegWords = None

    def __init__(self):
        self._classifierTypeQ = learn.dialog.trainTypeQuestion()
        self._posNegWords = learn.dialog.getPosNegWords()
        self._classifierWhQ = learn.dialog.trainWhQuestion()

    def _getPosNegScore(self, tokens):
        # neutral score
        posNegScore = 0
        # Get score of question (positive/negative)
        for token in tokens:
            if token in self._posNegWords:
                posNegScore += float(self._posNegWords[token])
        return posNegScore

    def _makeYesNoAnswer(self, subject, verbs, object, score, ans):
        # Get the subject
        if ans == "No, " or (ans == "" and score < 0):
            ans = "No, "
            notBe = " not "
            notDo = "don't "

            if object == ".":
                notBe = " not"
        elif ans == "Yes, " or (ans == "" and score >= 0):
            ans = "Yes, "
            notDo = " "
            notBe = " "

        subject = ans + subject

        print subject
        print verbs
        print object
        # Answer according to previous results
        if len(verbs) == 1:
            if verbs[0].lower() in ['am', 'are', 'is']:
                notDo = ""
            else:
                notBe = ""

            return re.sub(r'\s+', ' ',
                          subject + notDo + verbs[0] + notBe + object)
        elif len(verbs) == 2:
            if verbs[0].lower() == 'do':
                verbs[0] = ''
            if verbs[0].lower() == 'did':
                verbs[0] = ''
                verbs[1] = en.verb.past(verbs[1])
            if verbs[0].lower() == 'will':
                verbs[0] = 'will'

            return re.sub(r'\s+', ' ',
                          subject + verbs[0] + notBe + verbs[1] + object)
        else:
            if score < 0:
                return "No."
            else:
                return "Yes !"

    def _getAnswerFromWikipedia(self, subject, verbs, object):
        page = wikipedia.page(wikipedia.search(subject)[0])

        tokens = nltk.word_tokenize(object)
        t = nltk.Text(tokens)
        qTags = nltk.pos_tag(t)

        newObject = ''.join([o for o, tag in qTags
                             if tag not in ['DT', 'IN']])
        newObject = newObject[:-1]
        print newObject
        sent = re.findall(r"([^.]*?" +
                          newObject +
                          "[^.]*\.)", page.summary, re.IGNORECASE)

        if len(sent) == 0 or re.search(r'\bnot|n\'t\b', sent[0]):
            return "No, "
        else:
            return "Yes, "

    def answer(self, question):
        type = self._classifierTypeQ.classify(
            learn.dialog.dialogue_act_features(question))
            
        if type == "whQuestion":
            whType = self._classifierWhQ.classify(learn.dialog.dialogue_act_features(question))
            return "This question is of type wh and its category is: "+whType

        if type == "ynQuestion":
            tokens = nltk.word_tokenize(question)
            tokens[0] = tokens[0].lower()
            score = self._getPosNegScore(tokens)
            ans = ""

            # Find the sentence's verb
            q = nltk.Text(tokens)
            qTags = nltk.pos_tag(q)
            print qTags

            # Get the verbs
            verbs = _getVerbs(q)

            # Get the subject
            subject = _getSubject(q)

            # Get the object
            object = _getObject(q, subject)
            object += "."

            # We need to check the answer : yes or no
            if subject not in ["I ", "you ", "we ",
                               "he ", "she ", "it ", "they "]:
                ans = self._getAnswerFromWikipedia(subject, verbs, object)

            return self._makeYesNoAnswer(subject, verbs, object, score, ans)
        elif type == "whQuestion":

            d = Definition()
            return d.answer(question)
        else:
            return "I don't know what you mean."

    def chat(self):
        #k = aiml.Kernel()
        #k.learn("./turbot/standard-aiml/std-startup.xml")
        #while True:
        #   k.respond(raw_input(">"))
        return ""


class Definition():

    def __init__(self):
        '''
        self._sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        self._sparql.setReturnFormat(JSON)
        req = urllib2.Request(
            "http://dbpedia.org/ontology/data/definitions.jsonld")
        f = urllib2.urlopen(req)
        response = f.read()
        f.close()
        data = json.loads(response)
        result = [row["http://open.vocab.org/terms/defines"]
                for row in data["@graph"]
                if row["@id"] == "http://dbpedia.org/ontology/"][0]
        self._properties = [p[28:] for p in result]
        '''

    def nounify(verb_word):
        ''' Transform a verb to the closest noun: die -> death '''
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
                               for l in drf[1]
                               if l.synset.name.split('.')[1] == 'n']

        # Extract the words from the lemmas
        words = [l.name for l in related_noun_lemmas]
        len_words = len(words)

        # Build the result in the form of
        # a list containing tuples (word, probability)
        result = [(w, float(words.count(w)) / len_words) for w in set(words)]
        result.sort(key=lambda w: -w[1])

        # return all the possibilities sorted by probability
        return result

    def answer(self, sentence):
        '''
        self._sparql.setQuery("""
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT ?birthPlace
            WHERE { <http://dbpedia.org/resource/Claude_Monet>
             <http://dbpedia.org/property/birthPlace> ?birthPlace }
            """)

        results = self._sparql.query().convert()

        return results["results"]["bindings"]
        '''
        #tokens = nltk.word_tokenize(sentence.lower())
        #s = nltk.Text(tokens)
        #sTags = nltk.pos_tag(s)
        #nltk.help.upenn_tagset()
        #print sTags
        #print wikipedia.search(sentence)

        params = urllib.urlencode({'q': sentence})
        req = urllib2.Request("http://wiki.answers.com/search?" + params)
        response = urllib2.urlopen(req, params).read()
        soup = bs4.BeautifulSoup(response)
        results = soup.findAll('div', attrs={'class': 'answer_text'})
        if len(results) > 0:
            return results[0].text.strip()
        else:
            return "I don't know"
