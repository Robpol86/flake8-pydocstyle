# coding=utf-8
"""pytest fixtures for this directory."""

from textwrap import dedent

import pytest


@pytest.fixture(autouse=True)
def sample_code(tmpdir):
    """Sample source files.

    :param tmpdir: pytest fixture.

    :return: tmpdir fixture.
    :rtype: py.path
    """
    tmpdir.ensure_dir('empty')
    tmpdir.join('sample.py').write(dedent("""\
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
    """))
    tmpdir.join('sample_unicode.py').write(dedent(u"""\
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
    """).encode('utf-8'), mode='wb')
    return tmpdir
