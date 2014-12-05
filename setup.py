import os
import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand

import turbot


class ToxTestCommand(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        sys.exit(os.system('tox'))


setup(
    name=turbot.__name__,
    version=turbot.__version__,
    author=turbot.__author__,
    author_email=turbot.__author_email__,
    description=turbot.__doc__,
    license='',
    keywords='turbot',
    url='http://github.com/Jens84/Turbot',
    packages=['en', 'en/wordnet', 'en/verb', 'en/spelling',
              'en/ogden', 'turbot', 'turbot/learn'],
    package_data={'turbot/learn': ['*.txt', '*.pkl'],
                  'en/wordnet': ['wordnet2/dict/*'],
                  'en/verb': ['*.txt'],
                  'en/spelling': ['*.txt'],
                  'en/ogden': ['*.txt']},
    py_modules=['turbot'],
    long_description=open('README.rst').read(),
    install_requires=[
        'docopt>=0.6.0,<0.7.0',
        'wikipedia',
        'SPARQLWrapper',
        'BeautifulSoup4',
        'nltk>=3.0.0'
    ],
    cmdclass={'test': ToxTestCommand},
    tests_require=['tox'],
    scripts=['bin/turbot'],
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
    ],
)

if 'install' in sys.argv:
    import nltk
    nltk.download("wordnet")
    nltk.download("nps_chat")
    nltk.download("punkt")
