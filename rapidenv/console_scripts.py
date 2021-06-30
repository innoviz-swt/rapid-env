import importlib
import sys
from pathlib import Path
import os


def path_in_tree(rel_path: str or Path):
    path = Path(os.path.abspath(os.curdir))

    # iterate on parent folder look for test_vectors dir
    if (path / rel_path).exists():
        return (path / rel_path).absolute()

    while path.parent:
        if (path / rel_path).exists():
            return (path / rel_path).absolute()
        path = path.parent

    return Path()


def root_dir():
    return path_in_tree(".git").parent


def mng():
    """
    if manage.py exit in folder runs script
    :return:
    """
    sys.path.append(str(root_dir()))

    try:
        module = importlib.import_module('manage')
    except ImportError:
        print(f"unable to locate file: manage.py")
        return

    try:
        module.main()
    except Exception as e:
        print(f"manage.py doesn't contain 'def main()'")


if __name__ == "__main__":
    mng()
