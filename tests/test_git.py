from pathlib import Path
import os
import shutil

from .helpers import tmp_folder

from .context import rapidenv
from rapidenv import git


def test_add_gitignore_defaultpath():
    # change working dir
    cwd = os.getcwd()

    try:
        # change working directory to tmp
        tmpf = tmp_folder(__file__)
        os.makedirs(tmpf)
        os.chdir(tmpf)

        # copy test vector
        git.add_gitignore()

        # validate one of conan outputs exist
        assert os.path.exists('.gitignore')

        # restore working directory
        os.chdir(cwd)

        # delete output
        shutil.rmtree(tmpf)
    except Exception as e:
        # restore working directory
        os.chdir(cwd)
        raise e


def test_add_gitignore_custom_path():
    # copy test vector
    dst = tmp_folder(__file__)
    git.add_gitignore(dst)

    # validate one of conan outputs exist
    assert os.path.exists(dst / '.gitignore')

    # delete outputs
    shutil.rmtree(dst)

