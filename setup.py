#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import sys
import re
import os.path as op

from setuptools import setup

def get_version():
    contents = ''

    with open(op.join('airwatch', '__init__.py'), 'r') as infile:
        contents = infile.read()

    try:
        version = re.search(r"__version__ = '(.+)'", contents).group(1)
    except Exception as e:
        raise Exception('Unable to find version. Files may be damaged.')

    return version

name='pyAirWatch'
version=get_version()
description='Library for communicating with AirWatch via REST.'

author='Benedicte Emilie BrÃ¦kken'
author_email='b.e.brakken@usit.uio.no'

packages=['airwatch']

install_requires=[
    'requests',
]

setup(name=name,
      version=version,
      description=description,
      author=author,
      author_email=author_email,
      packages=packages,
      install_requires=install_requires)
