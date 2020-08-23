import subprocess
from pathlib import Path, WindowsPath, PosixPath

from ..helpers.validate import validate_obj_type


def run_process(cmd: list or str, cwd: None or str or Path = None, raise_exception: bool = True):
    """
    runs process using Popen at cwd as working directory (if available)
    :param cmd: if string, split into spaces separated by " "
    :param cwd: working directory in which to run cmd
    :param raise_exception: if True exception will be raised on cmd error code.
    """

    # validate
    validate_obj_type(cmd, 'cmd', [str, list])
    validate_obj_type(cwd, 'cwd', [None, str, Path, WindowsPath, PosixPath])

    # split cmd to list if string
    if type(cmd) is str:
        cmd = cmd.split(' ')

    # run subprocess
    if cwd is not None:
        p = subprocess.Popen(cmd, cwd=cwd)
    else:
        p = subprocess.Popen(cmd)

    p.wait()

    # validate error code
    if p.returncode != 0:
        msg = f"process exited with error code '{p.returncode}'"
        print(msg)
        if raise_exception:
            raise Exception(msg)


