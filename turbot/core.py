"""

"""

__version__ = '0.0.1'
__author__ = 'JBO, JES, JRG'
__author_email__ = 'jeremy.rombourg@gmail.com'

import learn
from learn import *


class Dialog():
    _classifierTypeQ = None

    def __init__(self):
        self._classifierTypeQ = learn.dialog.trainTypeQuestion()

    def answer(self, question):
        return self._classifierTypeQ.classify(
            learn.dialog.dialogue_act_features(question))


class Definition():

    def __new__(class_, turbot):
        return ""
