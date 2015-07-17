import os
import unittest

ldap_integration_test = unittest.skipIf('LDAP_TEST_USER' not in os.environ, "LDAP_TEST_USER env variable not defined")

LDAP_CONFIG =  {'ldap-config' : os.path.abspath('tests/fixture/valid-ldap.yaml')}
LDAP_CONFIG_INVALID =  {'ldap-config' : os.path.abspath('tests/fixture/invalid-ldap.yaml')}

LDAP_USER = os.environ.get('LDAP_TEST_USER', 'undefined')
LDAP_PASSWORD = os.environ.get('LDAP_TEST_PASSWORD', 'undefined')
LDAP_GROUP = os.environ.get('LDAP_TEST_GROUP', 'undefined')

NATIVE_USER = 'test-user'
NATIVE_PASSWORD = 'test-password'
