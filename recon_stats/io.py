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
    def __init__(self, structure, measure, value, units, descrip=None,
            short_name=None):
        self.structure = structure
        self.measure = measure
        self.value = float(value)
        self.units = units
        self.descrip = descrip
        self.short_name = short_name

    def __repr__(self):
        return "<Measure(%s(%s)[%s]:%0.4f)>" % \
            (self.structure, self.measure, self.units, self.value)


class Parser(object):

    parseable = ('aseg.stats',
                 'lh.aparc.a2009s.stats',
                 'lh.aparc.stats',
                 'rh.aparc.a2009s.stats',
                 'rh.aparc.stats',
                 'wmparc.stats')

    @classmethod
    def can_parse(cls, fname):
        return basename(fname) in cls.parseable

    def __init__(self, fname):
        self.type = basename(fname)
        with open(fname) as f:
            self.raw = map(lambda x: x.strip(), f.read().splitlines())
        self.parser_fxn = self.get_parser()
        self.measures = self.parse()

    def __repr__(self):
        return "<Parser(%s)>" % self.type

    def get_parser(self):
        def _common(raw):
            measure_lines = filter(lambda x: x.startswith('# Measure'), raw)
            measures = []
            for ml in measure_lines:
                splat = ml.replace('# Measure', '').split(',')
                pieces = map(lambda x: x.strip(), splat)
                str, meas, descrip, val, units = pieces
                m = Measure(str, meas, val, units, descrip=descrip)
                measures.append(m)
            return measures

        def _inner_aseg(raw):
            common = _common(raw)
            return common

        def _inner_aparc(raw):
            common = _common(raw)
            return common

        def _inner_wmparc(raw):
            common = _common(raw)
            return common

        key_parsers = {
            'aseg.stats': _inner_aseg,
            'lh.aparc.stats': _inner_aparc,
            'rh.aparc.stats': _inner_aparc,
            'lh.aparc.a2009s.stats': _inner_aparc,
            'rh.aparc.a2009s.stats': _inner_aparc,
            'wmparc.stats': _inner_wmparc,
        }
        return key_parsers[self.type]

    def parse(self):
        return self.parser_fxn(self.raw)
