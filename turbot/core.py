"""

"""

__version__ = '0.0.1'
__author__ = 'JBO, JES, JRG'
__author_email__ = 'jeremy.rombourg@gmail.com'

import nltk
import en

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
                     if tag in ['VB', 'VBD', 'VBP', 'VBN', 'VBG', 'VBZ', 'MD']]

            # Find the sentence's object
            prevWord = None
            prevTag = None
            object = ' '
            for word, tag in qTags:
                if(prevTag in ['DT', 'IN', 'JJ']
                   and tag in ['NN', 'NNS', 'NNP', 'NNPS']):
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

            # Subject
            if posNegScore < 0:
                ans = "No, "
            else:
                ans = "Yes, "

            if q[1].lower() == 'you':
                subject = ans + "I "
                if verbs[0].lower() == 'are':
                    verbs[0] = 'am'
            elif q[1].lower() == 'i':
                subject = ans + "you "
            else:
                subject = ans + q[1] + " "

            # Answer according to previous results
            if len(verbs) == 1:
                if posNegScore < 0:
                    if verbs[0].lower() in ['am', 'are', 'is']:
                        return subject + verbs[0] + " not " + object
                    else:
                        return subject + "don't " + verbs[0] + object
                else:
                    return subject + verbs[0] + object
            elif len(verbs) == 2:
                if verbs[0].lower() == 'do':
                    verbs[0] = ''
                if verbs[0].lower() == 'did':
                    verbs[0] = ''
                    verbs[1] = en.verb.past(verbs[1])
                if verbs[0].lower() == 'will':
                    verbs[0] = 'will'
                if posNegScore < 0:
                    return subject + verbs[0] + ' not ' + verbs[1] + object
                else:
                    return subject + verbs[0] + ' ' + verbs[1] + object
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
