from random import randrange
import glob
import os
import re


class Markov():
    _chainLength = 2
    _stopWord = '\x03'
    _markovChains = {}

    def __init__(self, markovChains={}):
        if markovChains:
            self._markovChains = markovChains
            return

        current_dir = os.getcwd()
        for file in glob.glob(current_dir + '/book_*.txt'):
            with open(file, 'r') as f:
                data = " ".join(f.read().splitlines())
                for sentence in re.split(r"[!?\.]+", data):
                    self.input(sentence.lstrip()
                               .replace("\"", "").replace("'", ""))

    def _splitSentence(self, sentence):
        words = sentence.split(' ')

        if len(words) < self._chainLength:
            yield -1

        words.append(self._stopWord)
        for i in range(len(words) - self._chainLength):
            yield words[i:i + self._chainLength + 1]

    def _putIntoDictionary(self, split):
        for w in split:
            if w == -1:
                break
            key = (w[0], w[1])
            if not key in self._markovChains:
                self._markovChains[key] = [w[2]]
            else:
                self._markovChains[key].append(w[2])

    def _getMessage(self, key, object):
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
        (w1, w2) = key
        return (w2, next_word)

    def _getInitKey(self, subject, verbs):
        for w1, w2 in self._markovChains.keys():
            if (w1.lower().replace(" ", "") == subject.lower().replace(" ", "")
                    and w2.lower() in verbs):
                return (w1, w2)

    def input(self, sentence):
        split = self._splitSentence(sentence)
        self._putIntoDictionary(split)

    def output(self, subject, verbs, object):
        key = self._getInitKey(subject, verbs)
        return ' '.join(self._getMessage(key, verbs)[:-1]) + "."

    def getMarkov(self):
        return self._markovChains
