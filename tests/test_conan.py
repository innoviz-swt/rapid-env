from pathlib import Path
import os
import shutil

import pytest

from test_utils.helpers import tmp_folder
from test_utils.context import rapidenv

from rapidenv.osh import copy
from rapidenv.conan import run_conan


@pytest.mark.dev
def test_run_conan_file_found():
    # copy test vector
    src = Path(__file__).parent / 'conan_test_vector' / 'conanfile.tv.txt'
    tmpf = tmp_folder(__file__)
    dst = tmpf / 'conanfile.txt'
    copy(src, dst)
    run_conan()

    # validate one of conan outputs exist
    assert os.path.exists(dst.parent / 'conaninfo.txt')

    # delete outputs
    shutil.rmtree(tmpf)
