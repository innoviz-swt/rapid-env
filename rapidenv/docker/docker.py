import subprocess

from rapidenv.osh import run_process, run_process_with_stdout

__SPACER__ = '    '


def rm_all():
    """
    attempt to remove all running docker containers specified in docker ps -a
    """
    # get ids of running container
    ids = []
    stdout = run_process_with_stdout('docker ps -a')
    # assumption: first line is header, last line is empty
    for line in stdout.split('\n')[1:-1]:
        ids += [line.split(f'{__SPACER__}')[0]]

    # remove all containers
    run_process(f"docker rm {' '.join(ids)}", raise_exception=False)


# def dist(...):
# docker build . -t innovizswt/swt-xenial-docker:0.0.0
# docker push innovizswt/swt-xenial-docker:0.0.0
# docker run -it innovizswt/swt-xenial-docker:0.0.0 --rm --name swtxenial
