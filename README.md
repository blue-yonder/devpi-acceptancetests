Devpi Acceptance Tests
=======================

[![Build Status](https://travis-ci.org/blue-yonder/devpi-acceptancetests.svg?branch=master)](https://travis-ci.org/blue-yonder/devpi-acceptancetests)
[![Requirements Status](https://requires.io/github/blue-yonder/devpi-acceptancetests/requirements.png?branch=master)](https://requires.io/github/blue-yonder/devpi-acceptancetests/requirements/?branch=master)

We rely on some devpi features and want to make sure they continue to work as expected.

How to run the tests
--------------------

Run the tests

    nosetests

Travis runs the tests without LDAP support. If you want to enable them (as we do
internally to check against our own LDAP server), replace the configuration in
`tests/fixture/valid-ldap.yml` and define the following environment variables:

    export LDAP_TEST_USER=myuser
    export LDAP_TEST_PASSWORD=mypassword
    export LDAP_TEST_GROUP=a-group-of-myuser


Update requirements
-------------------

Simply run the following command to update the `requirements.txt` with the lastest
Devpi version:

    pip-compile --upgrade --no-index requirements.in


License
-------

[New BSD](COPYING)
