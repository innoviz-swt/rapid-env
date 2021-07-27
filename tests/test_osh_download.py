import shutil 
import os
import pytest 

from test_utils.context import rapidenv
from test_utils.helpers import tmp_folder

from rapidenv.osh import download_archive

tmpf = tmp_folder(__file__)
samples = [
    "https://file-examples-com.github.io/uploads/2017/02/zip_2MB.zip",
]


def setup_function(function):
    """ setup any state tied to the execution of the given method in a
    class.  setup_method is invoked for every test method of a class.
    """
    if not os.path.exists(tmpf):
        os.makedirs(tmpf)


def teardown_function(function):
    """ teardown any state that was previously setup with a setup_method
    call.
    """
    shutil.rmtree(tmpf)


@pytest.mark.parametrize("sample", samples)
def test_download_and_unpack_succeed(sample):
    print(sample)
    download_archive(sample, tmpf / 'sample')    
    assert os.path.exists(tmpf / 'sample')
    assert os.path.exists(tmpf / 'sample' / 'file-sample_1MB.doc')


def test_download_makedirs_false_failed():
    sample = samples[0]

    e = None
    try:
        download_archive(sample, tmpf / 'dir' / 'sample', makedirs=False)    
    except Exception as ex:
        e = ex

    assert e is not None
    assert e.strerror == "No such file or directory"
    assert e.filename == str(tmpf / 'dir' / 'zip_2MB.zip')


def test_download_makedirs_true_success():
    sample = samples[0]

    e = None
    try:
        download_archive(sample, tmpf / 'dir' / 'sample', makedirs=True)
    except Exception as ex:
        e = ex

    assert e is None


def test_download_skip_dst_exists_false_fail_when_dst_exists():
    sample = samples[0]

    os.makedirs(tmpf / 'sample')
    e = None
    try:
        download_archive(sample, tmpf / 'sample', skip_dst_exists=False)
    except Exception as ex:
        e = ex

    assert e is not None
    assert e.args[0] == "Archive unpack destination already exists"
    assert e.args[1] == str(tmpf / 'sample')


def test_download_skip_dst_exists_true_do_nothing_when_dst_exists():
    sample = samples[0]

    os.makedirs(tmpf / 'sample')
    download_archive(sample, tmpf / 'sample', skip_dst_exists=True)
    assert not os.path.exists(tmpf / 'sample' / 'file-sample_1MB.doc')


def test_download_delete_archive_false_success():
    sample = samples[0]

    download_archive(sample, tmpf / 'sample', delete_archive=False)
    assert os.path.exists(tmpf / 'zip_2MB.zip')


def test_download_delete_archive_true_success():
    sample = samples[0]

    download_archive(sample, tmpf / 'sample', delete_archive=True)
    assert not os.path.exists(tmpf / 'zip_2MB.zip')
