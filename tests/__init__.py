"""Non-fixture code shared among test modules."""


try:
    from subprocess import check_output, STDOUT
except ImportError:
    from subprocess32 import check_output, STDOUT


assert check_output
assert STDOUT
