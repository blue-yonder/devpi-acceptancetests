Devpi Acceptance Tests
=======================

We rely on some devpi features and want to make sure they continue to work as expected.

How to run the tests
--------------------

Provide some details about your LDAP environment:

    export LDAP_TEST_USER=myuser
    export LDAP_TEST_PASSWORD=mypassword
    export LDAP_TEST_GROUP=a-group-where-myuser-is-part-of

Create the test fixtures (otherwise the upload tests will fail)

    python setup.py sdist

Run the tests

    python setup.py test

License
-------

[New BSD](COPYING)
