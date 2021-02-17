# source: https://gist.github.com/jlinoff/0f7b290dc4e1f58ad803
import os
import sys
import time


def _copy_large_file(src, dst, chunk_size, copied):
    '''
    Copy a large file showing progress.
    '''
    # Start the timer and get the size.
    start = time.time()
    size = os.stat(src).st_size

    # Adjust the chunk size to the input size.
    if chunk_size > size:
        chunk_size = size
    print(f'chunk size is {chunk_size}')

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
                print(f'{per:>6.1f}% {eststr}', end='\r')

                # Read in the next chunk.
                chunk = ifp.read(chunk_size)


def copy_large_file(src, dst, chunk_size=10 * 1024 * 1024, retries=3, retry_delay=1):
    '''
    Copy a large file showing progress.
    '''
    print(f'copying "{src}" --> "{dst}"')
    if not os.path.exists(src):
        print('ERROR: file does not exist: "{}"'.format(src))
        exit(1)
    # if os.path.exists(dst) is True:
    #     os.remove(dst)
    # if os.path.exists(dst) is True:
    #     print('ERROR: file exists, cannot overwrite it: "{}"'.format(dst))
    #     sys.exit(1)

    if os.path.exists(dst):
        size = os.stat(dst).st_size
        copied = [size]
    else:
        copied = [0]

    # Start the timer and get the size.
    start = time.time()
    print(f'{os.stat(src).st_size} bytes')

    for i in range(retries):
        try:
            _copy_large_file(src, dst, chunk_size, copied)
            break
        except Exception as e:
            print(f"Copy failure, retry {i+1} of {retries} retries, "
                  f"{retry_delay} sec retry delay, Error: {e}")

            # sanity validation
            if (os.stat(dst).st_size != copied[0]):
                print(f"Error: dst size ('{os.stat(dst).st_size}') "
                      f"doesn't match bytes copied ('{copied[0]}').")
                exit(1)

            time.sleep(retry_delay)

    elapsed = time.time() - start
    print()
    print(f'copied in {elapsed:>.1f}s"')


if __name__ == '__main__':
    src = sys.argv[1]
    dst = sys.argv[2]

    copy_large_file(src, dst)