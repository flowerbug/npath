#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) Flowerbug <flowerbug@anthive.com>

from os import path
from setuptools import setup, find_packages

from npath.version import GetVersion


# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


__version__ = GetVersion()


setup(
    name="npath",
    version=__version__,
    author="Flowerbug",
    author_email="flowerbug@anthive.com",
    description="A variable grid framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.github.com/flowerbug/npath",
    license="Apache-2.0",
    setup_requires=["setuptools >= 40.6.3",
                    "twine >= 1.12.1",
                    "wheel >= 0.32.3"
                    ],
    packages=find_packages(),
    install_requires=["pyglet >= 2.0.dev6"
                     ],
    provides=["npath"],
    include_package_data=True,
    entry_points={
        "console_scripts": ["runnpath = npath.npath:main"]
                 },
    python_requires=">=3",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Games/Entertainment :: Puzzle Games"
    ],
)
