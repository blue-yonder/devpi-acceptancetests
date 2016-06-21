import os
import unittest
from collections import OrderedDict

from devpi_plumber.server import TestServer
from devpi_plumber.client import DevpiClientError
from tests.config import NATIVE_PASSWORD
from tests.fixture import DIST_DIR, FLASK_WHEEL


class InheritanceTests(unittest.TestCase):

    @unittest.skip("Broken in devpi 4.0.0")
    def test_correct_resolution_order(self):
        """
        We assert two points:
        * Mirrors should not shadow packages available on internal indices.
        * Internal indices are checked before mirrors so that we know about
          whitelisted packages.

        https://bitbucket.org/hpk42/devpi/issues/214/issues-with-recursive-index-lookups
        """
        users = {'user': {'password': NATIVE_PASSWORD}}
        indices = OrderedDict([
            ('user/baseindex1', {}),
            ('user/baseindex2', {'bases': 'user/baseindex1'}),
            ('user/index', {'bases': 'user/baseindex2,root/pypi'})
        ])
        with TestServer(users, indices) as master:
            master.use('user', 'baseindex1')
            master.login('user', NATIVE_PASSWORD)
            master.upload(os.path.join(DIST_DIR, FLASK_WHEEL))

            master.use('user', 'index')
            self.assertEqual(len(master.list('flask')), 1)

