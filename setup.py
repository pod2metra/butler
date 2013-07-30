#!/usr/bin/env python
from setuptools import setup, find_packages

__version__ = '0.0.1'

setup(
    name='butler',
    url='http://www.github.com/pod2metra/butler/',
    packages=find_packages(),
    include_package_data=True,
    requires=[
        'django>1.4',
    ],
)
