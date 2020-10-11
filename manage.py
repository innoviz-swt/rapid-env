import pytest
from pathlib import Path
import re

from rapidenv.process import run_process_with_stdout, run_process


def get_release(branch):
    release_pattern = r'release_(\d+).(\d+).(\d+)'
    m = re.match(release_pattern, branch)
    if m is None:
        ret = False, "0.0.0-dev"
    else:
        ret = True, f"{m[1]}.{m[2]}.{m[3]}"

    return ret


def dist(ver):
    # todo: improve tag message

    # create tag
    # git tag -a v1.4 -m "my version 1.4"
    run_process(f'git tag -a {ver} -m "rapid env version {ver}"')

    # get git commit
    commit = run_process_with_stdout('git rev-parse --short HEAD').strip()
    libname = "rapidenv"

    print(f'########################################################################')
    print(f'# {libname} distribution')
    print(f'# ver: {ver}')
    print(f'# commit: {commit}')
    print(f'# library name: {libname}')
    print(f'########################################################################')


    # distribute


def main():
    # run pytest
    # cmd = (Path('.dev').exists() and ['-m', "not dist"]) or ['-m', "not dev"]
    # pytest.main(cmd)

    # get git branch
    # branch = run_process_with_stdout('git rev-parse --abbrev-ref HEAD').strip()
    branch = "release_0.0.0"

    # check for release
    release, ver = get_release(branch)

    if release:
        dist(ver)


if __name__ == "__main__":
    main()
