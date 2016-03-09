import os
import unittest

from devpi_plumber.server import TestServer

from tests.config import NATIVE_USER, NATIVE_PASSWORD
from tests.utils import download, wait_until


PYTHON_PACKAGE = os.path.abspath("dist") # just use the package containing these tests



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
            master.upload(PYTHON_PACKAGE, directory=True)

            with TestServer(config={'master-url': master.server_url, 'port': 2413}) as replica1:
                replica1.use(NATIVE_USER, 'index')

                self.assertTrue(download('devpi_acceptancetests', replica1.url))
                master.remove('devpi_acceptancetests')
                self.assertFalse(download('devpi_acceptancetests', replica1.url))

                with TestServer(config={'master-url': master.server_url, 'port': 2412}) as replica2:
                    replica2.use(NATIVE_USER, 'index')

                    self.assertFalse(download('devpi_acceptancetests', replica2.url))

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
                    replica1.upload(PYTHON_PACKAGE, directory=True)

                    wait_until(lambda: download('devpi_acceptancetests', replica2.url) == True)

                    replica1.remove('devpi_acceptancetests')

                    wait_until(lambda: download('devpi_acceptancetests', replica2.url) == False)
