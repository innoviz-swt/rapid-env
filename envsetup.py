import sys
from pathlib import Path

from rapidenv.osh import run_process, copy_path

if sys.platform == 'win32':
    venvpath = Path('venv')
    venvbase = venvpath / "Scripts"
else:  # unix
    venvpath = Path('env')
    venvbase = venvpath / "bin"

pycmd = venvbase / "python"


def main():
    # python environment
    run_process(f'python -m pip install --upgrade pip')
    if not venvpath.exists():
        run_process(f'python -m venv {venvpath}')

    run_process(f'{venvbase}/python -m pip install --upgrade pip')
    run_process(f'{venvbase}/python -m pip install -r requirements.txt')


if __name__ == '__main__':
    main()
