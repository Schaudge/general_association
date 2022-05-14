#!/usr/bin/env python3
# General Association Packge
# Written By Schaudge King
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


setup(name='general_association',
      version='0.0.1',
      description='general association for bioinformatics',
      author='Schaudge King',
      license='MIT',
      packages=['src'],
      entry_points={'console_scripts': ['ga = association:main',]}
      )
