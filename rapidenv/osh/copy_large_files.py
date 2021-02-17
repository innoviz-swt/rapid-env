# source: https://gist.github.com/jlinoff/0f7b290dc4e1f58ad803
import os
import sys
import time
from pathlib import Path


def _copy_large_file(src, dst, chunk_size, copied, log):
    '''
    Copy a large file showing progress.
    '''
    # Start the timer and get the size.
    start = time.time()
    size = os.stat(src).st_size

    # Adjust the chunk size to the input size.
    if chunk_size > size:
        chunk_size = size
    if log:
        log(f'chunk size is {chunk_size}')

    # Copy.
    session_copied = 0
    with open(src, 'rb') as ifp:
        # advance input to relevant position
        ifp.seek(copied[0])
        with open(dst, 'ab') as ofp:
            chunk = ifp.read(chunk_size)
            while chunk:
                # Write and calculate how much has been written so far.
                ofp.write(chunk)
                ofp.flush()
                copied[0] += len(chunk)
                session_copied += len(chunk)
                per = 100. * float(copied[0]) / float(size)

                # Calculate the estimated time remaining.
                elapsed = time.time() - start  # elapsed so far
                avg_time_per_byte = elapsed / float(session_copied)
                remaining = size - copied[0]
                est = remaining * avg_time_per_byte / 60  # minutes
                est1 = size * avg_time_per_byte / 60      # minutes
                eststr = f'rem={est:>.1f} min, tot={est1:>.1f} min'

                # Write out the status.
                if log:
                    print(f'{per:>6.1f}% {eststr}', end='\r')

                # Read in the next chunk.
                chunk = ifp.read(chunk_size)


def copy_large_file(src, dst, chunk_size=10 * 1024 * 1024, retries=3,
                    retry_delay=1, log=lambda *kargs, **vargs: ()):
    """
    copy src file to dst file

    :param src: source file path
    :param dst: destination file path
    :param chunk_size: single write chunk size, 10M is used as default
    :param retries: number of retries per file write failure
    :param retries_delay: number of dealys between retries per file write failure
    """
    log(f'copying "{src}" --> "{dst}"')

    if os.path.exists(dst):
        size = os.stat(dst).st_size
        copied = [size]
    else:
        copied = [0]

    # Start the timer and get the size.
    start = time.time()
    log(f'{os.stat(src).st_size} bytes')

    for i in range(retries):
        try:
            _copy_large_file(src, dst, chunk_size, copied, log)
            break
        except Exception as e:
            log(f"Copy failure, retry {i+1} of {retries} retries, "
                f"{retry_delay} sec retry delay, Error: {e}")

            # sanity validation
            if (os.stat(dst).st_size != copied[0]):
                raise Exception(f"Error: dst size ('{os.stat(dst).st_size}') "
                                f"doesn't match bytes copied ('{copied[0]}').")

            time.sleep(retry_delay)

    elapsed = time.time() - start
    log()
    log(f'copied in {elapsed:>.1f}s')


def copy_large(src, dst, chunk_size=10 * 1024 * 1024, retries=3,
               retry_delay=1, makedirs=True, log=lambda *kargs, **vargs: ()):
    """
    copy (file) or copytree (dir)
    if src doesn't exist FileExistsError is thrown

    src    dst            action
    ----   -------------  ---------------------------------------
    file   file           dst file is copied \ appended until reaches src file size
    file   dir            src file is copied to dst/file
    file   doesn't exist  src file is copied to dst path
    dir    file           Exception is thrown
    dir    dir            src dir content is copied to dst dir (copytree)
    dir    doesn't exist  src dir is copied to dst path (copytree)

    :param src: source path
    :param dst: destination path
    :param chunk_size: single write chunk size, 10M is used as default
    :param retries: number of retries per file write failure
    :param retries_delay: number of dealys between retries per file write failure
    :param makedirs: create parent dir tree if not exists
    :param log callback, used as print function
    :return:
    """
    src = Path(src)
    dst = Path(dst)

    # validate source exists
    if not src.exists():
        raise FileExistsError(f"src '{src.absolute()}' does not exists")

    if src.is_dir() and dst.is_file():
        raise Exception(f"can't copy dir to file. '{src}' is dir,"
                        f"'{dst}' is file. ")

    # explicit dst path in case src is file and dst is dir
    if src.is_file() and dst.is_dir():
        dst = dst / src.name

    # create parent dir if doesn't exists
    if makedirs and dst.parent != dst and not dst.parent.exists():
        os.makedirs(dst.parent)

    if src.is_dir():
        # if dst doesnt exists create dst as folder
        if not dst.exists():
            os.makedirs(dst)

        for root, dirs, files in os.walk(src):
            rel = (Path(root)).relative_to(src)
            # create dir if such doesn't exists
            for dir in dirs:
                dpath = dst / rel / dir
                if not dpath.exists():
                    os.makedirs(dpath)

            # copy files
            for file in files:
                fpath = dst / rel / file
                copy_large_file(f"{root}/{file}", str(fpath), chunk_size,
                                retries, retry_delay, log)

    elif src.is_file():
        copy_large_file(str(src), str(dst), chunk_size, 
                        retries, retry_delay, log)

    else:
        raise RuntimeError(f"Unsupported source path type: {src}")


def main():
    src = sys.argv[1]
    dst = sys.argv[2]

    def log(*vargs, **kargs):
        print(*vargs, **kargs)

    copy_large(src, dst, log=log)


if __name__ == '__main__':
    main()
