"""

"""

__version__ = '0.0.1'
__author__ = 'JBO, JES, JRG'
__author_email__ = 'jeremy.rombourg@gmail.com'

import nltk
import random

import learn
from learn import *


class Dialog():
    _classifierTypeQ = None

    def __init__(self):
        self._classifierTypeQ = learn.dialog.trainTypeQuestion()

    def answer(self, question):
        type = self._classifierTypeQ.classify(
            learn.dialog.dialogue_act_features(question))

        if type == "ynQuestion":
            tokens = nltk.word_tokenize(question.lower())
            q = nltk.Text(tokens)
            qTags = nltk.pos_tag(q)
            print qTags
            verbs = [word for word, tag in qTags if tag == 'VB']
            print verbs
            yesNo = ['Yes', 'No']
            if len(verbs) == 1:
                return random.choice(yesNo) + ", I do !"
        else:
            return "I don't know what you mean."

    def chat(self):
        return ""


class Definition():

    def __new__(class_, turbot):
        return ""
