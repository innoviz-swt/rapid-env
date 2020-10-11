from pathlib import Path
import os
import shutil

import pytest

from .helpers import tmp_folder

from .context import rapidenv
from rapidenv.path import copy_path
from rapidenv.conan import run_conan


@pytest.mark.dev
def test_run_conan_file_found():
    # copy test vector
    src = Path(__file__).parent / 'conan_test_vector' / 'conanfile.tv.txt'
    tmpf = tmp_folder(__file__)
    dst = tmpf / 'conanfile.txt'
    copy_path(src, dst)
    run_conan()

    # validate one of conan outputs exist
    assert os.path.exists(dst.parent / 'conaninfo.txt')

    # delete outputs
    shutil.rmtree(tmpf)
