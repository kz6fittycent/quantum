#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="quantum_test_pip_chdir",
    version="0",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'quantum_test_pip_chdir = quantum_test_pip_chdir:main'
        ]
    }
)
