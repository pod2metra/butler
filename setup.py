#!/usr/bin/env python
from distutils.core import setup
from setuptools import find_packages

setup(
    name='butler',
    url='http://www.github.com/pod2metra/butler/',
    packages=find_packages(),
    include_package_data=True,
    requires=[
        'django>1.4',
    ],
)
