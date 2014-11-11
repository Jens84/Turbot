"""

"""

__version__ = '0.0.1'
__author__ = 'JBO, JES, JRG'
__author_email__ = 'jeremy.rombourg@gmail.com'

import nltk

import learn


class Dialog():
    _classifierTypeQ = None
    _posNegWords = None

    def __init__(self):
        self._classifierTypeQ = learn.dialog.trainTypeQuestion()
        self._posNegWords = learn.dialog.getPosNegWords()

    def answer(self, question):
        type = self._classifierTypeQ.classify(
            learn.dialog.dialogue_act_features(question))

        if type == "ynQuestion":
            tokens = nltk.word_tokenize(question.lower())
            # neutral score
            posNegScore = 0
            # Get score of question (positive/negative)
            for token in tokens:
                if token in self._posNegWords:
                    posNegScore += float(self._posNegWords[token])

            # Find the sentence's verb
            q = nltk.Text(tokens)
            qTags = nltk.pos_tag(q)
            print qTags
            verbs = [word for word, tag in qTags
                     if tag in ['VB', 'VBD', 'VBP', 'VBN', 'VBG', 'VBZ']]

            # Find the sentence's object
            prevWord = None
            prevTag = None
            object = ' '
            for word, tag in qTags:
                if(prevTag == 'DT' and tag in ['NN', 'NNS', 'NNP', 'NNPS']):
                    object += prevWord + ' ' + word
                    break
                if tag in ['NN', 'NNS', 'NNP', 'NNPS']:
                    object += word
                    break
                prevWord = word
                prevTag = tag

            # remove the space if we didn't find an object
            if object == ' ':
                object = ''

            # Answer according to previous results
            if len(verbs) == 1:
                if posNegScore < 0:
                    return "No, I don't " + verbs[0] + object
                else:
                    return "Yes, I " + verbs[0] + object
            elif len(verbs) == 2:
                if posNegScore < 0:
                    return "No, I " + verbs[0] + ' not ' + verbs[1] + object
                else:
                    return "Yes, I " + verbs[0] + ' ' + verbs[1] + object
            else:
                if posNegScore < 0:
                    return "No."
                else:
                    return "Yes !"
        else:
            return "I don't know what you mean."

    def chat(self):
        return ""


class Definition():

    def __new__(class_, turbot):
        return ""
