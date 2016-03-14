from contextlib import contextmanager
import os
import requests
import unittest

from devpi_plumber.server import TestServer

from tests.config import NATIVE_USER, NATIVE_PASSWORD, LDAP_CONFIG
from tests.fixture import SOURCE_DIR
from tests.utils import cd, wait_until


OTHER_USER = "otheruser"
OTHER_PASSWORD = "otherpassword"


@contextmanager
def cd(path):
    old_dir = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old_dir)


class DocUploadTests(unittest.TestCase):

    def test_upload(self):
        users = {NATIVE_USER: {'password': NATIVE_PASSWORD}}
        indices = {NATIVE_USER + '/index': {}}

        with TestServer(users=users, indices=indices, config=LDAP_CONFIG) as devpi:

            devpi.use(NATIVE_USER, 'index')
            devpi.login(NATIVE_USER, NATIVE_PASSWORD)

            with cd(SOURCE_DIR):
                devpi.upload(path=None, with_docs=True)

            wait_until(
                lambda: requests.get(
                    devpi.server_url + "/{}/index/test-package/0.1/+d/index.html".format(NATIVE_USER),
                ).status_code == 200,
                maxloop=300,
            )
