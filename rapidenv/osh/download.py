import shutil
from pathlib import Path

def download(url, dst, makedirs=True, unpack=False, skip_dst_exists=False):
    """
    copy (file) or copytree (dir)
    if src doesn't exist FileExistsError is thrown

    src        dst            action
    ----       -------------  ---------------------------------------
    url(file)  file           dst file is overwritten
    url(file)  dir            src file is copied to dst/file
    url(file)  doesn't exist  src file is copied to dst path

    :param src: source url, source must be file url
    :param dst: destination path
    :param makedirs: create dst parent dir tree if not exists
    :param unpack: unpack downloaded file (.zip or .tar)
    :param skip_dst_exists: do nothing if dst exists
    :return:
    """

    import urllib.request
    import os

    dst = Path(dst)

    # explicit dst path in case src is file and dst is dir
    if dst.is_dir():
        dst = dst / url.split('/')[-1]

    # do nothing if dst exists and skip_dst_exists flag is raised
    if skip_dst_exists and dst.exists():
        return

    # create parent dir if doesn't exists
    if makedirs and dst.parent != dst and not dst.parent.exists():
        os.makedirs(dst.parent)

    # download file
    urllib.request.urlretrieve(url, dst)

    if unpack:
        s_dst = str(dst)
        suffix = None
        supported = ['.zip', '.tar.gz']
        for s in supported:
            if s_dst.endswith(s):
                suffix = s
        if suffix is None:
            raise Exception(f"Unsupported archive type to unpack {dst}, supported: {', '.join(supported)}")

        s_dst_trim = s_dst[:-len(suffix)]

        shutil.unpack_archive(s_dst, extract_dir=s_dst_trim)

        # check if unpacked folder contains only 1 folder, if so move its content to parent folder
        content = os.listdir(s_dst_trim)
        if len(content) == 1 and Path(content[0]).is_dir:
            shutil.move(f"{s_dst_trim}", f"{s_dst_trim}_temp")
            shutil.move(f"{s_dst_trim}_temp/{content[0]}", str(dst.parent / content[0]))
            os.rmdir(f"{s_dst_trim}_temp")


if __name__ == __main__:
    url = 'https://www.tcpdump.org/release/libpcap-1.10.0.tar.gz'
    download(url, './tmp')
