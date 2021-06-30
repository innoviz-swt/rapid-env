import pytest
import shutil
import os
from pathlib import Path

from test_utils.context import rapidenv
from test_utils.helpers import tmp_folder

from rapidenv.osh import run_process_with_stdout

tmpf = tmp_folder(__file__)


def tmpf_decorator(func):
    def wrapper():
        if not os.path.exists(tmpf):
            os.makedirs(tmpf)

        func()

        shutil.rmtree(tmpf)

    return wrapper


@pytest.mark.dist
@tmpf_decorator
def test_mng_module_not_found():
    open(tmpf / '.git', 'a').close()

    msg = run_process_with_stdout('mng', cwd=tmpf)

    assert msg == "unable to locate file: manage.py"


@pytest.mark.dist
@tmpf_decorator
def test_mng_no_main():
    open(tmpf / 'manage.py', 'a').close()
    open(tmpf / '.git', 'a').close()

    msg = run_process_with_stdout('mng', cwd=tmpf)

    assert msg == "manage.py doesn't contain 'def main()'"


@pytest.mark.dist
@tmpf_decorator
def test_mng_success():
    with open(tmpf / 'manage.py', 'w') as f:
        f.write("def main():")
        f.write("\tprint('success')")
    open(tmpf / '.git', 'a').close()

    msg = run_process_with_stdout('mng', cwd=tmpf)

    assert msg == "success"
