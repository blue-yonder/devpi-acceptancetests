import requests
from twitter.common.contextutil import pushd
import unittest

from devpi_plumber.server import TestServer
from tests.config import NATIVE_PASSWORD, NATIVE_USER
from tests.fixture import PACKAGE_VERSION, SOURCE_DIR
from tests.utils import wait_until


class DocUploadTests(unittest.TestCase):

    def test_upload(self):
        users = {NATIVE_USER: {'password': NATIVE_PASSWORD}}
        indices = {NATIVE_USER + '/index': {}}

        with TestServer(users=users, indices=indices) as devpi:

            devpi.use(NATIVE_USER, 'index')
            devpi.login(NATIVE_USER, NATIVE_PASSWORD)

            with pushd(SOURCE_DIR):
                devpi.upload(path=None, with_docs=True)

            def doc_present(version=PACKAGE_VERSION):
                return requests.get(
                    devpi.server_url + "/{}/index/test-package/{}/+d/index.html".format(NATIVE_USER, version),
                ).status_code == 200,

            wait_until(doc_present, maxloop=300)
            self.assertTrue(doc_present('+latest'))
            self.assertTrue(doc_present('+stable'))
