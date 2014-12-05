Definition
***********
from .nlp import tokenizeFromStanfordNLP, nounify
import difflib
import operator
import json
import en
import re
import urllib
import urllib2
import bs4
from nltk import wordnet as wn
from SPARQLWrapper import SPARQLWrapper, JSON


class Definition():
    _sentence = None
    _sTags = []

    def __init__(self):
        self._sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        self._sparql.setReturnFormat(JSON)

    def _getKeywordsFromQuestionType(self, typeOfQuestion):
        """Return a list of keywords related to a question label.

        Argument:
        typeOfQuestion -- label of a question

        Return values:
        List of strings where each element is a word related to the given
        question label
        """
        # Depending on the type of question, different keywords will be
        # associated with it
        keywords = []
        if typeOfQuestion == "Entity":
            keywords.append("comment")
            keywords.append("name")
            keywords.append("description")
            keywords.append("abstract")
            keywords.append("title")
        elif typeOfQuestion == "Place":
            keywords.append("place")
            keywords.append("placeOf")
            keywords.append("spot")
        elif typeOfQuestion == "Reason":
            keywords.append("reason")
        elif typeOfQuestion == "TimeWhat":
            keywords.append("date")
        elif typeOfQuestion == "TimeWhen":
            keywords.append("date")
        elif typeOfQuestion == "Manner":
            keywords.append("transport")
        elif typeOfQuestion == "Dimension":
            keywords.append("size")
            keywords.append("unit")
            keywords.append("length")
            keywords.append("height")
            keywords.append("volume")
            keywords.append("distance")
        elif typeOfQuestion == "LookAndShape":
            keywords.append("shape")
            keywords.append("aspet")
            keywords.append("look")
        elif typeOfQuestion == "Composition":
            keywords.append("composition")
            keywords.append("content")
            keywords.append("constitution")
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
            keywords.append("number")
            keywords.append("amount")
            keywords.append("capacity")
        elif typeOfQuestion == "Frequency":
            keywords.append("frequency")

        return keywords

    def _getConcatenationCombinations(self, nouns, additionalKeywords, mode):
        """Return a list of combination of words.

        Return a list of combination of nouns if mode == 1.
        Return a list of combination of nouns with other words if mode ==2.

        Arguments:
        nouns -- list of words
        additionalKeywords -- list of words

        Return values:
        List of strings where each element is a combination of words given as
        arguments

        Restrictions:
        nouns has to be a list of strings
        additionalWords has to be a list of strings
        """
        combinations = []
        if mode == 1:
            for i in nouns:
                for j in nouns:
                    if i == j:
                        continue
                    # Adding concation of nouns to the list
                    combinations.append(i + j)
        elif mode == 2:
            for i in nouns:
                for j in additionalKeywords:
                    if i == j:
                        continue
                    # Adding concatenation of keywords before and after the
                    # nouns to the list
                    combinations.append(i + j)
                    combinations.append(j + i)
        return combinations

    def _getOverlappingProperty(self, possibleProperties, propertiesOfSubject):
        """
        Return a list of strings that match an element on list of properties.

        Return a list of properties that match an extensive list of DBpedia
        properties.

        Arguments:
        possibleProperties -- list of properties
        propertiesOfSubject -- list of DBpedia properties

        Return values:
        List of properties that have a match

        Restrictions:
        possibleProperties has to be a list of strings
        propertiesOfSubject has to be a list of strings
        """
        matches = []
        for possibleProperty in possibleProperties:
            # Getting close matches from a list of properties
            closeMatches = difflib.get_close_matches(possibleProperty,
                                                     propertiesOfSubject,
                                                     5)
            # Checking if a candidate property matches exactly one property
            # the list that was checked as being similar to it
            for match in closeMatches:
                for i in possibleProperties:
                    # Candidate property is added to the list if it is a
                    # perfect match
                    if i.lower() == match.lower():
                        matches.append(match)
        if matches == []:
            return None
        else:
            return matches

    def _getPropertyName(self, nouns, additionalWords, typeOfQuestion,
                         propertiesOfSubject):
        """Return the DBpedia property name that best fits given arguments.

        Return one property from the list of properties given that is the best
        fit for all the words given and the type of the question.

        Arguments:
        nouns -- list of nouns from a sentence
        additionalWords -- list of additional words from a sentence
        typeOfQuestion -- a question label
        propertiesOfSubjectlistOfStrings -- list of properties from a DBpedia
                page

        Return values:
        List of original words and additional related words

        Restrictions:
        nouns has to be a list of strings
        additionalWords has to be a list of strings
        """
        # Elements are added to the listOfKeywords because they are meaningful
        listOfKeywords = []
        listOfKeywords.extend(nouns)

        # Getting perfect matches of nouns
        nounsMatches = []
        nounsMatches = self._getOverlappingProperty(nouns, propertiesOfSubject)

        # Getting concatenations of nouns
        concatenations = []
        concatenations = self._getConcatenationCombinations(nouns, None, 1)
        # Elements are added to the listOfKeywords because they are meaningful
        listOfKeywords.extend(concatenations)

        # Getting perfect matches of nouns concatenations
        nounsConcatenationsMatches = []
        nounsConcatenationsMatches = self._getOverlappingProperty(
            concatenations, propertiesOfSubject)

        if nounsConcatenationsMatches is not None:
            # TODO delete this if???
            # First priority is given to perfect matches of nouns concatenation
            if len(nounsConcatenationsMatches) > 1:
                return nounsConcatenationsMatches[0]
            return nounsConcatenationsMatches[0]

        # Getting keywords associated with the type of question
        additionalKeywords = []
        additionalKeywords = self._getKeywordsFromQuestionType(typeOfQuestion)
        # List of adjectives is merged with list of type of question keywords
        additionalKeywords.extend(additionalWords)
        # Elements are added to the listOfKeywords because they are meaningful
        listOfKeywords.extend(additionalKeywords)

        # Getting concatenations of nouns with keywords
        concatenations = []
        concatenations = self._getConcatenationCombinations(nouns,
                                                            additionalKeywords,
                                                            2)
        # Elements are added to the listOfKeywords because they are meaningful
        listOfKeywords.extend(concatenations)

        # Getting perfect matches of concatenations of nouns with keywords
        nounsKeywordsConcatenationsMatches = []
        nounsKeywordsConcatenationsMatches = self._getOverlappingProperty(
            concatenations, propertiesOfSubject)

        if nounsKeywordsConcatenationsMatches is not None:
            # Second priority is given to perfect matches of concatenation of
            # noun with keyword
            # TODO delete if????
            if len(nounsKeywordsConcatenationsMatches) > 1:
                nounsKeywordsConcatenationsMatches
                return nounsKeywordsConcatenationsMatches[0]
            return nounsKeywordsConcatenationsMatches[0]
        elif nounsMatches is not None:
            # Third priority is given to perfect matches of single nouns
            # TODO delete if????
            if len(nounsMatches) > 1:
                return nounsMatches[0]
            return nounsMatches[0]

        # Getting synonyms of the nouns on the question, which may help
        # getting the right property
        synonyms = []
        synonyms = self._getSynonyms(nouns)
        listOfKeywords.extend(synonyms)

        # If a match was not found yet, a list of all the word combinations
        # will be iterated. Each word will try to be matched with properties.
        # The property that occurs the most is chosen.
        properties = []
        for word in listOfKeywords:
            properties.extend(difflib.get_close_matches(word,
                                                        propertiesOfSubject,
                                                        2))

        # It is created a dictionary in which each key is a property and the
        # associated value is the number of times it was found as a possible
        # match
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

        # Convert the sorted dictionary into a list and exclude the very common
        # entry "abstract" if it was the one with most occurrences, but not the
        # only one on the list
        i = 0
        listOfProperties = []
        for key, value in sorted_x:
            i += 1
            if i > 10:
                break
            listOfProperties.append(key)
        if listOfProperties == []:
            return listOfProperties
        elif listOfProperties[0] == "abstract" and (
                len(listOfProperties) > 1 and sorted_x[1][1] > 1):
            return listOfProperties[1]
        else:
            return listOfProperties[0]

    def _getSimpleWords(self, listOfStrings):
        """Return a list containing words related to the ones given.

        Return a list containing the original list of words and possibly
        others. Words are split if they are recognized as common english
        compound words.

        Arguments:
        listOfStrings -- list of elements of type str

        Return values:
        List of original words and additional split words

        Restrictions:
        listOfStrings hast to be a list of strings
        """
        # listOfStrings is a list of nouns
        substrings = ["day", "date", "place", "name"]

        # Searching for common substrings in nouns that are combinations
        # of two words and splits them
        for string in listOfStrings:
            if type(string) is str or type(string) is unicode:
                # Search for every common substring in the string
                for substring in substrings:
                    if (string.lower().find(substring) != -1 and
                            string is not substring):
                        newStrings = string.lower().split(substring)
                        # Check if newStrings is one string or a list of
                        # strings
                        if (type(newStrings) is str or
                                type(newStrings) is unicode):
                            listOfStrings.append(newStrings)
                        else:
                            for newString in newStrings:
                                # Only adds non empty strings
                                if (newString is not '' and
                                        newString is not unicode('')):
                                    listOfStrings.append(newString)
                        # We also add the substring found
                        listOfStrings.append(substring)
                    else:
                        pass
            # If string is not of type str or unicode
            else:
                pass
        return listOfStrings

    def _getSynonyms(self, listOfStrings):
        """Return a list containing original words and their synonyms.

        Arguments:
        listOfStrings -- list of elements of type str

        Return values:
        List of the original words and their synonyms
        """
        # Searching synonyms of the words in listOfStrings
        synonyms = []
        for word in listOfStrings:
            for i, j in enumerate(wn.synsets(word)):
                w = 0
                for synonym in j.lemma_names():
                    w += 1
                    if word.lower() != synonym.lower():
                        synonyms.append(synonym)
                    if w > 2:
                        break
                # Allows only sysnonyms for one meaning of the word
                if i == 0:
                    break
            # Special case: it is important the synonym leader for "president"
            # in DBpedia
            if word.lower().find("president") != -1:
                synonyms.append("leader")

        listOfStrings += synonyms
        return listOfStrings

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
        # print "Prep: %s" % prep

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
            # print "Subj: %s" % " ".join(subj)
            vb.append(self._sTags[i][0])
            i += 1
            # print "Verb: %s" % " ".join(vb)

            while i < len(self._sTags) - 1:
                cmpl.append(self._sTags[i][0])
                i += 1
            # print "Cmpl: %s" % " ".join(cmpl)
        else:
            while i < len(self._sTags) - 1:
                subj.append(self._sTags[i][0])
                i += 1
            # print "Subj: %s" % " ".join(subj)

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
        # print "Temp: Type of this question: ", whType, " <<<\n"

        # Word tokenizer using Stanford NLP Parser (better than NLTK)
        self._sTags = tokenizeFromStanfordNLP(sentence)
        # print self._sTags

        # Get the object and verb of the sentence
        obj = ' '.join([w[0] for w in self._sTags if 'NNP' in w[1]])

        # print "Temp: >Object of sentence: ", obj

        # temporary code
        # if obj == []:
        # print "Temp: For now, I only answer stuff about known people."

        vb = None
        for w, t in self._sTags:
            if 'VB' in t and t != 'VB':
                vb = w
            elif t == 'VB':
                vb = w
                break
        # print vb

        if vb is not None:
            # verb 's is considered to be is
            if vb == "'s":
                vb = "is"
            # TODO Probably not really good (first element not always the best)
            noun = nounify(vb)[1][0]

        # Getting additional information from the sentence: nouns and ajectives
        nouns = []
        adjectives = []
        nouns = [w[0] for w in self._sTags if w[1] == 'NN' or w[1] == 'NNS']
        adjectives = [w[0] for w in self._sTags if 'JJ' in w[1]]

        # Adding the information to the proper lists
        additionalWords = []
        if not(noun == "having" or noun == "being"):
            nouns.append(noun)

        nouns = self._getSimpleWords(nouns)

        additionalWords.extend(adjectives)

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
            proprty = self._getPropertyName(nouns,
                                            additionalWords,
                                            whType,
                                            properties.keys())

            # If found a property match, we will find which one it is
            if len(proprty) > 0:
                # Find close matches for our keyword and available properties
                matches = difflib.get_close_matches(proprty,
                                                    properties.keys(),
                                                    3)
                # Pick the best match
                pname = properties[matches[0]]

                # query the database for the value of the property that had the
                # best match
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

                # If there is (supposed to be) a result, then return the value
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

                            newObject = ([o for o, tag in self._sTags
                                          if tag not in ['DT', 'IN',
                                                         'WDT', 'WP',
                                                         'WP$', 'WRB']])
                            newObject = newObject[:-1]

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
            return results[0].text.strip()
        else:
            # Answers.com could not return an answer either
            return "I don't know"
