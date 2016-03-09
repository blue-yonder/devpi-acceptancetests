import os
import subprocess
import unittest

from devpi_plumber.server import TestServer
from twitter.common.contextutil import temporary_dir

from tests.config import NATIVE_USER, NATIVE_PASSWORD


PYTHON_PACKAGE = os.path.abspath("dist") # just use the package containing these tests


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


class DownloadTests(unittest.TestCase):

    def assert_pypi_downloads(self, devpi):
        devpi.use('root', 'pypi')
        self.assertTrue(download('progressbar', devpi.url))
        self.assertFalse(download('non_existing_package', devpi.url))

        # A package which used to exist on PyPi but is now gone.
        # This special case used to trigger tracebacks in Devpi.
        self.assertFalse(download('mesos.native', devpi.url))

    def assert_internal_downloads(self, devpi):
        devpi.use(NATIVE_USER, 'index')
        devpi.login(NATIVE_USER, NATIVE_PASSWORD)

        self.assertTrue(download('progressbar', devpi.url))
        self.assertFalse(download('non_existing_package', devpi.url))

        self.assertFalse(download('devpi-acceptancetests', devpi.url))
        devpi.upload(PYTHON_PACKAGE, directory=True)
        self.assertTrue(download('devpi_acceptancetests', devpi.url))

    def test_master(self):
        users = { NATIVE_USER: {'password': NATIVE_PASSWORD} }
        indices = { NATIVE_USER + '/index' : {'bases': 'root/pypi'} }

        with TestServer(users, indices) as devpi:
            self.assert_pypi_downloads(devpi)
            self.assert_internal_downloads(devpi)

    def test_replica(self):
        users = { NATIVE_USER: {'password': NATIVE_PASSWORD} }
        indices = { NATIVE_USER + '/index' : {'bases': 'root/pypi'} }

        with TestServer(users, indices, config={'port' : 2414 }) as master:
            with TestServer(config={'master-url': master.url, 'port': 2413}) as replica:

                self.assert_pypi_downloads(replica)
                self.assert_internal_downloads(replica)
