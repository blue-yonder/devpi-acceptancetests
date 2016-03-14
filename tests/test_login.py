import unittest

from devpi_plumber.client import DevpiClientError
from devpi_plumber.server import TestServer
from tests.config import (
    LDAP_CONFIG,
    LDAP_CONFIG_INVALID,
    LDAP_PASSWORD,
    LDAP_USER,
    NATIVE_PASSWORD,
    NATIVE_USER,
    ldap_integration_test
)


class NativeLoginTest(unittest.TestCase):
    """
    Assert the behaviour of the classic devpi login (even when LDAP is enabled)
    """

    def test_login_success(self):
        users = {NATIVE_USER: {'password': NATIVE_PASSWORD}}

        with TestServer(users=users, config=LDAP_CONFIG) as devpi:
            self.assertIn('credentials valid', devpi.login(NATIVE_USER, NATIVE_PASSWORD))

    def test_login_failure(self):
        users = {NATIVE_USER: {'password': NATIVE_PASSWORD}}

        with TestServer(users=users, config=LDAP_CONFIG) as devpi:

            with self.assertRaisesRegexp(DevpiClientError, '401 Unauthorized'):
                devpi.login(NATIVE_USER, "wrong-password")


@ldap_integration_test
class LdapLoginTest(unittest.TestCase):
    """
    Assert the behaviour of the LDAP-powered devpi login
    """

    def test_login_success(self):
        with TestServer(config=LDAP_CONFIG) as devpi:
            self.assertIn('credentials valid', devpi.login(LDAP_USER, LDAP_PASSWORD))

    def test_login_failure(self):
        with TestServer(config=LDAP_CONFIG) as devpi:

            with self.assertRaisesRegexp(DevpiClientError, '401 Unauthorized'):
                devpi.login(LDAP_USER, "wrong-password")

    def test_proxy_auth_on_replica(self):
        master_config = {'port': 2414}
        master_config.update(LDAP_CONFIG)

        with TestServer(config=master_config) as devpi:
            with TestServer(config={'master-url': devpi.url, 'port': 2413}) as replica:

                self.assertIn('credentials valid', replica.login(LDAP_USER, LDAP_PASSWORD))

    def test_server_unavailable(self):
        with TestServer(config=LDAP_CONFIG_INVALID, fail_on_output=[]) as devpi:

            with self.assertRaisesRegexp(DevpiClientError, '401 Unauthorized'):
                devpi.login(LDAP_USER, LDAP_PASSWORD)

    def test_ldap_user_shadows_native_user(self):
        """
        The LDAP password of the user should overrule his native password, i.e.,
        when LDAP says no a user has no chance to log in.
        """
        users = {LDAP_USER: {'password': NATIVE_PASSWORD}}

        with TestServer(users=users, config=LDAP_CONFIG) as devpi:

            with self.assertRaisesRegexp(DevpiClientError, '401 Unauthorized'):
                devpi.login(LDAP_USER, NATIVE_PASSWORD)

            self.assertIn('credentials valid', devpi.login(LDAP_USER, LDAP_PASSWORD))

    def test_ldap_user_on_unavailable_server_shadows_native_user(self):
        """
        The LDAP password of the user should overrule his native password,
        even when the LDAP server is temporarily unavailable
        """
        users = {LDAP_USER: {'password': NATIVE_PASSWORD}}

        with TestServer(users=users, config=LDAP_CONFIG_INVALID, fail_on_output=[]) as devpi:

            with self.assertRaisesRegexp(DevpiClientError, '401 Unauthorized'):
                devpi.login(LDAP_USER, NATIVE_PASSWORD)

            with self.assertRaisesRegexp(DevpiClientError, '401 Unauthorized'):
                devpi.login(LDAP_USER, LDAP_PASSWORD)
