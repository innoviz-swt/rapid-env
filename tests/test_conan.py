from pathlib import Path
import os
import shutil

from .helpers import tmp_folder

from .context import rapidenv
from rapidenv import os as reos
from rapidenv import conan


# def test_run_conan_file_found():
#     # copy test vector
#     src = Path(__file__).parent / 'conan_test_vector' / 'conanfile.tv.txt'
#     tmpf = tmp_folder(__file__)
#     dst = tmpf / 'conanfile.txt'
#     reos.copy_path(src, dst)
#     conan.run_conan()
#
#     # validate one of conan outputs exist
#     assert os.path.exists(dst.parent / 'conaninfo.txt')
#
#     # delete outputs
#     shutil.rmtree(tmpf)
