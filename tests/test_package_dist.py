from pathlib import Path
import pytest

from rapidenv.process import run_process


@pytest.mark.dist
def test_pip_install():
    cwd = Path(__file__).parent
    path = cwd.parent
    run_process(f'python -m pip install --upgrade --force-reinstall {path}', cwd=cwd)
    run_process(f'python -c "import rapidenv"', cwd=cwd)
