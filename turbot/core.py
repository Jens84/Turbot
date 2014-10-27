"""Answering to some sentences.

Examples
--------
>>> Turbot('How are you?')
'Fine, and you?'

"""
__version__ = '0.0.1'
__author__ = 'JBO, JES, JRG'
__author_email__ = 'jeremy.rombourg@gmail.com'


class Turbot(str):

	"""Turbot sentence"""

	def __new__(class_, turbot):
		"""Construct new Turbot answer from string."""
		return "Fine, and you?"
