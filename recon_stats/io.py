#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" io.py

Low-level io
"""
__author__ = 'Scott Burns <scott.s.burns@vanderbilt.edu>'
__copyright__ = 'Copyright 2012 Vanderbilt University. All Rights Reserved'

from os.path import basename


class Measure(object):
    """Basic class for storing statistical measures"""
    def __init__(self, structure, measure, value, units, short_name=None):
        self.measure = measure
        self.value = value
        self.units = units
        if short_name:
            self.short_name = short_name

    def __repr__(self):
        return "<Measure(%s[%s]:%0.4f)>" % \
            (self.measure, self.units, self.value)


class Parser(object):

    parseable = ('aseg.stats',
                 'lh.aparc.a2009s.stats',
                 'lh.aparc.stats',
                 'rh.aparc.a2009s.stats',
                 'rh.aparc.stats',)

    @classmethod
    def can_parse(cls, fname):
        return basename(fname) in cls.parseable

    def __init__(self, fname):
        self.type = basename(fname)
        with open(fname) as f:
            raw = f.read().splitlines()
            self.raw = map(lambda x: x.strip(), raw)

        self.parser_fxn = self.get_parser()
        self.measures = self.parse()

    def get_parser(self):
        def _common(raw):
            print "Running common ops"
            return []

        def _inner_aseg(raw):
            common = _common(raw)
            print "Running aseg ops"
            return common.extend([])

        def _inner_aparc(raw):
            common = _common(raw)
            print "Running aparc ops"
            return common.extend([])

        key_parsers = {
            'aseg.stats': _inner_aseg,
            'lh.aparc.stats': _inner_aparc,
            'lh.aparc.stats': _inner_aparc,
            'lh.aparc.a2009s.stats': _inner_aparc,
            'rh.aparc.a2009s.stats': _inner_aparc,
        }
        return key_parsers[self.type]

    def parse(self):
        return self.parser_fxn(self.raw)
