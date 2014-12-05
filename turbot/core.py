""" Module that wraps the main classes of the project.

This class contains the entry points for the bot itself.

Classes:
Turbot
"""

from .definition import Definition
from .dialog import Dialog
from .nlp import Classify

__version__ = '0.0.1'
__author__ = 'JBO, JES, JRG'
__author_email__ = 'jeremy.rombourg@gmail.com'


class Turbot():

    """Bot that answers questions.

    Attributes:
    _c -- Classify object
    _de -- Definition object
    _di -- Dialog object
    """

    _c = None
    _de = None
    _di = None

    def __init__(self):
        """Constructor of Turbot.

        We create all objects we need (Classifiers, Definition, Dialog)
        """
        self._c = Classify()
        self._de = Definition()
        self._di = Dialog()

    def answer(self, sentence):
        """Make an answer thanks to turbot.

        Arguments:
        sentence -- input we have to answer.

        Return values:
        string answer
        """
        # Classify general type of the question
        qType = self.sentenceType(sentence)

        if qType == "whQuestion":
            whAnswerType = self.questionType(sentence)
            return self._de.answer(sentence, whAnswerType)
        else:
            return self._di.answer(sentence, qType)

    def sentenceType(self, sentence):
        """Compute the sentence's type thanks to classifier.

        Arguments:
        sentence -- input we have to classify.

        Return values:
        type sentence
        """
        qType = self._c.classifyTypeQuestion(sentence)
        return qType

    def questionType(self, question):
        """Compute the what question's type thanks to classifier.

        Arguments:
        sentence -- input we have to classify.

        Return values:
        type what question
        """
        whAnswerType = self._c.classifyWhQuestion(question)
        return whAnswerType

    def getClassifier(self):
        """Return the classifier object.

        Arguments:
        -

        Return values:
        classifier object
        """
        return self._c
