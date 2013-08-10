#!/usr/bin/env python
from setuptools import setup, find_packages

REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()]

__version__ = '0.0.2'

setup(
    name='butler',
    url='http://www.github.com/pod2metra/butler/',
    packages=find_packages(
        exclude=(
            'test_project',
            'tests',
        )
    ),
    version=__version__,
    include_package_data=True,
    install_requires=[REQUIREMENTS],
)
