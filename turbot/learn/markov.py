
"""Module that generate Markov chains.

Functions:
_splitSentence -- split a sentence according to the chain's length
_putIntoDictionary -- add sentence in Markov chains dictionary
_getMessage -- get message from dictionary based on Markov concept
_getNextKey -- get next key to pick in dictionary
_getInitKey -- get first key to pick according to subject, verb
input -- add an input in Markov Chains (in order to train)
output -- get a generated sentence from Markov Chains
getMarkov -- return the Markov Chains object
"""

from random import randrange
from random import choice
import glob
import os
import re


class Markov():

    """ Class that handles Markov Chains.

    Attributes:
    _chainLength -- length of a chain (number of words)
                    in Markov implementation.
    _stopWord -- special character in order to separate two words.
    _markovChains -- Markov chains object where we store each input.

    Functions:
    _splitSentence
    _putIntoDictionary
    _getMessage
    _getNextKey
    _getInitKey
    input ------------ > cannot be input
    output
    getMarkov
    """

    _chainLength = 2
    _stopWord = '\x03'
    _markovChains = {}

    def __init__(self, markovChains={}):
        """ Constructor of Markov Chains.

        We enrich them thanks to books dataset.
        """
        if markovChains:
            self._markovChains = markovChains
            return

        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))

        for file in glob.glob(__location__ + '/book_*.txt'):
            with open(file, 'r') as f:
                data = " ".join(f.read().splitlines())
                for sentence in re.split(r"[!?\.]+", data):
                    self.input(sentence.lstrip()
                               .replace("\"", "").replace("'", ""))

    def _splitSentence(self, sentence):
        """Split a sentence in a Markov chain based on _chainLength attribute.

        Arguments:
        sentence -- string to split
        """
        words = sentence.split(' ')

        if len(words) < self._chainLength:
            yield -1

        words.append(self._stopWord)
        for i in range(len(words) - self._chainLength):
            yield words[i:i + self._chainLength + 1]

    def _putIntoDictionary(self, split):
        """Add into the Markov chains dictionary a new value splitted.

        Arguments:
        split -- string already splitted to add.
        """
        for w in split:
            if w == -1:
                break
            key = (w[0], w[1])
            if key not in self._markovChains:
                self._markovChains[key] = [w[2]]
            else:
                self._markovChains[key].append(w[2])

    def _getMessage(self, key, object):
        """Generate a message from Markov chains.

        Arguments:
        key -- The initial key we have to begin the chain.
        object -- object of the sentence in order to increase
                  chance to pick a chain which contains the object.

        Return values:
        string generated
        """
        words_chosen = [key[0], key[1]]
        next_word = ""
        tryCorrelation = False
        while next_word != self._stopWord:

            words = self._markovChains[key]
            nb_possibilities = len(words)
            if not tryCorrelation:
                for w in words:
                    if w.lower() in object:
                        next_word = w
                        tryCorrelation = True
            if not tryCorrelation:
                next_word = words[randrange(nb_possibilities)]
            words_chosen.append(next_word)
            key = self._getNextKey(key, next_word)
        return words_chosen

    def _getNextKey(self, key, next_word):
        """Select the next key to pick.

        Arguments:
        key -- the current key.
        next_word -- the next_word chosen.

        Return values:
        key value
        """
        (w1, w2) = key
        return (w2, next_word)

    def _getInitKey(self, subject, verbs):
        """Select the initial key to pick.

        Arguments:
        subject -- subject of the sentence in order to increase
                   chance to pick a key which contains the object.
        verbs -- verbs of the sentence in order to increase
                 chance to pick a key which contains the object.

        Return values:
        key value
        """
        for w1, w2 in self._markovChains.keys():
            if (w1.lower().replace(" ", "") == subject.lower().replace(" ", "")
                    and w2.lower() in verbs):
                return (w1, w2)

        (w1, w2) = choice(self._markovChains.keys())
        while not w1[0].isupper():
            (w1, w2) = choice(self._markovChains.keys())
        return (w1, w2)

    # TODO change name of function. Can't be input
    def input(self, sentence):
        """Add a sentence in Markov chains.

        Arguments:
        sentence -- the sentence to add.
        """
        split = self._splitSentence(sentence)
        self._putIntoDictionary(split)

    def output(self, subject, verbs, object):
        """Generate a sentence from Markov chains.

        Arguments:
        subject -- subject of the sentence.
        verbs -- verbs of the sentence.
        object -- object of the sentence.

        Return values:
        string generated
        """
        key = self._getInitKey(subject, verbs)
        return ' '.join(self._getMessage(key, verbs)[:-1]) + "."

    def getMarkov(self):
        """Get Markov chains object.

        Return values:
        markov object
        """
        return self._markovChains
