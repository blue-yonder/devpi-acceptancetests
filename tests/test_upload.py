import os
import unittest

from devpi_plumber.client import DevpiClientError
from devpi_plumber.server import TestServer

from tests.config import ldap_integration_test
from tests.config import NATIVE_USER, NATIVE_PASSWORD, LDAP_CONFIG, LDAP_USER, LDAP_GROUP, LDAP_PASSWORD


OTHER_USER = "otheruser"
OTHER_PASSWORD = "otherpassword"
PYTHON_PACKAGE = os.path.abspath("dist") # just use the package containing these tests


class UploadPermissionTests(unittest.TestCase):

    def _test_upload(self, owner_user, owner_password, login_user, login_password, index_options):
        users = { owner_user: {'password': owner_password}, login_user: {'password': login_password} }
        indices = { owner_user + '/index' : index_options }

        with TestServer(users=users, indices=indices, config=LDAP_CONFIG) as devpi:

            devpi.use(owner_user, 'index')
            devpi.login(login_user, login_password)

            self.assertNotIn("FAIL", devpi.upload(PYTHON_PACKAGE, directory=True))

    def test_upload_to_own_index(self):
        options = {}
        self._test_upload(
            owner_user=NATIVE_USER,
            owner_password=NATIVE_PASSWORD,
            login_user=NATIVE_USER,
            login_password=NATIVE_PASSWORD,
            index_options=options)

    def test_upload_to_foreign_index(self):
        options = {}
        with self.assertRaisesRegexp(DevpiClientError, "403 FAIL"):
            self._test_upload(
                owner_user=NATIVE_USER,
                owner_password=NATIVE_PASSWORD,
                login_user=OTHER_USER,
                login_password=OTHER_PASSWORD,
                index_options=options)

    def test_upload_allowed_via_user_acl(self):
        options = {'acl_upload': str(OTHER_USER)}
        self._test_upload(
            owner_user=NATIVE_USER,
            owner_password=NATIVE_PASSWORD,
            login_user=OTHER_USER,
            login_password=OTHER_PASSWORD,
            index_options=options)

    @ldap_integration_test
    def test_upload_allowed_via_group_acl(self):
        options = {'acl_upload': ':{}'.format(LDAP_GROUP)}
        self._test_upload(
            owner_user=OTHER_USER,
            owner_password=OTHER_PASSWORD,
            login_user=LDAP_USER,
            login_password=LDAP_PASSWORD,
            index_options=options)

    def test_upload_on_own_index_denied_via_acl(self):
        options = {'acl_upload': ''}
        with self.assertRaisesRegexp(DevpiClientError, "403 FAIL"):
            self._test_upload(
                owner_user=NATIVE_USER,
                owner_password=NATIVE_PASSWORD,
                login_user=NATIVE_USER,
                login_password=NATIVE_PASSWORD,
                index_options=options)
