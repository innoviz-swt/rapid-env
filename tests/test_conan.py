from pathlib import Path
import os

from .context import rapidenv
from rapidenv import os as ros
from rapidenv import conan


def test_run_conan_file_found():
    # copy test vector
    src = Path(__file__).parent / 'conan_test_vector' / 'conanfile.tv.txt'
    dst = Path('tmp/tests/conan/conanfile.txt')
    ros.copy_path(src, dst)
    conan.run_conan()

    # validate one of conan outputs exist
    assert os.path.exists(dst.parent / 'conaninfo.txt')

