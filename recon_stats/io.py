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
        self.structure = structure.lower()
        self.measure = measure.lower()
        self.value = float(value)
        self.units = units.lower()
        self.descrip = descrip
        self.short_name = short_name

    def __repr__(self):
        return "<Measure(%s(%s)[%s]:%0.4f)>" % \
            (self.structure, self.measure, self.units, self.value)

    def name(self):
        return 'recon_%s_%s' % (self.structure, self.measure)

    def label(self):
        return '%s %s(%s)' % (self.structure, self.descrip, self.units)

    def value_as_str(self):
        return str(self.value)


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
            self.raw = list(map(lambda x: x.strip(), f.read().splitlines()))
        self.parser_fxn = self.get_parser()
        self.measures = self.parse()

    def __repr__(self):
        return "<Parser(%s)>" % self.type

    def get_parser(self):
        def _common(raw):
            measure_lines = list(filter(lambda x: x.startswith('# Measure'), raw))
            measures = []
            for ml in measure_lines:
                ml = ml.replace('# Measure', '')
                ml = ml.replace('CortexVol Total cortical gray matter volume', 'CortexVol, Total cortical gray matter volume') # Fix an issue in lh.aparc.stats
                splat = ml.split(',')
                pieces = list(map(lambda x: x.strip(), splat))
                str, meas, descrip, val, units = pieces
                m = Measure(str, meas, val, units, descrip=descrip)
                measures.append(m)
            return measures

        def _get_columns(raw):
            tablecol = list(filter(lambda x: x.startswith('# TableCol'), raw))
            ncols = int(list(filter(lambda x: x.startswith('# NTableCols'), raw))[0].split('# NTableCols')[1])
            columns = []
            for i in range(1, ncols + 1):
                i_table_rows = list(filter(lambda x: ' %d ' % i in x, tablecol))
                tup = (
                        i - 1,
                        list(filter(lambda x: 'ColHeader' in x, i_table_rows))[0].split(' ColHeader ')[-1].strip(),
                        list(filter(lambda x: 'FieldName' in x, i_table_rows))[0].split(' FieldName ')[-1].strip(),
                        list(filter(lambda x: 'Units' in x, i_table_rows))[0].split(' Units ')[-1].strip(),
                    )
                columns.append(tup)
            return columns

        def _grab(columns, col_name, ss_row):
            i, name, field, units = list(filter(lambda x: x[1] == col_name, columns))[0]
            return ss_row[i], field, units

        def _aseg(raw):
            common = _common(raw)
            columns = _get_columns(raw)
            rows = list(filter(lambda x: not x.startswith('#'), raw))
            measures = []
            for row in rows:
                ss_row = row.strip().split()
                measure_cols = ['Volume_mm3', 'normMean', 'normStdDev', 'normMin', 'normMax', 'normRange']
                measures.extend(_parse_row(ss_row, columns, measure_cols))
            return common + measures

        def _parse_row(ss_row, columns, columns_to_measure, hemi=None):
            struct, _, _ = _grab(columns, 'StructName', ss_row)
            struct = struct.replace('-', '_')
            measures = []
            for col in columns_to_measure:
                value, descrip, units = _grab(columns, col, ss_row)
                m = Measure(struct, col, value, units, descrip=descrip)
                if hemi:
                    m.structure = '%s_%s' % (hemi, m.structure)
                    # m.descrip = '%s %s' % (hemi, m.descrip)
                measures.append(m)
            return measures

        def _hemi(raw):
            return list(filter(lambda x: x.startswith('# hemi'), raw))[0].split('hemi')[1].strip()

        def _aparc(raw):
            common = _common(raw)
            # update these measures with hemisphere
            hemi = _hemi(raw)
            for meas in common:
                meas.structure = hemi + meas.structure
            rows = list(filter(lambda x: not x.startswith('#'), raw))
            columns = _get_columns(raw)
            measures = []
            for row in rows:
                ss_row = row.strip().split()
                measure_cols = ['NumVert', 'SurfArea', 'GrayVol', 'ThickAvg',
                    'ThickStd', 'MeanCurv', 'GausCurv', 'FoldInd', 'CurvInd']
                measures.extend(_parse_row(ss_row, columns, measure_cols, hemi=hemi))
            return common + measures

        def _a2009s(raw):
            # Don't need to do common
            hemi = _hemi(raw)
            rows = list(filter(lambda x: not x.startswith('#'), raw))
            columns = _get_columns(raw)
            measures = []
            for row in rows:
                ss_row = row.strip().split()
                measure_cols = ['NumVert', 'SurfArea', 'GrayVol', 'ThickAvg',
                    'ThickStd', 'MeanCurv', 'GausCurv', 'FoldInd', 'CurvInd']
                measures.extend(_parse_row(ss_row, columns, measure_cols, hemi=hemi))
            return measures

        key_parsers = {
            'aseg.stats': _aseg,
            'lh.aparc.stats': _aparc,
            'rh.aparc.stats': _aparc,
            'lh.aparc.a2009s.stats': _a2009s,
            'rh.aparc.a2009s.stats': _a2009s,
            'wmparc.stats': _aseg,
        }
        return key_parsers[self.type]

    def parse(self):
        return self.parser_fxn(self.raw)
