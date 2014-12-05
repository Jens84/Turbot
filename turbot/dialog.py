Dialog
*******
from .nlp import getSubject, getObject, getVerbs
import nltk
import learn
from learn import markov
import re
import en
import wikipedia


class Dialog():
    """
    Attributes:
    _posNegWords -- list of words and their happiness score
    _markovChains -- Dictionary representing markov chains
    _markov -- Markov object itself
    """
    _posNegWords = None
    _markovChains = None
    _markov = None

    def __init__(self):
        """Constructor of Dialog.
           We create all objects we need (happiness list and Markov chains)
        """
        self._posNegWords = learn.pickleHandler.load_object('posNegWords.pkl')
        self._markovChains = (learn.pickleHandler.
                              load_object('markovSentences.pkl'))
        self._markov = markov.Markov(self._markovChains)

    def _getPosNegScore(self, tokens):
        """Return the happiness of a sentence.

        Arguments:
        tokens -- sentence tokenized.

        Return values:
        int score
        """
        # neutral score
        posNegScore = 0
        # Get score of question (positive/negative)
        for token in tokens:
            if token in self._posNegWords:
                posNegScore += float(self._posNegWords[token])
        return posNegScore

    def _makeYesNoAnswer(self, subject, verbs, object, score, ans):
        """Construct a yes/no answer.

        Arguments:
        subject -- subject of sentence we already found.
        verbs -- verbs of sentence we already found.
        object -- object of sentence we already found.
        score -- happiness score of sentence we already computed.
        ans -- begin of the answer we will return.

        Return values:
        string ans
        """
        # Get the subject and negation or not
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

        # Answer according to previous results and number of verbs
        if len(verbs) == 1:
            if verbs[0].lower() in ['am', 'are', 'is']:
                notDo = ""
            else:
                notBe = ""

            return re.sub(r'\s+', ' ',
                          subject + notDo + verbs[0] + notBe + object)
        # according to time
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
        # default case
        else:
            if score < 0:
                return "No."
            else:
                return "Yes !"

    def _getAnswerFromWikipedia(self, subject, verbs, object):
        """Search an answer to yes/no question on wikipedia.

        Arguments:
        subject -- subject of sentence we already found.
        verbs -- verbs of sentence we already found.
        object -- object of sentence we already found.

        Return values:
        string yes or no
        """
        # Get closest page from subject
        page = wikipedia.page(wikipedia.search(subject)[0])

        tokens = nltk.word_tokenize(object)
        t = nltk.Text(tokens)
        qTags = nltk.pos_tag(t)

        # Remove determinants of object and ponctuation
        newObject = ' '.join([o for o, tag in qTags
                             if tag not in ['DT', 'IN']])
        newObject = newObject[:-1]

        # Find a sentence according to the object in summary of the
        # wiki page
        if len(newObject.split()) > 1:
            regObject = '|'.join([o for o in newObject])
        else:
            regObject = newObject

        sent = re.findall(r"([^.]*?" +
                          regObject +
                          "[^.]*\.)", page.summary, re.IGNORECASE)

        # Check if the sentence is negative or not
        if len(sent) == 0 or re.search(r'\bnot|n\'t\b', sent[0]):
            return "No, "
        else:
            return "Yes, "

    def answer(self, sentence, type):
        """Main function of dialog to answer.

        Arguments:
        sentence -- string we have to answer.
        type -- type of the sentence found.

        Return values:
        string final answer
        """
        tokens = nltk.word_tokenize(sentence)
        tokens[0] = tokens[0].lower()
        score = self._getPosNegScore(tokens)

        s = sentence

        # Yes/No question type
        if type == "ynQuestion":
            ans = ""

            # Get the subject
            subject = getSubject(s, 1)

            # Get the verbs
            verbs = getVerbs(s, subject)

            # Get the object
            object = getObject(s, subject, verbs, True)
            object += "."

            # We need to check the answer : yes or no
            if subject not in ["I ", "you ", "we ",
                               "he ", "she ", "it ", "they "]:
                ans = self._getAnswerFromWikipedia(subject, verbs, object)

            return self._makeYesNoAnswer(subject, verbs, object, score, ans)
        # Statement or Emphasis
        elif type == "Statement" or type == "Emphasis":
            # Get subject, verbs and object
            if s.split()[0].lower() in ["i"]:
                subject = s.split()[0] + " "
            else:
                subject = getSubject(s, 0)
            verbs = getVerbs(s, subject)
            object = getObject(s, subject, verbs, False)

            # Build a markov sentence based on subject, verbs, object
            return self._markov.output(subject, verbs, object)

        else:
            return "I don't know what you mean."
