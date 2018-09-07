# -*- coding: utf-8 -*-
"""
Created on Sat Jul 14 07:04:24 2018

@author: glawson
"""

import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="variable",
    version="0.0.4",
    author="gtlawson",
    author_email="glawson014@gmail.com",
    description="Forward and Backward Variable Selection",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gtlawson/variable/",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)