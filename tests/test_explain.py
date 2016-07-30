"""Test against sample modules using the explain option in all supported config sources."""

import os
from distutils.spawn import find_executable

import flake8.main
import pytest

from tests import check_output, STDOUT

EXPECTED = list()
EXPECTED.append("""\
./sample.py:1:1: D100 Missing docstring in public module
        All modules should normally have docstrings.  [...] all functions and
        classes exported by a module should also have docstrings. Public
        methods (including the __init__ constructor) should also have
        docstrings.

        Note: Public (exported) definitions are either those with names listed
              in __all__ variable (if present), or those that do not start
              with a single underscore.


./sample.py:5:1: D300 Use \"\"\"triple double quotes\"\"\" (found \'\'\'-quotes)
        For consistency, always use \"\"\"triple double quotes\"\"\" around
        docstrings. Use r\"\"\"raw triple double quotes\"\"\" if you use any
        backslashes in your docstrings. For Unicode docstrings, use
        u\"\"\"Unicode triple-quoted strings\"\"\".

        Note: Exception to this is made if the docstring contains
              \"\"\" quotes in its body.


./sample.py:5:1: D401 First line should be in imperative mood (\'Print\', not \'Prints\')
        [Docstring] prescribes the function or method's effect as a command:
        ("Do this", "Return that"), not as a description; e.g. don't write
        "Returns the pathname ...".


./sample.py:14:1: D203 1 blank line required before class docstring (found 0)
        Insert a blank line before and after all docstrings (one-line or
        multi-line) that document a class -- generally speaking, the class's
        methods are separated from each other by a single blank line, and the
        docstring needs to be offset from the first method by a blank line;
        for symmetry, put a blank line between the class header and the
        docstring.


./sample.py:14:1: D204 1 blank line required after class docstring (found 0)
        Insert a blank line before and after all docstrings (one-line or
        multi-line) that document a class -- generally speaking, the class's
        methods are separated from each other by a single blank line, and the
        docstring needs to be offset from the first method by a blank line;
        for symmetry, put a blank line between the class header and the
        docstring.


./sample.py:14:1: D300 Use \"\"\"triple double quotes\"\"\" (found \'\'\'-quotes)
        For consistency, always use \"\"\"triple double quotes\"\"\" around
        docstrings. Use r\"\"\"raw triple double quotes\"\"\" if you use any
        backslashes in your docstrings. For Unicode docstrings, use
        u\"\"\"Unicode triple-quoted strings\"\"\".

        Note: Exception to this is made if the docstring contains
              \"\"\" quotes in its body.

""")
EXPECTED.append("""\
./sample_unicode.py:1:1: D100 Missing docstring in public module
        All modules should normally have docstrings.  [...] all functions and
        classes exported by a module should also have docstrings. Public
        methods (including the __init__ constructor) should also have
        docstrings.

        Note: Public (exported) definitions are either those with names listed
              in __all__ variable (if present), or those that do not start
              with a single underscore.


./sample_unicode.py:15:1: D300 Use \"\"\"triple double quotes\"\"\" (found '''-quotes)
        For consistency, always use \"\"\"triple double quotes\"\"\" around
        docstrings. Use r\"\"\"raw triple double quotes\"\"\" if you use any
        backslashes in your docstrings. For Unicode docstrings, use
        u\"\"\"Unicode triple-quoted strings\"\"\".

        Note: Exception to this is made if the docstring contains
              \"\"\" quotes in its body.


./sample_unicode.py:15:1: D401 First line should be in imperative mood ('Print', not 'Prints')
        [Docstring] prescribes the function or method's effect as a command:
        ("Do this", "Return that"), not as a description; e.g. don't write
        "Returns the pathname ...".


./sample_unicode.py:24:1: D203 1 blank line required before class docstring (found 0)
        Insert a blank line before and after all docstrings (one-line or
        multi-line) that document a class -- generally speaking, the class's
        methods are separated from each other by a single blank line, and the
        docstring needs to be offset from the first method by a blank line;
        for symmetry, put a blank line between the class header and the
        docstring.


./sample_unicode.py:24:1: D204 1 blank line required after class docstring (found 0)
        Insert a blank line before and after all docstrings (one-line or
        multi-line) that document a class -- generally speaking, the class's
        methods are separated from each other by a single blank line, and the
        docstring needs to be offset from the first method by a blank line;
        for symmetry, put a blank line between the class header and the
        docstring.


./sample_unicode.py:24:1: D300 Use \"\"\"triple double quotes\"\"\" (found '''-quotes)
        For consistency, always use \"\"\"triple double quotes\"\"\" around
        docstrings. Use r\"\"\"raw triple double quotes\"\"\" if you use any
        backslashes in your docstrings. For Unicode docstrings, use
        u\"\"\"Unicode triple-quoted strings\"\"\".

        Note: Exception to this is made if the docstring contains
              \"\"\" quotes in its body.

""")


@pytest.mark.parametrize('stdin', ['', 'sample_unicode.py', 'sample.py'])
@pytest.mark.parametrize('which_cfg', ['tox.ini', 'tox.ini flake8', 'setup.cfg', '.pep257'])
def test_direct(capsys, monkeypatch, tmpdir, stdin, which_cfg):
    """Test by calling flake8.main.main() using the same running python process.

    :param capsys: pytest fixture.
    :param monkeypatch: pytest fixture.
    :param tmpdir: pytest fixture.
    :param str stdin: Pipe this file to stdin of flake8.
    :param str which_cfg: Which config file to test with.
    """
    # Prepare.
    monkeypatch.chdir(tmpdir.join('empty' if stdin else ''))
    monkeypatch.setattr('sys.argv', ['flake8', '-' if stdin else '.', '-j1'])
    if stdin:
        monkeypatch.setattr('pep8.stdin_get_value', lambda: tmpdir.join(stdin).read())

    # Write configuration.
    cfg = which_cfg.split()
    section = cfg[1] if len(cfg) > 1 else 'pep257'
    key = 'show-pep257' if section == 'flake8' else 'explain'
    tmpdir.join('empty' if stdin else '', cfg[0]).write('[{0}]\n{1} = True\n'.format(section, key))

    # Execute.
    with pytest.raises(SystemExit):
        flake8.main.main()
    out, err = capsys.readouterr()
    assert not err

    # Clean.
    if stdin:
        expected = EXPECTED[0 if stdin == 'sample.py' else 1].replace('./{0}:'.format(stdin), 'stdin:')
    elif os.name == 'nt':
        expected = '\n'.join(EXPECTED).replace('./sample', r'.\sample')
    else:
        expected = '\n'.join(EXPECTED)
    out = '\n'.join(l.rstrip() for l in out.splitlines())

    assert out == expected


@pytest.mark.parametrize('stdin', ['', 'sample_unicode.py', 'sample.py'])
@pytest.mark.parametrize('which_cfg', ['tox.ini', 'tox.ini flake8', 'setup.cfg', '.pep257'])
def test_subprocess(tmpdir, stdin, which_cfg):
    """Test by calling flake8 through subprocess using a dedicated python process.

    :param tmpdir: pytest fixture.
    :param str stdin: Pipe this file to stdin of flake8.
    :param str which_cfg: Which config file to test with.
    """
    # Prepare.
    cwd = str(tmpdir.join('empty' if stdin else ''))
    stdin_handle = tmpdir.join(stdin).open() if stdin else None

    # Write configuration.
    cfg = which_cfg.split()
    section = cfg[1] if len(cfg) > 1 else 'pep257'
    key = 'show-pep257' if section == 'flake8' else 'explain'
    tmpdir.join('empty' if stdin else '', cfg[0]).write('[{0}]\n{1} = True\n'.format(section, key))

    # Execute.
    command = [find_executable('flake8'), '--exit-zero', '-' if stdin else '.']
    environ = os.environ.copy()
    environ['COV_CORE_DATAFILE'] = ''  # Disable pytest-cov's subprocess coverage feature. Doesn't work right now.
    out = check_output(command, stderr=STDOUT, cwd=cwd, stdin=stdin_handle, env=environ).decode('utf-8')

    # Clean.
    if stdin:
        expected = EXPECTED[0 if stdin == 'sample.py' else 1].replace('./{0}:'.format(stdin), 'stdin:')
    elif os.name == 'nt':
        expected = '\n'.join(EXPECTED).replace('./sample', r'.\sample')
    else:
        expected = '\n'.join(EXPECTED)
    out = '\n'.join(l.rstrip() for l in out.splitlines())

    assert out == expected
