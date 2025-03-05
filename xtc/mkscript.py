#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Mon Aug 19 10:32:34 EDT 2019
import sys, os, os.path, shutil

def copy_file(fname):
    cwd = os.getcwd()
    xtc_root = os.path.dirname(os.path.abspath(__file__))
    ifile = os.path.join(xtc_root, 'example', fname)
    ofile = os.path.join(cwd, fname)
    if os.path.exists(ofile):
        print('[exists]:', fname)
    else:
        shutil.copyfile(ifile, ofile)
        print('[copied]:', fname, 'from', ifile)

fname = 'save_tc2netcdf.py'
copy_file(fname)

fname ='params.py'
copy_file(fname)
