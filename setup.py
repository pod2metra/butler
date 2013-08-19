#!/usr/bin/env python
from setuptools import setup, find_packages

__version__ = '0.0.2'

setup(
    name='butler',
    url='http://www.github.com/pod2metra/butler/',
    packages=find_packages(
        exclude=(
            'test_project',
        )
    ),
    version=__version__,
    include_package_data=True,
    install_requires=[
        'xmldict==0.4.1',
        'PyYAML==3.10',
        'python-dateutil==2.1',
        'six==1.3.0',
        'ujson==1.33'
    ],
)
