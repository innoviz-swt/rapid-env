import re
import os
import argparse
from pathlib import Path

from rapidenv.osh import run_process_with_stdout, run_process

from envsetup import venvbase, pycmd

root = Path(__file__).parent
pytestcmd = venvbase / "pytest"


def get_release(branch):
    release_pattern = r'release-(\d+).(\d+).(\d+)'
    m = re.match(release_pattern, branch)
    if m is None:
        ret = False, "0.0.0"
    else:
        ret = True, f"{m[1]}.{m[2]}.{m[3]}"

    return ret


def test_dev():
    print("## run dev tests")
    run_process(f'./{pytestcmd} -v -m "not dist"', cwd="./tests")


def test_dist():
    print("## install rapidenv and run tests")
    run_process(f'./{pycmd} -m pip install . -I')
    p = run_process(f'./{pytestcmd} -v -m "not dev"', cwd="./tests", raise_exception=False)
    run_process(f'./{pycmd} -m pip uninstall rapid-env -y')
    if p.returncode:
        raise RuntimeError("tests failed")


def dist(ver):
    print("## install locally and test distribution")
    test_dist()

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

    print('## distribute to pypi')
    run_process(f'{pycmd} -m pip install --upgrade pip')
    run_process(f"{pycmd} -m pip install --upgrade setuptools wheel twine")
    run_process(f"{pycmd} setup.py sdist bdist_wheel")
    run_process(f"{pycmd} -m twine upload --repository pypi dist/*")

    # create tag
    # todo: improve tag message
    run_process(f'git tag -a {ver} -m "rapid env version {ver}"')
    run_process('git push --follow-tags')

    print('## remove version file')
    os.remove(f"{libname}/version.py")


def parse_arguments():
    parser = argparse.ArgumentParser(description='manage py')

    parser.add_argument('ver', nargs='?', default="0.0.0", help='distribution version')

    parser.add_argument('--test-dev', '-td', dest='test_dev', action='store_true',
                        help='build the project')

    parser.add_argument('--test-dist', '-t', dest='test_dist', action='store_true',
                        help='build the project')

    parser.add_argument('--dist', '-d', dest='dist', action='store_true',
                        help='distribute the project')

    args = parser.parse_args()

    return args


def main():
    os.chdir(root)
    args = parse_arguments()

    if args.test_dev:
        test_dev()

    if args.test_dist:
        test_dist()

    if args.dist:
        dist(args.ver)

    print('')
    print('done running manage.py')


if __name__ == "__main__":
    main()
