"""Answering to some sentences.

Examples
--------
>>> turbot.answer('Where was Bjarne Stroustrup born?')
'Bjarne Stroustrup was born in Aarhus.'

"""

from .core import __doc__, __version__, __author__, __author_email__
from .core import answer, sentenceType, questionType
from .nlp import Classify
