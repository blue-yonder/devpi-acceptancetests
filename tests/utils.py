import subprocess
from time import sleep

from twitter.common.contextutil import temporary_dir


def wait_until(predicate, exception=RuntimeError, maxloop=30):
    n = 0
    while not predicate() and n < maxloop:
        sleep(0.1)
        n += 1
    if n >= maxloop:
        raise exception


def download(pkg, server_url):
    with temporary_dir() as scratch_dir:
        try:
            subprocess.check_output(
                [
                    'pip',
                    '--no-cache-dir',
                    '--isolated',
                    'download', pkg,
                    '--dest', scratch_dir,
                    '--index-url', server_url,
                ],
                stderr=subprocess.STDOUT
            )
            return True
        except subprocess.CalledProcessError:
            return False
