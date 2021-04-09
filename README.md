Devpi Acceptance Tests
=======================

Please note that we are no longer relying on this specific standalone set of Devpi acceptance tests and thus they are **no longer maintained**. We are keeping the code public for reference by anybody that might find it useful.

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
