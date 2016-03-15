from twitter.common.contextutil import temporary_dir
import unittest

from devpi_plumber.server import TestServer

from tests.config import NATIVE_USER, NATIVE_PASSWORD
from tests.fixture import DIST_DIR, PACKAGE_NAME
from tests.utils import download


class ExportImportTests(unittest.TestCase):

    def test_export_import(self):
        users = {NATIVE_USER: {'password': NATIVE_PASSWORD}}
        indices = {NATIVE_USER + '/index': {'bases': 'root/pypi'}}

        with temporary_dir() as export_dir:
            with TestServer(users, indices, export=export_dir) as devpi:
                devpi.login(NATIVE_USER, NATIVE_PASSWORD)
                devpi.use(NATIVE_USER, 'index')
                devpi.upload(DIST_DIR, directory=True)

            with TestServer(import_=export_dir) as devpi:
                devpi.login(NATIVE_USER, NATIVE_PASSWORD)
                devpi.use(NATIVE_USER, 'index')
                self.assertTrue(download(PACKAGE_NAME, devpi.url))


