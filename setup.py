#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from setuptools import find_packages

setup(
    name='butler',
    url='http://www.github.com/pod2metra/butler/',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Django >= 1.4.3",
    ],
)
