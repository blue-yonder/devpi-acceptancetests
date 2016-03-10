import os
import unittest

from devpi_plumber.server import TestServer

from tests.config import NATIVE_USER, NATIVE_PASSWORD
from tests.fixture import PACKAGE_DIR, PACKAGE_NAME
from tests.utils import download


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

        self.assertFalse(download(PACKAGE_NAME, devpi.url))
        devpi.upload(PACKAGE_DIR, directory=True)
        self.assertTrue(download(PACKAGE_NAME, devpi.url))

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
