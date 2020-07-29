import subprocess


def run_process(cmd, cwd=None, raise_exception=True):
    if cwd is not None:
        p = subprocess.Popen(cmd, cwd=cwd)
    else:
        p = subprocess.Popen(cmd)

    p.wait()

    # validate error code
    if p.returncode != 0:
        msg = f"process exited with error code '{p.returncode}'"
        print(msg)
        if raise_exception:
            raise Exception(msg)


