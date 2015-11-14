"""Basic tests."""

import os

import flake8.main
import pytest


@pytest.mark.parametrize('stdin', [True, False])
def test(capsys, monkeypatch, tmpdir, sample_module_unicode, stdin):
    """Test default settings.

    :param capsys: pytest fixture.
    :param monkeypatch: pytest fixture.
    :param tmpdir: pytest fixture.
    :param sample_module_unicode: conftest fixture.
    :param bool stdin: Use stdin source instead of file.
    """
    monkeypatch.chdir(tmpdir)
    monkeypatch.setattr('sys.argv', ['flake8', '-' if stdin else '.', '-j1'])

    if stdin:
        monkeypatch.setattr('pep8.stdin_get_value', lambda: sample_module_unicode)
    else:
        tmpdir.join('sample_module.py').write(sample_module_unicode.encode('utf-8'), 'wb')

    with pytest.raises(SystemExit):
        flake8.main.main()
    out, err = capsys.readouterr()
    assert not err

    expected = (
        './sample_module.py:1:1: D100 Missing docstring in public module\n'
        './sample_module.py:15:1: D300 Use """triple double quotes""" (found \'\'\'-quotes)\n'
        './sample_module.py:15:1: D401 First line should be in imperative mood (\'Print\', not \'Prints\')\n'
        './sample_module.py:24:1: D203 1 blank line required before class docstring (found 0)\n'
        './sample_module.py:24:1: D204 1 blank line required after class docstring (found 0)\n'
        './sample_module.py:24:1: D300 Use """triple double quotes""" (found \'\'\'-quotes)\n'
    )
    if stdin:
        expected = expected.replace('./sample_module.py:', 'stdin:')
    elif os.name == 'nt':
        expected = expected.replace('./sample_module.py:', r'.\sample_module.py:')

    assert expected == out
