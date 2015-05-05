import os
import unittest

from devpi_plumber.client import DevpiClientError
from devpi_plumber.server import TestServer

from tests.config import LDAP_CONFIG, LDAP_USER, LDAP_GROUP, LDAP_PASSWORD, NATIVE_USER, NATIVE_PASSWORD


OTHER_USER = "otheruser"
OTHER_PASSWORD = "otherpassword"
PYTHON_PACKAGE = os.path.abspath("dist") # just use the package containing these tests


class ModificationRestrictionTests(unittest.TestCase):

    def test_anonymous_user_creation(self):
        restriction = {'restrict-modify': ''}

        with TestServer(config=restriction) as devpi:
            devpi.logoff()

            with self.assertRaisesRegexp(DevpiClientError, '403 Forbidden'):
                devpi.create_user(OTHER_USER, password=OTHER_PASSWORD)

    def test_authorized_native_user(self):
        self._test_authorized(NATIVE_USER, NATIVE_PASSWORD, unrestricted=['root', str(NATIVE_USER)] )

    def test_authorized_ldap_user(self):
        self._test_authorized(LDAP_USER, LDAP_PASSWORD, unrestricted=['root', str(LDAP_USER)] )

    def test_authorized_ldap_group(self):
        self._test_authorized(LDAP_USER, LDAP_PASSWORD, unrestricted=['root', ':{}'.format(LDAP_GROUP)] )

    def _test_authorized(self, user, password, unrestricted):
        """
        An unrestricted user can do anything once logged in.
        """
        config = LDAP_CONFIG
        config.update({'restrict-modify': ",".join(unrestricted) })

        users = { user : {'password': password } }
        indices = { user + "/index" : {} }

        with TestServer(users=users, indices=indices, config=config) as devpi:

            devpi.use(user, 'index')
            devpi.login(user, password)

            # create new user
            self.assertIn("user created", devpi.create_user(OTHER_USER, password=OTHER_PASSWORD))

            # create new index
            self.assertIn(devpi.server_url, devpi.create_index(user + "/newindex"))

            # modify own user
            self.assertIn("user modified", devpi.modify_user(user, email="test@example.com"))

            # modify own index
            self.assertIn("changing volatile", devpi.modify_index(user + "/index", volatile=False))

            # upload to own index
            self.assertNotIn("FAIL", devpi.upload(PYTHON_PACKAGE, directory=True))

    def test_unauthorized_native_user(self):
        self._test_unauthorized(NATIVE_USER, NATIVE_PASSWORD, unrestricted=['root'])

    def test_unauthorized_ldap_user(self):
        self._test_unauthorized(LDAP_USER, LDAP_PASSWORD, unrestricted=['root'])

    def test_unauthorized_ldap_group(self):
        self._test_unauthorized(LDAP_USER, LDAP_PASSWORD, unrestricted=['root', ':NotOneOfMyGroups'])

    def _test_unauthorized(self, user, password, unrestricted):
        """
        A restricted user can only upload and do nothing else,
        """
        config = LDAP_CONFIG
        config.update({'restrict-modify': ",".join(unrestricted) })

        users = { user : {'password': password } }
        indices = { user + "/index" : {} }

        with TestServer(users=users, indices=indices, config=config) as devpi:

            devpi.use(user, 'index')
            devpi.login(user, password)

            # modify own user
            with self.assertRaisesRegexp(DevpiClientError, '403 Forbidden'):
                devpi.modify_user(user, password="newpassword")

            # modify own index
            with self.assertRaisesRegexp(DevpiClientError, '403 Forbidden'):
                devpi.modify_index(user + "/index", volatile=False)

            # create new user
            with self.assertRaisesRegexp(DevpiClientError, '403 Forbidden'):
                devpi.create_user(OTHER_USER, password=OTHER_PASSWORD)

            # create new index
            with self.assertRaisesRegexp(DevpiClientError, '403 Forbidden'):
                devpi.create_index(user + "/newindex")

            # upload to own index
            self.assertNotIn("FAIL", devpi.upload(PYTHON_PACKAGE, directory=True))
