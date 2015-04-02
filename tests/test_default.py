"""Basic tests."""

import os
import sys

import flake8.main
import pytest


@pytest.mark.parametrize('stdin', [True, False])
def test_cwd(tmpdir, capsys, sample_module, monkeypatch, stdin):
    """Test default settings."""
    sys.argv = ['flake8', '-' if stdin else '.', '-j1']
    os.chdir(str(tmpdir.ensure('project_dir', dir=True)))

    if stdin:
        monkeypatch.setattr('pep8.stdin_get_value', lambda: sample_module)
    else:
        with open('sample_module.py', 'w') as f:
            f.write(sample_module)

    with pytest.raises(SystemExit):
        flake8.main.main()
    out, err = capsys.readouterr()
    assert not err

    expected = (
        './sample_module.py:1:1: D100 Missing docstring in public module\n'
        './sample_module.py:5:1: D300 Use """triple double quotes""" (found \'\'\'-quotes)\n'
        './sample_module.py:5:1: D401 First line should be in imperative mood (\'Print\', not \'Prints\')\n'
        './sample_module.py:14:1: D203 1 blank line required before class docstring (found 0)\n'
        './sample_module.py:14:1: D204 1 blank line required after class docstring (found 0)\n'
        './sample_module.py:14:1: D300 Use """triple double quotes""" (found \'\'\'-quotes)\n'
    )
    if stdin:
        expected = expected.replace('./sample_module.py:', 'stdin:')
    elif os.name == 'nt':
        expected = expected.replace('./sample_module.py:', r'.\sample_module.py:')

    assert expected == out
