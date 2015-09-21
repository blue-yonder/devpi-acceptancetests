# coding=utf-8

import multiprocessing  # avoid crash on teardown
from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

setup(
    name='devpi-acceptancetests',
    version='0.1.0',
    packages=find_packages(exclude=['tests']),
    author='Stephan Erb',
    author_email='stephan.erb@blue-yonder.com',
    url='https://github.com/blue-yonder/devpi-acceptancetests',
    description='Acceptance tests for our devpi setup',
    long_description=readme,
    license='new BSD',
    install_requires=[
        'devpi-plumber',
        'devpi-ldap'
    ],
    setup_requires=[
        'nose'
    ],
    tests_require=[
        'nose',
        'coverage<4',
    ],
    test_suite='nose.collector',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Topic :: System :: Archiving :: Packaging',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
)
