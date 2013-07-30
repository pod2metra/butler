#!/usr/bin/env python
from setuptools import setup

REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()]

__version__ = '0.0.1'

setup(
    name='butler',
    url='http://www.github.com/pod2metra/butler/',
    packages=('butler',),
    version='v0.1.0',
    include_package_data=True,
    install_requires=[REQUIREMENTS],
)
