import os
import sys

import pytest

from xonsh.built_ins import run_subproc



@pytest.yield_fixture(autouse=True)
def chdir_to_test_dir(xonsh_builtins):
    old_cwd = os.getcwd()
    new_cwd = os.path.dirname(__file__)
    os.chdir(new_cwd)
    yield
    os.chdir(old_cwd)

#def test_runsubproc_simple(capfd, xonsh_builtins, xonsh_execer):
def test_runsubproc_simple(xonsh_builtins, xonsh_execer):
    new_cwd = os.path.dirname(__file__)
    xonsh_builtins.__xonsh_env__['PATH'] = os.path.join(new_cwd, 'bin') + \
        os.pathsep + os.path.dirname(sys.executable)
    xonsh_builtins.__xonsh_env__['XONSH_ENCODING'] = 'utf8'
    xonsh_builtins.__xonsh_env__['XONSH_ENCODING_ERRORS'] = 'surrogateescape'
    out = run_subproc([['pwd']], captured='stdout')
    assert out.rstrip() == new_cwd


def test_runsubproc_redirect_out_to_file(xonsh_builtins, xonsh_execer):
    run_subproc([['pwd', 'out>', 'tttt']], captured='stdout')
    with open('tttt') as f:
        assert f.read().rstrip() == os.getcwd()
    os.remove('tttt')

