import os
import sys

import flake8.main
import pytest


def test_cwd(tmpdir, capsys, sample_module):
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
    os.chdir(str(tmpdir.ensure('project_dir', dir=True)))
    with open('sample_module.py', 'w') as f:
        f.write(sample_module[0])
    sys.argv = ['flake8', '-', '-j1']
    with pytest.raises(SystemExit):
        with open('sample_module.py', 'r') as f:
            monkeypatch.setattr('sys.stdin', f)
            flake8.main.main()
    out, err = capsys.readouterr()
    assert not err
    assert sample_module[1] == out
