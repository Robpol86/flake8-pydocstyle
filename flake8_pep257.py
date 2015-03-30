"""A simple flake8 plugin for the pep257 Python utility for validating docstrings.

https://github.com/Robpol86/flake8-pep257
https://pypi.python.org/pypi/flake8-pep257
"""

import pep257
import pep8

__author__ = '@Robpol86'
__license__ = 'MIT'
__version__ = '0.0.1'


def load_file(filename):
    """Read file to memory.

    From: https://github.com/public/flake8-import-order/blob/620a376/flake8_import_order/__init__.py#L201

    Positional arguments:
    filename -- file path or 'stdin'. From Main().filename.

    Returns:
    Tuple, first item is the filename or 'stdin', second are the contents of the file.
    """
    if filename in ('stdin', '-', None):
        return 'stdin', pep8.stdin_get_value()
    with open(filename) as f:
        return filename, f.read()


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
        cls.options['show-source'] = options.show_source

    def run(self):
        pep257.Error.explain = self.options['explain']
        pep257.Error.source = self.options['show-source']
        filename, source = load_file(self.filename)
        for error in pep257.PEP257Checker().check_source(source, filename):
            if not hasattr(error, 'code') or ignore(error.code):
                continue
            lineno = error.line
            offset = 0  # Column number starting from 0.
            text = '{0} {1}'.format(error.code, error.message.split(': ', 1)[1])
            yield lineno, offset, text, Main
