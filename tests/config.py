import os

LDAP_CONFIG =  {'ldap-config' : os.path.abspath('tests/fixture/valid-ldap.yaml')}
LDAP_CONFIG_INVALID =  {'ldap-config' : os.path.abspath('tests/fixture/invalid-ldap.yaml')}

LDAP_USER = os.environ['LDAP_TEST_USER']
LDAP_PASSWORD = os.environ['LDAP_TEST_PASSWORD']
LDAP_GROUP = os.environ['LDAP_TEST_GROUP']

NATIVE_USER = 'test-user'
NATIVE_PASSWORD = 'test-password'
