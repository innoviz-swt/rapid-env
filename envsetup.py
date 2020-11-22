from pathlib import Path

from rapidenv.osh import run_process, copy_path


def main():
    venvbase = Path("venv/Scripts")

    # python environment
    run_process(f'python install upgrade pip')
    if not Path('venv').exists():
        run_process('python -m venv venv')

    run_process(f'{venvbase}/pip install -r requirements.txt')


if __name__ == '__main__':
    main()
