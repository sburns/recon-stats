#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
recon
~~~~~

A tiny module to parse recon-all logs
"""

__author__ = 'Scott Burns <scott.s.burns@gmail.com>'
__license__ = 'BSD 3-Clause'

import os
from datetime import datetime


def parse_status_file(sf):
    """ Pass in the path to a $SUBJECTS_DIR/$SUB/scripts/recon-all-status.log
    file and this returns a list recon-all step, time (s) tuples
    """
    with open(sf) as f:
        raw = f.read().splitlines()

    step_dt = [(' '.join(l.split()[1:-6]), datetime.strptime(' '.join(l.split()[-6:]), "%a %b %d %H:%M:%S %Z %Y")) for l in raw if l.startswith('#@#')]

    step_times = []
    for i, sd in enumerate(step_dt):
        if not i:
            continue
        step, dt = sd
        diff = dt - step_dt[i-1][1]
        step_times.append((step, diff.total_seconds()))
    return step_times

if __name__ == '__main__':

    f = '/scratch/burnsss1/freesurfer-subjects/cpu_214_206441/scripts/recon-all-status.log'
    step_times = parse_status_file(f)
