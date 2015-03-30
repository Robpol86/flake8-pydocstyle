from textwrap import dedent

import pytest


@pytest.fixture
def sample_module():
    code = """\
    #!/usr/bin/env python
    import sys


    def error(message, code=1):
        '''Prints error message to stderr and exits with a status of 1.'''
        if message:
            print('ERROR: {0}'.format(message), file=sys.stderr)
        else:
            print(file=sys.stderr)
        sys.exit(code)


    class Test(object):
        '''Does nothing.'''
        pass
    """

    expected = (
        './sample_module.py:1:1: D100 Missing docstring in public module\n'
        './sample_module.py:5:1: D300 Use """triple double quotes""" (found \'\'\'-quotes)\n'
        './sample_module.py:5:1: D401 First line should be in imperative mood (\'Print\', not \'Prints\')\n'
        './sample_module.py:14:1: D203 1 blank line required before class docstring (found 0)\n'
        './sample_module.py:14:1: D204 1 blank line required after class docstring (found 0)\n'
        './sample_module.py:14:1: D300 Use """triple double quotes""" (found \'\'\'-quotes)\n'
    )
    return dedent(code), expected
