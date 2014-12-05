from .definition import Definition
from .dialog import Dialog
from .nlp import Classify

__version__ = '0.0.1'
__author__ = 'JBO, JES, JRG'
__author_email__ = 'jeremy.rombourg@gmail.com'


def answer(sentence):
    # Classify general type of the question
    c = Classify()
    qType = sentenceType(sentence, c)

    if qType == "whQuestion":
        whAnswerType = questionType(sentence, c)
        d = Definition()
        return d.answer(sentence, whAnswerType)
    else:
        d = Dialog()
        return d.answer(sentence, qType)


def sentenceType(sentence, c=None):
    if c is None:
        c = Classify()
    qType = c.classifyTypeQuestion(sentence)
    return qType


def questionType(question, c=None):
    if c is None:
        c = Classify()
    whAnswerType = c.classifyWhQuestion(question)
    return whAnswerType
