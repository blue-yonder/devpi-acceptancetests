from twitter.common.contextutil import temporary_dir
import unittest

from devpi_plumber.server import TestServer, export_state, import_state

from tests.config import NATIVE_USER, NATIVE_PASSWORD
from tests.fixture import DIST_DIR, PACKAGE_NAME
from tests.utils import download


class ExportImportTests(unittest.TestCase):

    def test_export_import(self):
        users = {NATIVE_USER: {'password': NATIVE_PASSWORD}}
        indices = {NATIVE_USER + '/index': {'bases': 'root/pypi'}}

        with temporary_dir() as state_dir:
            with temporary_dir() as server_dir1:
                with TestServer(users, indices, config=dict(serverdir=server_dir1)) as devpi:
                    devpi.login(NATIVE_USER, NATIVE_PASSWORD)
                    devpi.use(NATIVE_USER, 'index')
                    devpi.upload(DIST_DIR, directory=True)
                export_state(server_dir1, state_dir)

            with temporary_dir() as server_dir2:
                import_state(server_dir2, state_dir)
                with TestServer(config=dict(serverdir=server_dir2)) as devpi:
                    devpi.login(NATIVE_USER, NATIVE_PASSWORD)
                    devpi.use(NATIVE_USER, 'index')
                    self.assertTrue(download(PACKAGE_NAME, devpi.url))
