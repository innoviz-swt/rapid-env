import sys
from pathlib import Path
import subprocess
import os

if sys.platform == 'win32':
    venvpath = Path('venv')
    venvbase = venvpath / "Scripts"
    pyexe = 'python'
else:  # unix
    venvpath = Path('env')
    venvbase = venvpath / "bin"
    pyexe = 'python3'

pycmd = venvbase / "python"


def venv_run_process(cmd: str, **kwargs):
    # run subprocess
    os.system(cmd)


def main():
    # python environment
    venv_run_process(f'{pyexe} -m pip install --upgrade pip')
    if not venvpath.exists():
        venv_run_process(f'{pyexe} -m venv {venvpath}')

    venv_run_process(f'{pycmd} -m pip install --upgrade pip')
    venv_run_process(f'{pycmd} -m pip install -r tests/test-requirements.txt')


if __name__ == '__main__':
    main()
