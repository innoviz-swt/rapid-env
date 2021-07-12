import pytest
import shutil
import os

from test_utils.context import rapidenv
from test_utils.helpers import tmp_folder

from rapidenv.osh import run_process_with_stdout, run_process

tmpf = tmp_folder(__file__)
root_options = [".root", ".git"]


def setup_function(function):
    """ setup any state tied to the execution of the given method in a
    class.  setup_method is invoked for every test method of a class.
    """
    if not os.path.exists(tmpf):
        os.makedirs(tmpf)


def teardown_function(function):
    """ teardown any state that was previously setup with a setup_method
    call.
    """
    shutil.rmtree(tmpf)


@pytest.mark.dist
@pytest.mark.parametrize("root_option", root_options)
def test_mng_module_not_found(root_option):
    open(tmpf / root_option, 'a').close()

    msg = run_process_with_stdout('mng', cwd=tmpf, raise_exception=False)

    assert msg == f"unable to locate file manage.py in '{tmpf}'"


@pytest.mark.dist
@pytest.mark.parametrize("root_option", root_options)
def test_mng_git_no_main(root_option):
    open(tmpf / 'manage.py', 'a').close()
    open(tmpf / root_option, 'a').close()

    msg = run_process_with_stdout('mng', cwd=tmpf, raise_exception=False)

    assert msg == f"manage.py doesn't contain 'def main()'. root: '{tmpf}'"


@pytest.mark.dist
@pytest.mark.parametrize("root_option", root_options)
def test_mng_success(root_option):
    with open(tmpf / 'manage.py', 'w') as f:
        f.write("def main():")
        f.write("\tprint('success')")
    open(tmpf / root_option, 'a').close()

    msg = run_process_with_stdout('mng', cwd=tmpf, raise_exception=False)

    assert msg == "success"


@pytest.mark.dist
@pytest.mark.parametrize("root_option", root_options[:1])
def test_mng_execute_exception(root_option):
    with open(tmpf / 'manage.py', 'w') as f:
        f.write("def main():")
        f.write("\traise Exception('failure')")
    open(tmpf / root_option, 'a').close()

    p = run_process('mng', cwd=tmpf, raise_exception=False)

    assert p.returncode == 1


@pytest.mark.dist
@pytest.mark.parametrize("root_option", root_options[:1])
def test_mng_execute_ecode(root_option):
    with open(tmpf / 'manage.py', 'w') as f:
        f.write("def main():")
        f.write("\texit(3)")
    open(tmpf / root_option, 'a').close()

    p = run_process('mng', cwd=tmpf, raise_exception=False)

    assert p.returncode == 3
