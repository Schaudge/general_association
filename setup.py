#!/usr/bin/env python3
# General Association Packge
# Written By Schaudge King
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages










setup(name='ga',
      version='0.0.1',
      description='general association for bioinformatics',
      author='Schaudge King',
      author_email='yuanshenran@yeah.net',
      license='MIT',
      packages=find_packages(),
      entry_points={'console_scripts': ['ga = ga.association:main',]}
      )
