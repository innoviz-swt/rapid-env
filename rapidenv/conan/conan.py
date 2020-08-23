import sys
from rapidenv.process import run_process
from pathlib import Path


def run_conan(build_type: str = "Debug", raise_exception=True):
    """
    runs 'conan install conanfile.txt' command line in folders in which 'conanfile.txt' is located using recursive
    search relative to current working directory.
    :param build_type: 'Debug' or 'Release', relevant for windows OS only,
    adds '-s build_type={build_type}' to conan cmd.
    :param raise_exception: if True raise exception on failure of running conan cmd.
    """

    for path in Path('.').rglob('conanfile.txt'):
        print(path.resolve())
        cwd = path.parent.resolve()
        if sys.platform == 'win32':
            cmd = f"conan install -s build_type={build_type} conanfile.txt"
        elif 'linux' in sys.platform:
            cmd = f"conan install conanfile.txt"
        else:
            raise RuntimeError(f"platform '{sys.platform}' is not supported")

        print(f"runing conan, cmd: '{cmd}', cwd: '{cwd}'")
        run_process(cmd, cwd=cwd, raise_exception=raise_exception)
