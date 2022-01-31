#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Tue Jan 21 16:06:55 EST 2020
import sys, os.path, os, datetime
#import xarray as xr, numpy as np, pandas as pd
#import matplotlib.pyplot as plt
print()
def fix_link(ilink):
    #istr = '/scratch/gpfs/wenchang'
    #ostr = '/home/wenchang/scratch'
    istr = '/scratch/gpfs'
    ostr = '/home/wenchang/tgScratch'
    #ilink = 'work_e1'
    if os.path.islink(ilink):
        ireal = os.readlink(ilink)
        if ireal.startswith(istr):
            print('[old]:', ilink, '->', ireal)
            ireal = ireal.replace(istr, ostr)
            os.remove(ilink)
            os.symlink(ireal, ilink)
            print('[new]:', ilink, '->', ireal)
            print()

 
if __name__ == '__main__':
    #t0 = datetime.datetime.now()
    #print('[start]:', t0.strftime(tformat))

    for ilink in sys.argv[1:]:
        fix_link(ilink)
    

