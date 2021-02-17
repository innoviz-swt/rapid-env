from pathlib import Path

from ..osh import copy


def add_gitignore(path: str or Path = '.'):
    """
    add gitignore template to path
    :param path: folder path, default '.' (working directory)
    :return:
    """
    copy(Path(__file__).parent / 'templates' / '.gitignore', Path(path) / '.gitignore')
