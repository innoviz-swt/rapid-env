from pathlib import Path

from rapidenv.osh import run_process, copy_path


def main():
    venvbase = Path("venv/Scripts")

    # python environment
    run_process(f'python -m pip install --upgrade pip')
    if not Path('venv').exists():
        run_process('python -m venv venv')

    run_process(f'{venvbase}/python -m pip install --upgrade pip')
    run_process(f'{venvbase}/python -m pip install -r requirements.txt')


if __name__ == '__main__':
    main()
