"""A simple flake8 plugin for the pep257 Python utility for validating docstrings.

https://github.com/Robpol86/flake8-pep257
https://pypi.python.org/pypi/flake8-pep257
"""

import pep257

__author__ = '@Robpol86'
__license__ = 'MIT'
__version__ = '0.0.1'


class Main(object):
    """TODO fill this out."""

    name = 'flake8-pep257'
    version = __version__

    def __init__(self, tree, filename):
        self.tree = tree  # python file tokenized into a list.
        self.filename = filename  # filename to analyze or 'stdin'.

    def run(self):
        check = type(self)
        for error in pep257.check([self.filename], ignore=list()):
            lineno = error.line
            offset = 0  # Column number starting from 0.
            text = error.message
            yield lineno, offset, text, check
