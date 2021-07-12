import importlib
import sys
from pathlib import Path
import os


def path_in_tree(rel_path: str or Path):
    path = Path(os.path.abspath(os.curdir))

    # iterate on parent folder look for test_vectors dir
    if (path / rel_path).exists():
        return (path / rel_path).absolute()

    while path.parent != path:
        if (path / rel_path).exists():
            return (path / rel_path).absolute()
        path = path.parent

    return None


def root_dir():
    ret = path_in_tree(".root")
    ret = ret if ret is None else ret.parent
    return ret


def git_dir():
    ret = path_in_tree(".git")
    ret = ret if ret is None else ret.parent
    return ret


def mng():
    """
    if manage.py exit in root dir (recursively searching folder containing .root or .git)
    if so, runs main function from module
    """

    rd = root_dir()
    if rd is None:
        rd = git_dir()

    if rd is None:
        print(f"can't locate root dir (dir containing .git or .root)")
        return 1

    if not (rd / 'manage.py').exists():
        print(f"unable to locate file manage.py in '{rd}'")
        return 1

    sys.path.append(str(rd))
    module = importlib.import_module('manage')

    if 'main' not in dir(module):
        print(f"manage.py doesn't contain 'def main()'. root: '{rd}'")
        return 1

    module.main()

    return 0


if __name__ == "__main__":
    exit(mng())
