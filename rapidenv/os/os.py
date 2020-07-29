from pathlib import Path
import shutil
import os


def copy_path(src, dst):
    src = Path(src)
    dst = Path(dst)

    # create parent dir if doesn't exists
    if dst.parent != dst and not os.path.exists(dst.parent):
        os.makedirs(dst.parent)

    if src.is_dir():
        shutil.copytree(src, dst)
    elif src.is_file():
        shutil.copy(src, dst)
    else:
        raise RuntimeError(f"Unsupported source path type: {src}")