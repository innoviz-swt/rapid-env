from pathlib import Path

from rapidenv.process import run_process
from rapidenv.path import copy_path

def main():
    # python environment
    if not Path('venv').exists():
        run_process('python -m venv venv')

    run_process('venv/scripts/pip install -r requirements.txt')

    # copy files locally
    # copy_path(src, local, skip_if_file_exists=True)


if __name__ == '__main__':
    main()
