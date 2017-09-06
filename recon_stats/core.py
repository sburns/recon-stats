#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" core.py

Main recon_stats code

"""
__author__ = 'Scott Burns <scott.s.burns@vanderbilt.edu>'
__copyright__ = 'Copyright 2012 Vanderbilt University. All Rights Reserved'

import os
from os.path import isdir, join

from .io import Parser


class Subject(object):
    def __init__(self, name):
        self.name = name
        try:
            self.stat_dir = join(os.environ['SUBJECTS_DIR'], name, 'stats')
        except KeyError:
            raise ValueError("SUBJECTS_DIR is not set")
        if not isdir(self.stat_dir):
            raise ValueError(f"This subject doesn't have a 'stats' dir at {self.stat_dir}")

    def get_measures(self):
        measures = []
        for root, d, fnames in os.walk(self.stat_dir):
            for fname in fnames:
                fullname = join(root, fname)
                if Parser.can_parse(fullname):
                    p = Parser(fullname)
                    measures.extend(p.measures)
        self.measures = measures

    def upload_dict(self):
        if not hasattr(self, 'measures'):
            self.get_measures()
        data = {}
        for m in self.measures:
            data[m.name()] = m.value_as_str()
        return data
