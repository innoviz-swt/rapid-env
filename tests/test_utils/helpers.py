from pathlib import Path


def tmp_folder(test_filename):
    return Path(__file__).parent / 'tmp' / Path(test_filename).stem