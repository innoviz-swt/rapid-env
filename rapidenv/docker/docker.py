# docker build . -t innovizswt/swt-xenial-docker:0.0.0
# docker push innovizswt/swt-xenial-docker:0.0.0
# docker run -it innovizswt/swt-xenial-docker:0.0.0 --rm --name swtxenial
import subprocess

from rapidenv.process import run_process

__SPACER__ = '    '


def rm_all():
    """
    attempt to remove all running docker containers specified in docker ps -a
    """
    # get ids of running container
    ids = []
    p = run_process('docker ps -a', stdout=subprocess.PIPE)
    stdout = p.stdout.read().decode()
    # assumption: first line is header, last line is empty
    for line in stdout.split('\n')[1:-1]:
        ids += [line.split(f'{__SPACER__}')[0]]

    # remove all containers
    run_process(f"docker rm {' '.join(ids)}", raise_exception=False)


if __name__ == '__main__':
    rm_all()
