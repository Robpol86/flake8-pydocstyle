"""A simple flake8 plugin for the pydocstyle Python utility for validating docstrings.

https://github.com/Robpol86/flake8-pydocstyle
https://pypi.python.org/pypi/flake8-pydocstyle
"""

import codecs
import gc
import os

import pep8
import pycodestyle
import pydocstyle

__author__ = '@Robpol86'
__license__ = 'MIT'
__version__ = '1.0.5'


def load_file(filename):
    """Read file to memory.

    For stdin sourced files, this function does something super duper incredibly hacky and shameful. So so shameful. I'm
    obtaining the original source code of the target module from the only instance of pycodestyle.Checker through the
    Python garbage collector. Flake8's API doesn't give me the original source code of the module we are checking.
    Instead it has pycodestyle give me an AST object of the module (already parsed). This unfortunately loses valuable
    information like the kind of quotes used for strings (no way to know if a docstring was surrounded by triple double
    quotes or just one single quote, thereby rendering pydocstyle's D300 error as unusable).

    This will break one day. I'm sure of it. For now it fixes https://github.com/Robpol86/flake8-pydocstyle/issues/2

    :param str filename: File path or 'stdin'. From Main().filename.

    :return: First item is the filename or 'stdin', second are the contents of the file.
    :rtype: tuple
    """
    if filename in ('stdin', '-', None):
        instances = [i for i in gc.get_objects() if isinstance(i, pycodestyle.Checker) or isinstance(i, pep8.Checker)]
        if len(instances) != 1:
            raise ValueError('Expected only 1 instance of pycodestyle.Checker, got {0} instead.'.format(len(instances)))
        return 'stdin', ''.join(instances[0].lines)
    with codecs.open(filename, encoding='utf-8') as handle:
        return filename, handle.read()


def ignore(code):
    """Should this code be ignored.

    :param str code: Error code (e.g. D201).

    :return: True if code should be ignored, False otherwise.
    :rtype: bool
    """
    if code in Main.options['ignore']:
        return True
    if any(c in code for c in Main.options['ignore']):
        return True
    return False


class Main(object):
    """pydocstyle flake8 plugin."""

    name = 'flake8-pydocstyle'
    options = dict()
    version = __version__

    def __init__(self, tree, filename):
        """Constructor.

        :param tree: Tokenized source code, not used.
        :param str filename: Single filename to analyze or 'stdin'.
        """
        self.tree = tree
        self.filename = filename

    @classmethod
    def add_options(cls, parser):
        """Add options to flake8.

        :param parser: optparse.OptionParser from pycodestyle.
        """
        parser.add_option('--show-pydocstyle', action='store_true', help='show explanation of each PEP 257 error')
        parser.config_options.append('show-pydocstyle')

    @classmethod
    def parse_options(cls, options):
        """Read parsed options from flake8.

        :param options: Options to add to flake8's command line options.
        """
        # Handle flake8 options.
        cls.options['explain'] = bool(options.show_pydocstyle)
        cls.options['ignore'] = options.ignore

        # Handle pydocstyle options.
        config = pydocstyle.RawConfigParser()
        for file_name in pydocstyle.ConfigurationParser.PROJECT_CONFIG_FILES:
            if config.read(os.path.join(os.path.abspath('.'), file_name)):
                break
        if not config.has_section('pydocstyle'):
            return
        native_options = dict()
        for option in config.options('pydocstyle'):
            if option == 'ignore':
                native_options['ignore'] = config.get('pydocstyle', option)
            if option in ('explain', 'source'):
                native_options[option] = config.getboolean('pydocstyle', option)
        native_options['show-source'] = native_options.pop('source', None)
        if native_options.get('ignore'):
            native_options['ignore'] = native_options['ignore'].split(',')
        cls.options.update(dict((k, v) for k, v in native_options.items() if v))

    def run(self):
        """Run analysis on a single file."""
        pydocstyle.Error.explain = self.options['explain']
        filename, source = load_file(self.filename)
        for error in pydocstyle.PEP257Checker().check_source(source, filename):
            if not hasattr(error, 'code') or ignore(error.code):
                continue
            lineno = error.line
            offset = 0  # Column number starting from 0.
            explanation = error.explanation if pydocstyle.Error.explain else ''
            text = '{0} {1}{2}'.format(error.code, error.message.split(': ', 1)[1], explanation)
            yield lineno, offset, text, Main
