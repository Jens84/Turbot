"""

"""

__version__ = '0.0.1'
__author__ = 'JBO, JES, JRG'
__author_email__ = 'jeremy.rombourg@gmail.com'

import nltk
import urllib
import urllib2
import bs4
import json
import en
import wikipedia
import learn
from learn import markov
import re
import difflib
from SPARQLWrapper import SPARQLWrapper, JSON
from nltk.corpus import wordnet as wn
import operator


def _getSubject(question, ind):
    subject = ""
    qTags = _tokenizeFromStanfordNLP(question)
    if qTags[ind][0].lower() == 'you':
        subject = "I "
    elif qTags[ind][0].lower() == 'i':
        subject = "you "
    elif (qTags[ind][1] == 'DT'
            and (qTags[ind + 1][1] not in
                    ['VB', 'VBD', 'VBP', 'VBN', 'VBG', 'VBZ', 'MD'])):
        subject = qTags[ind][0] + " " + qTags[ind + 1][0] + " "
    elif qTags[ind][1] == 'DT':
        subject = qTags[ind][0] + " "
    elif qTags[ind][1] in ['NNP', 'NNPS']:
        i = ind
        while (qTags[i][1] in ['NNP', 'NNPS']):
            subject += qTags[i][0] + " "
            i += 1
    else:
        subject = qTags[ind][0] + " "

    return subject


def _getObject(question, subject, verbs, isYesNoQuestion):
    object = ""
    qTags = _tokenizeFromStanfordNLP(question)
    print qTags
    # Find the sentence's object
    for word, tag in qTags:
        # This is the subject
        if(word in subject.replace(" ", "") or
           word in verbs or
           word.lower() in ["does", "do"]):
            continue
        if (word == "you" and subject == "I "or
           word == "I" and subject == "you ") and isYesNoQuestion:
            continue
        if(tag in ['DT', 'IN', 'JJ', 'NN', 'NNS', 'NNP', 'NNPS', 'RB', 'PRP']):
            if word.lower() == "me":
                object += ' you'
            else:
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
    elif verbs[0].lower() == 'am' and subject == 'you ':
        verbs[0] = 'are'
    elif (subject.lower() in ["he ", "she ", "it "]
          and verbs[0][len(verbs[0]) - 1] != 's'):
        verbs[0] += "s"

    return [v.lower() for v in verbs]


def _tokenizeFromStanfordNLP(sentence):
    params = urllib.urlencode({'query': sentence})
    req = urllib2.Request("http://nlp.stanford.edu:8080/parser/index.jsp")
    response = urllib2.urlopen(req, params).read()
    soup = bs4.BeautifulSoup(response)
    parsed = soup.find('h3', text='Tagging').find_next('div')
    sTags = []
    for d in parsed.find_all('div'):
        e = d.string.strip().split('/')
        sTags.append((e[0], e[1]))
    return sTags


def _nounify(verb_word):
    ''' Transform a verb to the closest noun: die -> death '''
    verb_synsets = wn.synsets(verb_word, pos="v")

    # Word not found
    if not verb_synsets:
        return []

    # Get all verb lemmas of the word
    verb_lemmas = [l for s in verb_synsets
                   # for l in s.lemmas() if s.name().split('.')[1] == 'v']
                   for l in s.lemmas if s.name.split('.')[1] == 'v']

    # Get related forms
    derivationally_related_forms = [(l, l.derivationally_related_forms())
                                    for l in verb_lemmas]

    # filter only the nouns
    related_noun_lemmas = [l for drf in derivationally_related_forms
                           for l in drf[1]
                           # if l.synset().name().split('.')[1] == 'n']
                           if l.synset.name.split('.')[1] == 'n']

    # Extract the words from the lemmas
    words = [l.name for l in related_noun_lemmas]
    # words = [l.name() for l in related_noun_lemmas]
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
    _markovChains = None
    _markov = None

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
        self._markovChains = (learn.pickleHandler.
                              load_object('markovSentences.pkl'))
        self._markov = markov.Markov(self._markovChains)
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
                notBe = " not "
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

        q = question
        print("Question : " + str(q))

        type = self._classifierTypeQ.classify(
            learn.dialog.dialogue_act_features(question))
        print "Type => " + type

        if type == "ynQuestion":
            ans = ""

            # Get the subject
            subject = _getSubject(q, 1)

            # Get the verbs
            verbs = _getVerbs(q, subject)

            # Get the object
            object = _getObject(q, subject, verbs, True)
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
            whAnswerType = self._classifyWhQuestion(question)
            d = Definition()
            return d.answer(question, whAnswerType)
        elif type == "Statement" or type == "Emphasis":
            if q.split()[0].lower() in ["i"]:
                subject = q.split()[0] + " "
            else:
                subject = _getSubject(q, 0)
            verbs = _getVerbs(q, subject)
            object = _getObject(q, subject, verbs, False)

            print subject
            print verbs
            print object
            '''
            if object == " you" and subject == "I ":
                ending = [" more", " too"]
                sentence = (subject + verbs[0] +
                            object + random.choice(ending) + ".")
            else:

                return self._makeYesNoAnswer(subject, verbs,
                                             object, score, sentence)
            '''
            return self._markov.output(subject, verbs, object)

        else:
            return "I don't know what you mean."

    def _classifyWhQuestion(self, question):
        whType = self._classifierWhQ.classify(
            learn.dialog.dialogue_act_features(question))
        if whType == "DescriptionOther":
            descriptionType = self._classifierDescOtherQ.classify(
                learn.dialog.dialogue_act_features(question))
            return descriptionType
        if whType == "DescriptionH":
            descriptionType = self._classifierDescHQ.classify(
                learn.dialog.dialogue_act_features(question))
            return descriptionType
        if whType == "DescriptionWh":
            descriptionType = self._classifierDescWhQ.classify(
                learn.dialog.dialogue_act_features(question))
            return descriptionType
        return whType


class Definition():
    _sentence = None
    _sTags = []

    def __init__(self):
        self._sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        self._sparql.setReturnFormat(JSON)

    def _getKeywordsFromQuestionType(self, typeOfQuestion):
        keywords = []
        if typeOfQuestion == "Entity":
            keywords.append("comment")
            keywords.append("name")
            keywords.append("description")
            keywords.append("abstract")
        elif typeOfQuestion == "Place":
            keywords.append("place")
            keywords.append("placeOf")
            keywords.append("spot")
        elif typeOfQuestion == "Reason":
            keywords.append("reason")
        elif typeOfQuestion == "Time":
            keywords.append("date")
        elif typeOfQuestion == "Manner":
            keywords.append("transport")
        elif typeOfQuestion == "Dimension":
            pass
        elif typeOfQuestion == "LookAndShape":
            pass
        elif typeOfQuestion == "Composition":
            pass
        elif typeOfQuestion == "Meaning":
            keywords.append("meaning")
            keywords.append("synonyms")
            keywords.append("synonym")
            keywords.append("abstract")
        elif typeOfQuestion == "Abbreviation":
            keywords.append("meaning")
            keywords.append("synonyms")
            keywords.append("synonym")
        elif typeOfQuestion == "Duration":
            keywords.append("duration")
        elif typeOfQuestion == "Age":
            keywords.append("age")
        elif typeOfQuestion == "Quantity":
            pass
        elif typeOfQuestion == "Frequency":
            keywords.append("frequency")

        return keywords

    def _getConcatenationCombinations(self, nouns, additionalKeywords, mode):
        combinations = []
        if mode == 1:
            for i in nouns:
                for j in nouns:
                    if i == j:
                        continue
                    combinations.append(i + j)
        elif mode == 2:
            for i in nouns:
                for j in additionalKeywords:
                    if i == j:
                        continue
                    combinations.append(i + j)
                    combinations.append(j + i)
        return combinations

    def _getOverlappingProperty(self, possibleProperties, propertiesOfSubject):
        matches = []
        for possibleProperty in possibleProperties:
            closeMatches = difflib.get_close_matches(possibleProperty,
                                                     propertiesOfSubject,
                                                     5)
            for match in closeMatches:
                for i in possibleProperties:
                    if i.lower() == match.lower():
                        matches.append(match)
        if matches == []:
            return None
        else:
            return matches

    def _getPropertyName(self, nouns, additionalWords, typeOfQuestion,
                         propertiesOfSubject):

        listOfKeywords = []
        listOfKeywords.extend(nouns)

        nounsMatches = []
        nounsMatches = self._getOverlappingProperty(nouns, propertiesOfSubject)
        print "Temp: Matching nouns: ", nounsMatches

        concatenations = []
        concatenations = self._getConcatenationCombinations(nouns, None, 1)
        print "noun combinations: ", concatenations
        listOfKeywords.extend(concatenations)

        nounsConcatenationsMatches = []
        nounsConcatenationsMatches = self._getOverlappingProperty(
            concatenations, propertiesOfSubject)

        print "Temp: Matching nouns concatenations: ", (
            nounsConcatenationsMatches)

        if nounsConcatenationsMatches is not None:
            print "Temp: Chose property in 1"
            if len(nounsConcatenationsMatches) > 1:
                print "Temp: LOOK: Several Matches1: " + (
                    nounsConcatenationsMatches)
                return nounsConcatenationsMatches[0]
            return nounsConcatenationsMatches[0]

        additionalKeywords = []
        additionalKeywords = self._getKeywordsFromQuestionType(typeOfQuestion)
        additionalKeywords.extend(additionalWords)
        listOfKeywords.extend(additionalKeywords)

        concatenations = []
        concatenations = self._getConcatenationCombinations(nouns,
                                                            additionalKeywords,
                                                            2)
        print "noun+keywords combinations: ", concatenations
        listOfKeywords.extend(concatenations)

        nounsKeywordsConcatenationsMatches = []
        nounsKeywordsConcatenationsMatches = self._getOverlappingProperty(
            concatenations, propertiesOfSubject)

        print "Temp: Matching nouns+keywords concatenations: ", (
            nounsKeywordsConcatenationsMatches)

        if nounsKeywordsConcatenationsMatches is not None:
            print "Temp: Chose property in 2"
            if len(nounsKeywordsConcatenationsMatches) > 1:
                print "Temp: LOOK: Several Matches2: " + (
                    nounsKeywordsConcatenationsMatches)
                return nounsKeywordsConcatenationsMatches[0]
            return nounsKeywordsConcatenationsMatches[0]
        elif nounsMatches is not None:
            print "Temp: Chose property in 3"
            if len(nounsMatches) > 1:
                print "Temp: LOOK: Several Matches3: ", nounsMatches
                return nounsMatches[0]
            return nounsMatches[0]

        print "Temp: Didn't find any match yet."
        print "Temp: Plan B: find closest match."

        # If a match wasn't found yet, a list of all the word combinations will
        # be iterated. Each word will try to be matched with properties. The
        # property that occur the most is chosen
        print "List of all combinations: ", listOfKeywords
        w = 0
        properties = []
        for word in listOfKeywords:
            w += 1
            print "Step: %i" % w
            print "The properties which are close matches for " + (
                word + " are:")
            print difflib.get_close_matches(word, propertiesOfSubject, 10)

            properties.extend(difflib.get_close_matches(word,
                                                        propertiesOfSubject,
                                                        10))

        "The list of all properties is:"
        print properties
        print "----------------------------"

        listOfProperties = properties
        properties = {}
        for proprty in listOfProperties:
            if proprty not in properties:
                properties[proprty] = 0
            properties[proprty] += 1

        # order properties by order of most occurrences
        sorted_x = sorted(properties.items(),
                          key=operator.itemgetter(1),
                          reverse=True)
        i = 0
        listOfProperties = []
        for key, value in sorted_x:
            i += 1
            if i > 10:
                break
            print "Property: >", key, "< with ", value, " occurrences"
            listOfProperties.append(key)
        if listOfProperties == []:
            return listOfProperties
        else:
            return listOfProperties[0]

        '''
        #searching for synonyms. It doesn't work well at all
        synonyms = []
        w=0
        print "List of keywords: ",listOfKeywords
        for keyword in listOfKeywords:
            w+=1
            print "Syn of word number:",w
            for i,j in enumerate(wn.synsets(keyword)):
                print "Synonyms of word ",keyword,":", ", ".join(j.lemma_names)
                synonyms += j.lemma_names
                print "Now the list of synonyms looks like: ",synonyms
                if i == 0:
                    break
        print "\n----------..-----...----.------\n\n"
        listOfKeywords += synonyms

        print listOfKeywords

        w=0
        properties = []
        for word in listOfKeywords:
            w+=1
            print "Step: ",w

            print "The properties which are close matches for ",word, " are:"
            print difflib.get_close_matches(word, propertiesOfSubject,10)

            properties.extend(difflib.get_close_matches(word,
                                                        propertiesOfSubject,
                                                        10))
        "The list of all properties is:"
        print properties
        print "----------------------------"

        listOfProperties = properties
        properties = {}
        for proprty in listOfProperties:
            if proprty not in properties:
                properties[proprty] = 0
            properties[proprty] += 1

        # order properties by order of most occurrences
        sorted_x = sorted(properties.items(),
                          key=operator.itemgetter(1),
                          reverse=True)
        i=0
        for key, value in sorted_x:
            i+=1
            if i>10:
                break
            print "Property: >",key,"< with ",value, " occurrences"

        return properties
        '''

    def _questionToAssertion(self, answer):
        prepositions = {"when": ["on the", "at", "in"],
                        "where": ["in", "at"],
                        "how": ["by"],
                        "who": ["a", "the"],
                        "which": ["the"],
                        "whereby": ["by"],
                        "wherein": ["in"],
                        "whereof": ["of"],
                        "what": ["", "a", "the"]
                        }

        prep = None
        hasAux = False
        vb = None
        subj = None
        cmpl = None

        i = 0
        while 'W' not in self._sTags[i][1]:
            i += 1
        prep = prepositions[self._sTags[i][0].lower()][0]  # First element here
        i += 1
        print "Prep: %s" % prep

        vb = []
        while 'VB' not in self._sTags[i][1]:
            i += 1

        vb.append(self._sTags[i][0])
        i += 1

        if len([w for w, t in self._sTags if "VB" in t]) > 1:
            hasAux = True

        subj = []
        cmpl = [""]
        if hasAux:
            while 'VB' not in self._sTags[i][1]:
                subj.append(self._sTags[i][0])
                i += 1
            print "Subj: %s" % " ".join(subj)
            vb.append(self._sTags[i][0])
            i += 1
            print "Verb: %s" % " ".join(vb)

            while i < len(self._sTags) - 1:
                cmpl.append(self._sTags[i][0])
                i += 1
            print "Cmpl: %s" % " ".join(cmpl)
        else:
            while i < len(self._sTags) - 1:
                subj.append(self._sTags[i][0])
                i += 1
            print "Subj: %s" % " ".join(subj)

        if en.verb.infinitive(vb[0]) == "do":
            if "past" in en.verb.tense(vb[0]):
                vb[1] = en.verb.past(vb[1])
            elif "present" in en.verb.tense(vb[0]):
                vb[1] = en.verb.present(vb[1])
            vb.remove(vb[0])

        subj[0] = subj[0].capitalize()

        return (" ".join(subj) + " " +
                " ".join(vb) + " " +
                prep + " " +
                answer + " ".join(cmpl)) + "."

    def answer(self, sentence, whType):
        print "Temp: Type of this question: " + whType

        # Word tokenizer using Stanford NLP Parser (better than NLTK)
        self._sTags = _tokenizeFromStanfordNLP(sentence)
        print self._sTags

        # Get the object and verb of the sentence
        obj = ' '.join([w[0] for w in self._sTags if 'NNP' in w[1]])

        print "Temp: >Object of sentence: ", obj

        # temporary code
        if obj == []:
            print "Temp: For now, I only answer stuff about known people."

        vb = None
        for w, t in self._sTags:
            if 'VB' in t and t != 'VB':
                vb = w
            elif t == 'VB':
                vb = w
                break

        # TODO Probability not really good (first element not always the best)
        noun = _nounify(vb)[1][0]
        print noun

        # Getting additional information from the sentence: nouns and ajectives
        nouns = []
        adjectives = []
        nouns = [w[0] for w in self._sTags if w[1] == 'NN' or w[1] == 'NNS']
        adjectives = [w[0] for w in self._sTags if 'JJ' in w[1]]

        # Adding the information to the proper lists
        additionalWords = []
        additionalWords.extend(adjectives)
        if not(noun == "having" or noun == "being"):
            nouns.append(noun)

        print "Temp: >Nouns of sentence: ", nouns
        print "Temp: >Adjectives of sentence: ", adjectives

        # Perform a search on DBPedia to find the concerned resource
        params = urllib.urlencode({'QueryString': obj,
                                   # 'QueryClass': keywords[whWord][0],
                                   'MaxHints': 1})
        url = "http://lookup.dbpedia.org/api/search/KeywordSearch?" + params
        req = urllib2.Request(url, headers={"Accept": "application/json"})
        response = json.loads(urllib2.urlopen(req).read())

        # If we found a resource to analyze
        if len(response["results"]) > 0:
            uri = response["results"][0]["uri"]
            print uri

            # Get the list of properties for this resoruce
            self._sparql.setQuery("""
                SELECT DISTINCT ?p
                WHERE { <%s> ?p ?o . }""" % uri)
            props = self._sparql.query().convert()["results"]["bindings"]

            # Generate a dictionary of properties
            properties = {}
            for p in props:
                puri = p['p']["value"]
                pname = puri.split('/')[-1].split('#')[-1]
                properties[pname] = puri

            # Choose property regarding the wh? word (ontology, property, rdf)

            # Find property that best matches what the sentence asks for
            proprty = self._getPropertyName(nouns,  # has to be a list
                                            additionalWords,
                                            whType,
                                            properties.keys())

            # Converting list prop unicode single entry to plain string proprty
            # check if it breaks! any problem with unicode and encodings??
            type(proprty)
            print "Temp: I am going to use this property: " + proprty

            # if found a property match
            if len(proprty) > 0:
                # Find close matches for our keyword and available properties
                matches = difflib.get_close_matches(proprty,
                                                    properties.keys(),
                                                    3)
                # Pick the best match
                pname = properties[matches[0]]

                # query the database for the best property value
                query = """
                    PREFIX owl: <http://www.w3.org/2002/07/owl#>
                    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                    PREFIX dc: <http://purl.org/dc/elements/1.1/>
                    PREFIX : <http://dbpedia.org/resource/>
                    PREFIX dbpedia2: <http://dbpedia.org/property/>
                    PREFIX dbpedia: <http://dbpedia.org/>
                    PREFIX dbo: <http://dbpedia.org/ontology/>
                    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                    SELECT ?pname
                    WHERE { <%s> <%s> ?pname }""" % (uri, pname)
                self._sparql.setQuery(query)
                results = self._sparql.query().convert()["results"]["bindings"]

                # If there is a result (supposed to) then return the value
                if len(results) > 0:
                    for r in results:
                        if ("xml:lang" not in r["pname"] or
                           r["pname"]["xml:lang"] == "en"):
                            # Retrieve name/label/abstract from db if needed
                            if r["pname"]["type"] == "uri":
                                uri = r["pname"]["value"]
                                query = """
                           PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                           SELECT ?pname
                           WHERE { <%s> rdfs:label ?pname }""" % uri
                                self._sparql.setQuery(query)
                                results = (self._sparql.query().convert()
                                           ["results"]["bindings"])
                                answer = results[0]["pname"]["value"]
                            else:
                                answer = r["pname"]["value"]

                            print answer

                            newObject = ([o for o, tag in self._sTags
                                          if tag not in ['DT', 'IN',
                                                         'WDT', 'WP',
                                                         'WP$', 'WRB']])
                            newObject = newObject[:-1]
                            print ("NO: " + " ".join(newObject))

                            sentences = re.findall(r"([^.]*\.)", answer)
                            for sentence in sentences:
                                if all(word in sentence for word in newObject):
                                    answer = sentence
                                    break

                            if "comment" not in pname:
                                return self._questionToAssertion(answer)
                            else:
                                return answer

        # If no result (return) until here, perform a search on answers.com
        params = urllib.urlencode({'q': sentence})
        req = urllib2.Request("http://wiki.answers.com/search?" + params)
        response = urllib2.urlopen(req, params).read()
        soup = bs4.BeautifulSoup(response)
        results = soup.findAll('div', attrs={'class': 'answer_text'})
        if len(results) > 0:
            print "Temp: Used wiki answers."
            return results[0].text.strip()
        else:
            return "I don't know"
