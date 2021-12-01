#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Mon Mar 29 13:12:34 EDT 2021
if __name__ == '__main__':
    from misc.timer import Timer
    tt = Timer(f'start {__file__}')
import sys, os.path, os, glob, datetime
#import xarray as xr, numpy as np, pandas as pd
#import matplotlib.pyplot as plt
#more imports
#
if __name__ == '__main__':
    tt.check('end import')
#
#start from here
def archive(ifile):
    """archive the input file by appending date information to the file name, e.g. test.txt -> test.txt.2021-03-29"""
    mtime = os.path.getmtime(ifile)
    mtime_s = datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d') # string format mtime
    ifile_archive = ifile + '.' + mtime_s
    #archive by renaming
    os.rename(ifile, ifile_archive)
    print('[archived]:', ifile, '->', ifile_archive)

    return ifile_archive

if __name__ == '__main__':
    #from wyconfig import * #my plot settings
    ifile = sys.argv[1]
    archive(ifile)
    tt.check(f'**Done**')
    
