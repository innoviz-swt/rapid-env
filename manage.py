import sys
import re
import os
from pathlib import Path

from rapidenv.osh import run_process_with_stdout, run_process

venvbase = Path("venv/Scripts")
pytestcmd = venvbase / "pytest"
if 'linux' in sys.platform:
    pycmd = venvbase / "python3"
    user_flag = "--user"
elif sys.platform == 'win32':
    pycmd = venvbase / "python"
    user_flag = ""


def get_release(branch):
    release_pattern = r'release-(\d+).(\d+).(\d+)'
    m = re.match(release_pattern, branch)
    if m is None:
        ret = False, "0.0.0"
    else:
        ret = True, f"{m[1]}.{m[2]}.{m[3]}"

    return ret


def test():
    print("## run distribution tests")
    run_process(f'{pytestcmd} -m "not dist"', cwd="./tests")


def dist(ver):
    print("## run distribution tests")
    run_process(f'{pytestcmd} -m "not dev"', cwd="./tests")

    # # get git branch
    # branch = run_process_with_stdout('git rev-parse --abbrev-ref HEAD')

    # get git commit
    commit = run_process_with_stdout('git rev-parse --short HEAD')
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

    # update relevant libraries
    run_process(f'{pycmd} -m pip install --upgrade pip')
    run_process(f"{pycmd} -m pip install {user_flag} --upgrade setuptools wheel twine")

    print('## distribute to pypi')
    run_process(f"{pycmd} setup.py sdist bdist_wheel")
    run_process(f"{pycmd} -m twine upload --repository pypi dist/*")

    # create tag
    # todo: improve tag message
    run_process(f'git tag -a {ver} -m "rapid env version {ver}"')
    run_process('git push --follow-tags')

    print('## remove version file')
    os.remove(f"{libname}/version.py")


def main():
    # get version
    ver = (len(sys.argv) > 1 and sys.argv[1]) or '0.0.0'

    if ver == '0.0.0':
        test()
    else:
        dist(ver)

    print('')
    print('done')


if __name__ == "__main__":
    main()
