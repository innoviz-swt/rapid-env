from pathlib import Path
import shutil
import os


def copy_path(src, dst, makedirs=True, skip_dst_exists=False):
    """
    copy (file) or copytree (dir)
    if src doesn't exist FileExistsError is thrown

    src    dst            action
    ----   -------------  ---------------------------------------
    file   file           src file is overwritten
    file   dir            src file is copied to dst/file
    file   doesn't exist  src file is copied to dst path
    dir    file           Exception is thrown
    dir    dir            src dir content is copied to dst dir (copytree)
    dir    doesn't exist  src dir is copied to dst path (copytree)

    :param src: source path
    :param dst: destination path
    :param makedirs: create parent dir tree if not exists
    :param skip_dst_exists: do nothing if dst exists
    :return:
    """

    src = Path(src)
    dst = Path(dst)

    # validate source exists
    if not src.exists():
        raise FileExistsError(f"src '{src.absolute()}' does not exists")

    if src.is_dir() and dst.is_file():
        raise Exception(f"can't copy dir to file. '{src}' is dir, '{dst}' is file. ")

    # explicit dst path in case src is file and dst is dir
    if src.is_file() and dst.is_dir():
        dst = dst / src.name

    # do nothing if dst exists and skip_dst_exists flag is raised
    if skip_dst_exists and dst.exists():
        return

    # create parent dir if doesn't exists
    if makedirs and dst.parent != dst and not dst.parent.exists():
        os.makedirs(dst.parent)

    if src.is_dir():
        shutil.copytree(src, dst)
    elif src.is_file():
        shutil.copy(src, dst)
    else:
        raise RuntimeError(f"Unsupported source path type: {src}")
