"""Basic tests."""

import os
import sys

import flake8.main
import pytest


def test_cwd(tmpdir, capsys, sample_module):
    """Test using a Python test module in the current working directory."""
    os.chdir(str(tmpdir.ensure('project_dir', dir=True)))
    with open('sample_module.py', 'w') as f:
        f.write(sample_module[0])
    sys.argv = ['flake8', '.', '-j1']
    with pytest.raises(SystemExit):
        flake8.main.main()
    out, err = capsys.readouterr()
    assert not err
    assert sample_module[1] == out


def test_stdin(tmpdir, capsys, sample_module, monkeypatch):
    """Test using a Python test module passed through stdin."""
    monkeypatch.setattr('pep8.stdin_get_value', lambda: sample_module[0])
    os.chdir(str(tmpdir.ensure('project_dir', dir=True)))
    sys.argv = ['flake8', '-', '-j1']
    with pytest.raises(SystemExit):
        flake8.main.main()
    out, err = capsys.readouterr()
    assert not err
    assert sample_module[2] == out
