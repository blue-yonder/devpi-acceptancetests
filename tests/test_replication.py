import os
import unittest

from devpi_plumber.server import TestServer

from tests.config import NATIVE_USER, NATIVE_PASSWORD
from tests.fixture import DIST_DIR, PACKAGE_NAME
from tests.utils import download, wait_until


class ReplicationTests(unittest.TestCase):

    def test_late_replication(self):
        """
        Test that the replicas are properly catching up with changes, even
        if they were not online when the change happened.

        This sometimes used to result in tracebacks.
        """
        users = { NATIVE_USER: {'password': NATIVE_PASSWORD} }
        indices = { NATIVE_USER + '/index' : {'bases': 'root/pypi'} }

        with TestServer(users, indices, config={'port' : 2414 }) as master:
            master.use(NATIVE_USER, 'index')
            master.login(NATIVE_USER, NATIVE_PASSWORD)
            master.upload(DIST_DIR, directory=True)

            with TestServer(config={'master-url': master.server_url, 'port': 2413}) as replica1:
                replica1.use(NATIVE_USER, 'index')

                wait_until(lambda: download(PACKAGE_NAME, replica1.url) is True)
                master.remove(PACKAGE_NAME)
                wait_until(lambda: download(PACKAGE_NAME, replica1.url) is False)

                with TestServer(config={'master-url': master.server_url, 'port': 2412}) as replica2:
                    replica2.use(NATIVE_USER, 'index')

                    wait_until(lambda: download(PACKAGE_NAME, replica2.url) is False)

    def test_cross_replica_synchronization(self):
        """
        Any change performed by a replica should be observable by another one.
        """
        users = { NATIVE_USER: {'password': NATIVE_PASSWORD} }
        indices = { NATIVE_USER + '/index' : {'bases': 'root/pypi'} }

        with TestServer(users, indices, config={'port' : 2414 }) as master:
            with TestServer(config={'master-url': master.server_url, 'port': 2413}) as replica1:
                with TestServer(config={'master-url': master.server_url, 'port': 2412}) as replica2:
                    replica1.use(NATIVE_USER, 'index')
                    replica2.use(NATIVE_USER, 'index')

                    replica1.login(NATIVE_USER, NATIVE_PASSWORD)
                    replica1.upload(DIST_DIR, directory=True)

                    wait_until(lambda: download(PACKAGE_NAME, replica2.url) is True)
                    replica1.remove(PACKAGE_NAME)
                    wait_until(lambda: download(PACKAGE_NAME, replica2.url) is False)
