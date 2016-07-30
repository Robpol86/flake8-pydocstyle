"""Non-fixture code shared among test modules."""

import os
import subprocess


def check_output(command, cwd=None, env=None, stdin=None):
    """Basically subprocess.check_output since it doesn't exist in Python 2.6.

    :raise CalledProcessError: Command exits non-zero.

    :param iter command: Command to run.
    :param str cwd: Current working directory.
    :param dict env: Set environment variables.
    :param file stdin: Pipe handle to subprocess' stdin.

    :return: Command output.
    :rtype: str
    """
    stdout = subprocess.STDOUT
    pipe = subprocess.PIPE

    # Setup env.
    environ = os.environ.copy()
    if env:
        environ.update(env)

    # Run command.
    with open(os.devnull) as null:
        proc = subprocess.Popen(command, cwd=cwd, env=environ, stdout=pipe, stderr=stdout, stdin=stdin or null)
        output = proc.communicate()[0].decode('utf-8')  # Blocks until command exits.

    # Raise if non-zero exit.
    if proc.poll() != 0:
        raise subprocess.CalledProcessError(proc.poll(), command, output=output)

    return output
