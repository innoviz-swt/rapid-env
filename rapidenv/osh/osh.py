import shutil
import os
import subprocess
from pathlib import Path, WindowsPath, PosixPath
import re

from ..helpers.validate import validate_obj_type


def str_split(cmd):
    sstr = "<#>"
    o = 0
    tcmd = ""
    while True:
        # search for strings in apostrophes
        m = re.search('\"(.*?)\"|\'(.*?)\'', cmd[o:])

        # append end of string and exit when no match
        if m is None:
            tcmd += cmd[o:]
            break

        # attach updated part
        r = m.regs[0]
        tcmd += cmd[o:o + r[0]] + cmd[o + r[0]: o + r[1]].replace(' ', sstr)

        # update offset for original string
        o += r[1]

    tcmd = tcmd.split(' ')

    # resore spaces replaced by special string
    cmd = []
    for i in range(len(tcmd)):
        s = tcmd[i]
        s = s.replace(sstr, ' ')
        # remove apostrophes if are part of string
        if len(s) > 2 and s[0] == "\'" and s[-1] == "\'":
            s = s[1:-1]
        elif len(s) > 2 and s[0] == "\"" and s[-1] == "\"":
            s = s[1:-1]

        # skip empty (multiple spaces)
        if len(s) == 0:
            continue

        cmd += [s]

    return cmd


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
        cmd = str_split(cmd)

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
