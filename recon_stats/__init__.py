#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" __init__.py

recon_stats:

A python package to parse statistics generated from recon-all
"""
__author__ = 'Scott Burns <scott.s.burns@vanderbilt.edu>'
__copyright__ = 'Copyright 2012 Vanderbilt University. All Rights Reserved'
__version__ = '0.0'

from .io import Parser, Measure
from .core import Subject
