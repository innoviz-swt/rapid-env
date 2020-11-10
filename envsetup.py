from pathlib import Path

from rapidenv.osh import run_process, copy_path


def main():
    venvbase = Path("venv/Scripts")

    # python environment
    if not Path('venv').exists():
        run_process('python -m venv venv')

    run_process(f'{venvbase}/pip install upgrade pip')
    run_process(f'{venvbase}/pip install -r requirements.txt')

    # copy files locally
    # copy_path(src, local, skip_if_file_exists=True)


if __name__ == '__main__':
    main()
