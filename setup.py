#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (C) 2017 IBM Corporation

Licensed under the Apache License, Version 2.0 (the “License”);
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an “AS IS” BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

    Contributors:
        * Rafael Sene <rpsene@br.ibm.com>
"""

from setuptools import setup, find_packages
from pip.req import parse_requirements

with open('README.rst') as f:
    README = f.read()

REQUIREMENTS_LIST = parse_requirements('./requirements.txt', session=False)
REQUIREMENTS = [str(required.req) for required in REQUIREMENTS_LIST]

setup(
    name='mambo',
    version='1.0.timestamp',
    description='IBM POWER8 and POWER9 Functional Simulator',
    long_description=README,
    author='Rafael Peria de Sene',
    author_email='rpsene@br.ibm.com',
    url='https://www-304.ibm.com/webapp/set2/sas/f/lopdiags/sdklop.html',
    license='Apache Software License 2.0',
    install_requires=REQUIREMENTS,
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    test_suite='nose.collector',
    tests_require=['nose'],
    scripts=['bin/mambo'],
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: POSIX :: Linux',
        'Topic :: System :: Emulators',
        'License :: OSI Approved :: Apache Software License 2.0',
    ],
)
