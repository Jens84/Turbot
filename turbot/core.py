from .definition import Definition
from .dialog import Dialog
from .nlp import Classify

__version__ = '0.0.1'
__author__ = 'JBO, JES, JRG'
__author_email__ = 'jeremy.rombourg@gmail.com'


class Turbot():
    _c = None
    _de = None
    _di = None

    def __init__(self):
        self._c = Classify()
        self._de = Definition()
        self._di = Dialog()

    def answer(self, sentence):
        # Classify general type of the question
        qType = self.sentenceType(sentence)

        if qType == "whQuestion":
            whAnswerType = self.questionType(sentence)
            return self._de.answer(sentence, whAnswerType)
        else:
            return self._di.answer(sentence, qType)

    def sentenceType(self, sentence):
        qType = self._c.classifyTypeQuestion(sentence)
        return qType

    def questionType(self, question):
        whAnswerType = self._c.classifyWhQuestion(question)
        return whAnswerType

    def getClassifier(self):
        return self._c
