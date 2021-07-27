import urllib.request
import os
import shutil
from pathlib import Path


def download_archive(url, dst, makedirs=True, skip_dst_exists=False, delete_archive=True):
    """
    download archive from url ro dst parent directory and unpack it to dst folder.
    if archive contains single folders recursively remove them placing main folder in dst.

    :param src source url, source must be and archive file url
    :param dst destination directory
    :param makedirs create dst parent dir tree if not exists
    :param skip_dst_exists do nothing if dst exists
    :param delete_archive delete archive downloaded once done
    :return:
    """
    dst = Path(dst)

    # do nothing if dst exists and skip_dst_exists flag is raised
    if skip_dst_exists and dst.exists():
        return

    # validate destination folder doesn't already exists
    if dst.exists():
        raise Exception("Archive unpack destination already exists", str(dst))

    # create parent dir if doesn't exists
    if makedirs and dst.parent != dst and not dst.parent.exists():
        os.makedirs(dst.parent)

    # download file
    archive = dst.parent / url.split('/')[-1]
    urllib.request.urlretrieve(url, archive)

    shutil.unpack_archive(archive, extract_dir=dst)

    # check if unpacked folder contains only 1 folder (recursively), if so move its content to parent folder
    content = os.listdir(dst)
    while len(content) == 1 and Path(content[0]).is_dir:
        shutil.move(f"{dst}", f"{dst}_temp")
        shutil.move(f"{dst}_temp/{content[0]}", dst)
        os.rmdir(f"{dst}_temp")
        content = os.listdir(dst)

    if delete_archive:
        os.remove(archive)


if __name__ == "__main__":
    # url = 'https://www.tcpdump.org/release/libpcap-1.10.0.tar.gz'
    url = "https://file-examples-com.github.io/uploads/2017/02/zip_2MB.zip"
    download_archive(url, './tmp/zip_2MB')
