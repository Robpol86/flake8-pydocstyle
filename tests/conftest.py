# coding=utf-8
"""Plugins for pytest."""

from textwrap import dedent

import pytest


@pytest.fixture
def sample_module():
    """Sample python module for testing."""
    code = """\
    #!/usr/bin/env python
    import sys


    def error(message, code=1):
        '''Prints error message to stderr and exits with a status of 1.'''
        if message:
            print('ERROR: {0}'.format(message))
        else:
            print()
        sys.exit(code)


    class Test(object):
        '''Does nothing.'''
        pass
    """
    return dedent(code)


@pytest.fixture
def sample_module_unicode():
    """Sample python module for testing with Unicode characters."""
    code = u"""\
    #!/usr/bin/env python
    import sys

    UNICODE_TABLE = '''
    +Foods----+--------+---------+
    | Name    | Color  | Type    |
    +---------+--------+---------+
    | Avocado | green  | nut     |
    | Cupuaçu | yellow | fruit   |
    | äöüß    |        | neither |
    +---------+--------+---------+
    '''


    def error(message, code=1):
        '''Prints error message to stderr and exits with a status of 1.'''
        if message:
            print('ERROR: {0}'.format(message))
        else:
            print()
        sys.exit(code)


    class Test(object):
        '''Does nothing.'''
        pass
    """
    return dedent(code)
