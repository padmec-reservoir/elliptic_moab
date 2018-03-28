#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

requirements = ['elliptic', 'pymoab']

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author="Guilherme Praciano Karst Caminha",
    author_email='gpkc@cin.ufpe.br',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
    ],
    description="MOAB backend for ELLIPTIc.",
    install_requires=requirements,
    license="MIT license",
    include_package_data=True,
    keywords='elliptic_moab',
    name='elliptic_moab',
    packages=find_packages(include=['elliptic_moab']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/gpkc/elliptic_moab',
    version='0.1.0',
    zip_safe=False,
)
