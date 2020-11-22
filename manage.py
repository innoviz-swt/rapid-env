import sys
import re
import os
from pathlib import Path

from rapidenv.osh import run_process_with_stdout, run_process


def get_release(branch):
    release_pattern = r'release-(\d+).(\d+).(\d+)'
    m = re.match(release_pattern, branch)
    if m is None:
        ret = False, "0.0.0"
    else:
        ret = True, f"{m[1]}.{m[2]}.{m[3]}"

    return ret


def dist(ver):
    venvbase = Path("venv/Scripts")
    pytestcmd = venvbase / "pytest"
    if 'linux' in sys.platform:
        pycmd = venvbase / "python3"
        user_flag = "--user"
    elif sys.platform == 'win32':
        pycmd = venvbase / "python"
        user_flag = ""

    print("## run distribution tests")
    run_process(f'{pytestcmd} -m "not dev"', cwd="./tests")

    # get git commit
    commit = run_process_with_stdout('git rev-parse --short HEAD').strip()
    libname = "rapidenv"

    print(f'########################################################################')
    print(f'# {libname} distribution')
    print(f'# ver: {ver}')
    print(f'# commit: {commit}')
    print(f'# library name: {libname}')
    print(f'########################################################################')

    print("## create version file")
    with open(f"{libname}/version.py", "w") as f:
        f.write(f"__version__ = '{ver}'\n")
        f.write(f"__build__ = '{commit}'\n")

    # create tag
    # todo: improve tag message
    run_process(f'git tag -a {ver} -m "rapid env version {ver}"')
    run_process('git push --follow-tags')

    print('## distribute to pypi')
    run_process(f"{pycmd} -m pip install {user_flag} --upgrade setuptools wheel twine")
    run_process(f"{pycmd} setup.py sdist bdist_wheel")
    run_process(f"{pycmd} -m twine upload --repository pypi dist/*")

    print('## remove version file')
    os.remove(f"{libname}/version.py")


def main():
    # get git branch
    branch = run_process_with_stdout('git rev-parse --abbrev-ref HEAD').strip()

    # check for release
    release, ver = get_release(branch)

    if release:
        dist(ver)


if __name__ == "__main__":
    main()
