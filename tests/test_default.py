"""Test against sample modules using the default options."""

import os
from distutils.spawn import find_executable

import flake8.main
import pytest

from tests import check_output

EXPECTED = """\
./sample.py:1:1: D100 Missing docstring in public module
./sample.py:5:1: D300 Use \"\"\"triple double quotes\"\"\" (found '''-quotes)
./sample.py:5:1: D401 First line should be in imperative mood ('Print', not 'Prints')
./sample.py:14:1: D203 1 blank line required before class docstring (found 0)
./sample.py:14:1: D204 1 blank line required after class docstring (found 0)
./sample.py:14:1: D300 Use \"\"\"triple double quotes\"\"\" (found '''-quotes)
./sample_unicode.py:1:1: D100 Missing docstring in public module
./sample_unicode.py:15:1: D300 Use \"\"\"triple double quotes\"\"\" (found '''-quotes)
./sample_unicode.py:15:1: D401 First line should be in imperative mood ('Print', not 'Prints')
./sample_unicode.py:24:1: D203 1 blank line required before class docstring (found 0)
./sample_unicode.py:24:1: D204 1 blank line required after class docstring (found 0)
./sample_unicode.py:24:1: D300 Use \"\"\"triple double quotes\"\"\" (found '''-quotes)\
"""


@pytest.mark.parametrize('stdin', ['', 'sample_unicode.py', 'sample.py'])
def test_direct(capsys, monkeypatch, tmpdir, stdin):
    """Test by calling flake8.main.main() using the same running python process.

    :param capsys: pytest fixture.
    :param monkeypatch: pytest fixture.
    :param tmpdir: pytest fixture.
    :param str stdin: Pipe this file to stdin of flake8.
    """
    # Prepare.
    monkeypatch.chdir(tmpdir.join('empty' if stdin else ''))
    monkeypatch.setattr('sys.argv', ['flake8', '-' if stdin else '.', '-j1'])
    if stdin:
        monkeypatch.setattr('pep8.stdin_get_value', lambda: tmpdir.join(stdin).read())

    # Execute.
    with pytest.raises(SystemExit):
        flake8.main.main()
    out, err = capsys.readouterr()
    assert not err

    # Clean.
    if stdin:
        expected = '\n'.join('stdin:' + l.split(':', 1)[-1] for l in EXPECTED.splitlines() if stdin in l)
    elif os.name == 'nt':
        expected = EXPECTED.replace('./sample', r'.\sample')
    else:
        expected = EXPECTED
    out = '\n'.join(l.rstrip() for l in out.splitlines())

    assert out == expected


@pytest.mark.parametrize('stdin', ['', 'sample_unicode.py', 'sample.py'])
def test_subprocess(tmpdir, stdin):
    """Test by calling flake8 through subprocess using a dedicated python process.

    :param tmpdir: pytest fixture.
    :param str stdin: Pipe this file to stdin of flake8.
    """
    # Prepare.
    cwd = str(tmpdir.join('empty' if stdin else ''))
    stdin_handle = tmpdir.join(stdin).open() if stdin else None

    # Execute.
    command = [find_executable('flake8'), '--exit-zero', '-' if stdin else '.']
    environ = os.environ.copy()
    environ['COV_CORE_DATAFILE'] = ''  # Disable pytest-cov's subprocess coverage feature. Doesn't work right now.
    out = check_output(command, cwd=cwd, stdin=stdin_handle, env=environ)

    # Clean.
    if stdin:
        expected = '\n'.join('stdin:' + l.split(':', 1)[-1] for l in EXPECTED.splitlines() if stdin in l)
    elif os.name == 'nt':
        expected = EXPECTED.replace('./sample', r'.\sample')
    else:
        expected = EXPECTED
    out = '\n'.join(l.rstrip() for l in out.splitlines())

    assert out == expected
