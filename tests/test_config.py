"""Basic tests."""

import os
import sys
from textwrap import dedent

import flake8.main
import pytest


@pytest.mark.parametrize('which_cfg', ['tox.ini', 'tox.ini flake8', 'setup.cfg', '.pep257'])
@pytest.mark.parametrize('stdin', [True, False])
def test_ignore(tmpdir, capsys, sample_module, monkeypatch, stdin, which_cfg):
    """Test ignore setting in all supported config sources."""
    sys.argv = ['flake8', '-' if stdin else '.', '-j1']
    os.chdir(str(tmpdir.ensure('project_dir', dir=True)))

    if stdin:
        monkeypatch.setattr('pep8.stdin_get_value', lambda: sample_module)
    else:
        with open('sample_module.py', 'w') as f:
            f.write(sample_module)

    cfg = which_cfg.split()
    section = cfg[1] if len(cfg) > 1 else 'pep257'
    with open(cfg[0], 'w') as f:
        f.write('[{0}]\nignore = D203,D204\n'.format(section))

    with pytest.raises(SystemExit):
        flake8.main.main()
    out, err = capsys.readouterr()
    if 'DeprecationWarning' in err and (True, 'tox.ini', (2, 6)) == (stdin, which_cfg, sys.version_info[:2]):
        assert err  # Temporary hack until flake8 fixes https://gitlab.com/pycqa/flake8/blob/master/flake8/engine.py#L33
    else:
        assert not err

    expected = (
        './sample_module.py:1:1: D100 Missing docstring in public module\n'
        './sample_module.py:5:1: D300 Use """triple double quotes""" (found \'\'\'-quotes)\n'
        './sample_module.py:5:1: D401 First line should be in imperative mood (\'Print\', not \'Prints\')\n'
        './sample_module.py:14:1: D300 Use """triple double quotes""" (found \'\'\'-quotes)\n'
    )
    if stdin:
        expected = expected.replace('./sample_module.py:', 'stdin:')
    elif os.name == 'nt':
        expected = expected.replace('./sample_module.py:', r'.\sample_module.py:')

    assert expected == out


@pytest.mark.parametrize('which_cfg', ['tox.ini', 'tox.ini flake8', 'setup.cfg', '.pep257'])
@pytest.mark.parametrize('stdin', [True, False])
def test_ignore_short(tmpdir, capsys, sample_module, monkeypatch, stdin, which_cfg):
    """Test broad ignore settings in all supported config sources."""
    sys.argv = ['flake8', '-' if stdin else '.', '-j1']
    os.chdir(str(tmpdir.ensure('project_dir', dir=True)))

    if stdin:
        monkeypatch.setattr('pep8.stdin_get_value', lambda: sample_module)
    else:
        with open('sample_module.py', 'w') as f:
            f.write(sample_module)

    cfg = which_cfg.split()
    section = cfg[1] if len(cfg) > 1 else 'pep257'
    with open(cfg[0], 'w') as f:
        f.write('[{0}]\nignore = D2,D3\n'.format(section))

    with pytest.raises(SystemExit):
        flake8.main.main()
    out, err = capsys.readouterr()
    assert not err

    expected = (
        './sample_module.py:1:1: D100 Missing docstring in public module\n'
        './sample_module.py:5:1: D401 First line should be in imperative mood (\'Print\', not \'Prints\')\n'
    )
    if stdin:
        expected = expected.replace('./sample_module.py:', 'stdin:')
    elif os.name == 'nt':
        expected = expected.replace('./sample_module.py:', r'.\sample_module.py:')

    assert expected == out


@pytest.mark.parametrize('which_cfg', ['tox.ini', 'tox.ini flake8', 'setup.cfg', '.pep257'])
@pytest.mark.parametrize('stdin', [True, False])
def test_explain(tmpdir, capsys, sample_module, monkeypatch, stdin, which_cfg):
    """Test explain setting in all supported config sources."""
    sys.argv = ['flake8', '-' if stdin else '.', '-j1']
    os.chdir(str(tmpdir.ensure('project_dir', dir=True)))

    if stdin:
        monkeypatch.setattr('pep8.stdin_get_value', lambda: sample_module)
    else:
        with open('sample_module.py', 'w') as f:
            f.write(sample_module)

    cfg = which_cfg.split()
    section = cfg[1] if len(cfg) > 1 else 'pep257'
    with open(cfg[0], 'w') as f:
        f.write('[{0}]\n{1} = True\n'.format(section, 'show-pep257' if section == 'flake8' else 'explain'))

    with pytest.raises(SystemExit):
        flake8.main.main()
    out, err = capsys.readouterr()
    assert not err

    expected = dedent("""\
        ./sample_module.py:1:1: D100 Missing docstring in public module
                All modules should normally have docstrings.  [...] all functions and
                classes exported by a module should also have docstrings. Public
                methods (including the __init__ constructor) should also have
                docstrings.

                Note: Public (exported) definitions are either those with names listed
                      in __all__ variable (if present), or those that do not start
                      with a single underscore.


        ./sample_module.py:5:1: D300 Use \"\"\"triple double quotes\"\"\" (found \'\'\'-quotes)
                For consistency, always use \"\"\"triple double quotes\"\"\" around
                docstrings. Use r\"\"\"raw triple double quotes\"\"\" if you use any
                backslashes in your docstrings. For Unicode docstrings, use
                u\"\"\"Unicode triple-quoted strings\"\"\".

                Note: Exception to this is made if the docstring contains
                      \"\"\" quotes in its body.


        ./sample_module.py:5:1: D401 First line should be in imperative mood (\'Print\', not \'Prints\')
                [Docstring] prescribes the function or method's effect as a command:
                ("Do this", "Return that"), not as a description; e.g. don't write
                "Returns the pathname ...".


        ./sample_module.py:14:1: D203 1 blank line required before class docstring (found 0)
                Insert a blank line before and after all docstrings (one-line or
                multi-line) that document a class -- generally speaking, the class's
                methods are separated from each other by a single blank line, and the
                docstring needs to be offset from the first method by a blank line;
                for symmetry, put a blank line between the class header and the
                docstring.


        ./sample_module.py:14:1: D204 1 blank line required after class docstring (found 0)
                Insert a blank line before and after all docstrings (one-line or
                multi-line) that document a class -- generally speaking, the class's
                methods are separated from each other by a single blank line, and the
                docstring needs to be offset from the first method by a blank line;
                for symmetry, put a blank line between the class header and the
                docstring.


        ./sample_module.py:14:1: D300 Use \"\"\"triple double quotes\"\"\" (found \'\'\'-quotes)
                For consistency, always use \"\"\"triple double quotes\"\"\" around
                docstrings. Use r\"\"\"raw triple double quotes\"\"\" if you use any
                backslashes in your docstrings. For Unicode docstrings, use
                u\"\"\"Unicode triple-quoted strings\"\"\".

                Note: Exception to this is made if the docstring contains
                      \"\"\" quotes in its body.
        """)
    if stdin:
        expected = expected.replace('./sample_module.py:', 'stdin:')
    elif os.name == 'nt':
        expected = expected.replace('./sample_module.py:', r'.\sample_module.py:')

    assert ''.join(l.rstrip() for l in expected.splitlines()) == ''.join(l.rstrip() for l in out.splitlines())
