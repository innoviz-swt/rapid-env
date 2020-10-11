import subprocess
from pathlib import Path, WindowsPath, PosixPath
import re

from ..helpers.validate import validate_obj_type


def run_process(cmd: list or str, raise_exception: bool = True, **kwargs):
    """
    runs process using Popen at cwd as working directory (if available)
    :param cmd: if string, split into spaces separated by " "
    :param raise_exception: if True exception will be raised on cmd error code, default: True.
    :param kwargs: kwargs to pass to Popen, running subprocess.Popen(cmd, **kwargs)

    :return process
    """

    # validate
    validate_obj_type(cmd, 'cmd', [str, list])
    kwargs.get('cwd') and validate_obj_type(kwargs['cwd'], 'cwd', [type(None), str, Path, WindowsPath, PosixPath])

    # split cmd to list if string
    if type(cmd) is str:
        # sstr = "<#>"
        # # change spaces inside "", or '' to special character sequence
        # m = True
        # while m:
        #     # search for
        #     m = re.search('(\")(.*?)(\")', cmd)
        #     rep = m[0].replace(' ', sstr)
        #     cmd.replace(m[0], rep)
        cmd = cmd.split(' ')

    # exit(0)

    # run subprocess
    p = subprocess.Popen(cmd, **kwargs)

    p.wait()

    # validate error code
    if p.returncode != 0:
        msg = f"process exited with error code '{p.returncode}'"
        print(msg)
        if raise_exception:
            raise Exception(msg)

    return p


def run_process_with_stdout(cmd: list or str, raise_exception: bool = True, **kwargs):
    # validate stdout not defined in kwargs
    if kwargs.get('stdout'):
        raise RuntimeError("run_process_with_stdout defines stdout and returns stdout as decoded string.")

    p = run_process(cmd, raise_exception, stdout=subprocess.PIPE, **kwargs)
    stdout = p.stdout.read().decode()

    return stdout
