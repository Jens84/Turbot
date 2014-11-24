"""

"""

__version__ = '0.0.1'
__author__ = 'JBO, JES, JRG'
__author_email__ = 'jeremy.rombourg@gmail.com'

import nltk
import random
import urllib
import urllib2
import bs4
import json
import en
import wikipedia
import learn
import re
import difflib
from SPARQLWrapper import SPARQLWrapper, JSON
from nltk.corpus import wordnet as wn


def _tokenizeFromStanfordNLP(sentence):
    params = urllib.urlencode({'query': sentence})
    req = urllib2.Request("http://nlp.stanford.edu:8080/parser/index.jsp")
    response = urllib2.urlopen(req, params).read()
    soup = bs4.BeautifulSoup(response)
    parsed = soup.find('div', attrs={'class': 'parserOutputMonospace'})
    sTags = []
    for c in parsed.children:
        if c.name != "div" or c.string == "None":
            continue
        print c.string
        e = c.string.strip().split('/')
        sTags.append((e[0], e[1]))
    return sTags


def _getSubject(question, ind):
    subject = ""
    qTags = _tokenizeFromStanfordNLP(question)
    if question[ind].lower() == 'you':
        subject = "I "
    elif question[ind].lower() == 'i':
        subject = "you "
    elif qTags[ind][1] == 'DT':
        subject = question[ind] + " " + question[ind + 1] + " "
    elif qTags[ind][1] in ['NNP', 'NNPS']:
        i = ind
        while (qTags[i][1] in ['NNP', 'NNPS']):
            subject += question[i] + " "
            i += 1
    else:
        subject = question[ind] + " "

    return subject


def _getObject(question, subject, verbs):
    object = ""
    qTags = _tokenizeFromStanfordNLP(question)
    # Find the sentence's object
    for word, tag in qTags:
        # This is the subject
        if(word in subject.replace(" ", "") or
           word in verbs):
            continue
        # TODO : add PRP without take care of the subject
        if(tag in ['DT', 'IN', 'JJ', 'NN', 'NNS', 'NNP', 'NNPS']):
            object += ' ' + word
        else:
            if(object != ""):
                break

    return object


def _getVerbs(question, subject):
    qTags = _tokenizeFromStanfordNLP(question)
    verbs = [word for word, tag in qTags
             if (tag in ['VB', 'VBD', 'VBP', 'VBN', 'VBG', 'VBZ', 'MD'] and
                 word != subject.replace(' ', ''))]
    if verbs[0].lower() == 'are' and subject == 'I ':
        verbs[0] = 'am'

    return verbs


def _nounify(verb_word):
    ''' Transform a verb to the closest noun: die -> death '''
    verb_synsets = wn.synsets(verb_word, pos="v")

    # Word not found
    if not verb_synsets:
        return []

    # Get all verb lemmas of the word
    verb_lemmas = [l for s in verb_synsets
                   for l in s.lemmas() if s.name().split('.')[1] == 'v']

    # Get related forms
    derivationally_related_forms = [(l, l.derivationally_related_forms())
                                    for l in verb_lemmas]

    # filter only the nouns
    related_noun_lemmas = [l for drf in derivationally_related_forms
                           for l in drf[1]
                           if l.synset().name().split('.')[1] == 'n']

    # Extract the words from the lemmas
    words = [l.name() for l in related_noun_lemmas]
    len_words = len(words)

    # Build the result in the form of
    # a list containing tuples (word, probability)
    result = [(w, float(words.count(w)) / len_words) for w in set(words)]
    result.sort(key=lambda w: -w[1])

    # return all the possibilities sorted by probability
    return result


class Dialog():
    _classifierTypeQ = None
    _classifierWhQ = None
    _posNegWords = None

    def __init__(self):
        self._posNegWords = learn.dialog.getPosNegWords()
        # load classifiers from pickle file
        self._classifierWhQ = (learn.pickleHandler.
                               load_object('classifierWhQ.pkl'))
        self._classifierTypeQ = (learn.pickleHandler.
                                 load_object('classifierTypeQ.pkl'))
        self._classifierDescOtherQ = (learn.pickleHandler.
                                      load_object('classifierDescOtherQ.pkl'))
        self._classifierDescHQ = (learn.pickleHandler.
                                  load_object('classifierDescHQ.pkl'))
        self._classifierDescWhQ = (learn.pickleHandler.
                                   load_object('classifierDescWhQ.pkl'))
        # self._classifierWhQ = learn.dialog.trainWhQuestion()
        # self._classifierTypeQ = learn.dialog.trainTypeQuestion(1)
        # self._classifierDescOtherQ = learn.dialog.trainWhQuestion(2)
        # self._classifierDescHQ = learn.dialog.trainWhQuestion(3)
        # self._classifierDescWhQ = learn.dialog.trainWhQuestion(4)

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

        newObject = ' '.join([o for o, tag in qTags
                             if tag not in ['DT', 'IN']])
        newObject = newObject[:-1]

        if len(newObject.split()) > 1:
            regObject = '|'.join([o for o in newObject])
        else:
            regObject = newObject

        sent = re.findall(r"([^.]*?" +
                          regObject +
                          "[^.]*\.)", page.summary, re.IGNORECASE)

        if len(sent) == 0 or re.search(r'\bnot|n\'t\b', sent[0]):
            return "No, "
        else:
            return "Yes, "

    def answer(self, question):
        tokens = nltk.word_tokenize(question)
        tokens[0] = tokens[0].lower()
        score = self._getPosNegScore(tokens)

        q = nltk.Text(tokens)

        type = self._classifierTypeQ.classify(
            learn.dialog.dialogue_act_features(question))
        print "Type => " + type
        '''
        if type == "whQuestion":
            whType = self._classifierWhQ.classify(
                learn.dialog.dialogue_act_features(question))
            if whType == "DescriptionOther":
                descriptionType = self._classifierDescOtherQ.classify(
                    learn.dialog.dialogue_act_features(question))
                return ("This question is of type wh and its category is: "
                        + descriptionType)
            if whType == "DescriptionH":
                descriptionType = self._classifierDescHQ.classify(
                    learn.dialog.dialogue_act_features(question))
                return ("This question is of type wh and its category is: "
                        + descriptionType)
            if whType == "DescriptionWh":
                descriptionType = self._classifierDescWhQ.classify(
                    learn.dialog.dialogue_act_features(question))
                return ("This question is of type wh and its category is: "
                        + descriptionType)
            return "This question is of type wh and its category is: " + whType
        '''

        if type == "ynQuestion":
            ans = ""

            # Get the subject
            subject = _getSubject(q, 1)

            # Get the verbs
            verbs = _getVerbs(q, subject)

            # Get the object
            object = _getObject(q, subject, verbs)
            object += "."
            print subject
            print verbs
            print object
            # We need to check the answer : yes or no
            if subject not in ["I ", "you ", "we ",
                               "he ", "she ", "it ", "they "]:
                ans = self._getAnswerFromWikipedia(subject, verbs, object)

            return self._makeYesNoAnswer(subject, verbs, object, score, ans)
        elif type == "whQuestion":

            d = Definition()
            return d.answer(question)
        elif type == "Statement" or type == "Emphasis":
            subject = q[0] + " "
            verbs = _getVerbs(q, subject)
            object = _getObject(q, subject)

            sentence = ""
            if object == " you":
                ending = [" more", " too", ""]
                sentence = (subject + verbs[0] +
                            object + random.choice(ending) + ".")
            return sentence.capitalize()

        else:
            return "I don't know what you mean."


class Definition():

    def __init__(self):
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

    def answer(self, sentence):
        keywords = {'where': ['place', 'city', 'country'],
                    'when': ['date', 'time'],
                    'what': ['thing'],
                    'which': ['thing'],
                    'who': ['person'],
                    'how': ['way', 'means'],
                    'why': ['reason']
                    }

        # Word tokenizer using Stanford NLP Parser (better than NLTK)
        sTags = _tokenizeFromStanfordNLP(sentence)
        print sTags

        # Get the wh? word from the sentence
        whWord = ""
        for word, tag in sTags:
            if "W" in tag:
                whWord = word.lower()
                break

        # Get the object and verb of the sentence
        obj = ' '.join([w[0] for w in sTags if 'NN' in w[1]])
        vb = None
        for w, t in sTags:
            if 'VB' in t and t != 'VB':
                vb = w
            elif t == 'VB':
                vb = w
                break
        # TODO Probability not really good (first element not always the best)
        noun = _nounify(vb)[1][0]
        print noun

        # Perform a search on DBPedia to find the concerned resource
        params = urllib.urlencode({'QueryString': obj,
                                   # 'QueryClass': keywords[whWord][0],
                                   'MaxHints': 1})
        url = "http://lookup.dbpedia.org/api/search/KeywordSearch?" + params
        req = urllib2.Request(url, headers={"Accept": "application/json"})
        response = urllib2.urlopen(req).read()
        # print response
        uri = json.loads(response)["results"][0]["uri"]
        print uri

        # Choose the property regarding the wh? word
        keyword = noun

        if whWord == 'where' or whWord == 'when':
            keyword += keywords[whWord][0]

        properties = difflib.get_close_matches(keyword, self._properties)
        print properties
        pname = 'dbo:' + properties[0]
        filters = ""
        # filters = 'FILTER (langMatches(lang(?pname), "EN"))'
        self._sparql.setQuery("""
            PREFIX dbo: <http://dbpedia.org/ontology/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT ?pname
            WHERE { <%s> %s ?pname %s }""" % (uri, pname, filters))
        results = self._sparql.query().convert()
        print results
        answer = results["results"]["bindings"][0]['pname']['value']
        print answer
        # TODO Check for None
        return answer

        '''
        search = wikipedia.search(obj.strip())
        print search
        page = wikipedia.page(search[0])
        summary = wikipedia.summary(search[0], sentences=1)
        print summary
        '''

        # If no result (return) until here, perform a search on answers.com
        params = urllib.urlencode({'q': sentence})
        req = urllib2.Request("http://wiki.answers.com/search?" + params)
        response = urllib2.urlopen(req, params).read()
        soup = bs4.BeautifulSoup(response)
        results = soup.findAll('div', attrs={'class': 'answer_text'})
        if len(results) > 0:
            return results[0].text.strip()
        else:
            return "I don't know"
