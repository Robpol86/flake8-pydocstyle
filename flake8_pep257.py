"""A simple flake8 plugin for the pep257 Python utility for validating docstrings.

https://github.com/Robpol86/flake8-pep257
https://pypi.python.org/pypi/flake8-pep257
"""

import pep257

__author__ = '@Robpol86'
__license__ = 'MIT'
__version__ = '0.0.1'


def ignore(code):
    """Should this code be ignored?

    Positional arguments:
    code -- error code (e.g. D201).

    Returns:
    True if code should be ignored, False otherwise.
    """
    if code in Main.options['ignore']:
        return True
    if any(c in code for c in Main.options['ignore']):
        return True
    return False


class Main(object):
    """TODO fill this out."""

    name = 'flake8-pep257'
    options = dict()
    version = __version__

    def __init__(self, tree, filename):
        self.tree = tree  # python file tokenized into a list.
        self.filename = filename  # filename to analyze or 'stdin'.

    @classmethod
    def add_options(cls, parser):
        options = dict((o.get_opt_string(), o) for o in pep257.get_option_parser().option_list)
        option_explain = options.pop('--explain')
        parser.add_options([option_explain, ])
        parser.config_options.append('explain')

    @classmethod
    def parse_options(cls, options):
        cls.options['explain'] = bool(options.explain)
        cls.options['ignore'] = options.ignore

    def run(self):
        if self.filename != 'stdin':
            filename = self.filename
            with open(self.filename) as f:
                source = f.read()
        else:
            raise NotImplementedError
        for error in pep257.PEP257Checker().check_source(source, filename):
            if not hasattr(error, 'code') or ignore(error.code):
                continue
            lineno = error.line
            offset = 0  # Column number starting from 0.
            text = error.message
            yield lineno, offset, text, Main
