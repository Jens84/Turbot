from random import randrange
#import nltk.classify.util


class Markov():
    _chainLength = 2
    _stopWord = '\x03'
    _markovChains = {}

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

    def _getMessage(self, key):
        words_chosen = []

        next_word = ""
        while next_word != self._stopWord:
            words = self._markovChains[key]
            nb_possibilities = len(words)
            next_word = words[randrange(nb_possibilities)]
            words_chosen.append(next_word)

        return words_chosen

    def _getKey(self, sentence):
        # Depends on the sentence
        return sentence

    def input(self, sentence):
        split = self._splitSentence(sentence)
        self._putIntoDictionary(split)

    def output(self, sentence):
        key = self._getKey(sentence)
        return self._getMessage(key)

    def getMarkov(self):
        return self._markovChains

'''
mark = Markov()
posts = nltk.corpus.nps_chat.xml_posts()[:10000]
chat_words = ["JOIN", "QUIT", "PART", "ACTION", "NICK"]
for post in posts[:50]:
    if any(w in post.text for w in chat_words):
        continue
    print post.text
print mark.getMarkov()
'''
