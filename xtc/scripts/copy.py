#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Mon Aug 19 10:32:34 EDT 2019
import sys, os, os.path, shutil

def copy_file(fname):
    '''copy files under example folder to cwd'''
    cwd = os.getcwd()
    scripts_root = os.path.dirname(os.path.abspath(__file__))
    ifile = os.path.join(scripts_root, fname)
    ofile = os.path.join(cwd, fname)
    if os.path.exists(ofile):
        print('[exists]:', fname)
    else:
        shutil.copyfile(ifile, ofile)
        print('[copied]:', fname, 'from', ifile)

for fname in ['save_tc2netcdf.py', 'params.py']:
    copy_file(fname)
