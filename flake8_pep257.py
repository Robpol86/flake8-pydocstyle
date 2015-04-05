"""A simple flake8 plugin for the pep257 Python utility for validating docstrings.

https://github.com/Robpol86/flake8-pep257
https://pypi.python.org/pypi/flake8-pep257
"""

import pep257
import pep8

__author__ = '@Robpol86'
__license__ = 'MIT'
__version__ = '1.0.0'


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
    """Should this code be ignored.

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
    """pep257 flake8 plugin."""

    name = 'flake8-pep257'
    options = dict()
    version = __version__

    def __init__(self, tree, filename):
        """Constructor.

        Positional arguments:
        tree -- tokenized source code, not used.
        filename -- single filename to analyze or 'stdin'.
        """
        self.tree = tree
        self.filename = filename

    @classmethod
    def add_options(cls, parser):
        """Add options to flake8."""
        parser.add_option('--show-pep257', action='store_true', help='show explanation of each PEP 257 error')
        parser.config_options.append('show-pep257')

    @classmethod
    def parse_options(cls, options):
        """Read parsed options from flake8."""
        # Handle flake8 options.
        cls.options['explain'] = bool(options.show_pep257)
        cls.options['ignore'] = options.ignore

        # Handle pep257 options.
        opt_parser = pep257.get_option_parser()
        setattr(opt_parser, '_get_args', lambda *_: list())
        native_options = vars(pep257.get_options(['.'], opt_parser))
        native_options.pop('match', None)
        native_options.pop('match_dir', None)
        native_options['show-source'] = native_options.pop('source', None)
        if native_options.get('ignore'):
            native_options['ignore'] = native_options['ignore'].split(',')
        cls.options.update(dict((k, v) for k, v in native_options.items() if v))

    def run(self):
        """Run analysis on a single file."""
        pep257.Error.explain = self.options['explain']
        filename, source = load_file(self.filename)
        for error in pep257.PEP257Checker().check_source(source, filename):
            if not hasattr(error, 'code') or ignore(error.code):
                continue
            lineno = error.line
            offset = 0  # Column number starting from 0.
            explanation = error.explanation if pep257.Error.explain else ''
            text = '{0} {1}{2}'.format(error.code, error.message.split(': ', 1)[1], explanation)
            yield lineno, offset, text, Main
