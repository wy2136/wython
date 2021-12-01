#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Sat Feb 13 12:35:18 EST 2021
if __name__ == '__main__':
    from misc.timer import Timer
    tt = Timer(f'start {__file__}')
import sys, os.path, os, glob, datetime
import xarray as xr, numpy as np, pandas as pd
#import matplotlib.pyplot as plt
#more imports
#
if __name__ == '__main__':
    tt.check('end import')
#
#start from here
def nc2csv(ifile, transpose=False):
    #ifile = 'chirps.precip.daily.China.subregion.2009-2014.nc'
    print('[ifile]:', ifile)
    da = xr.open_dataarray(ifile).load()
    if 'units' in da.attrs:
        units = da.attrs['units'].replace('/', '_per_')
        ofile = ifile.replace('.nc', f'.{units}.csv')
    else:
        ofile = ifile.replace('.nc', f'.csv')
    if os.path.exists(ofile):
        print('[exists]:', ofile)
        return 
    if transpose:
        da = da.transpose()
    da.to_pandas().to_csv(ofile)
    print('[saved]:', ofile)

if __name__ == '__main__':
    #from wyconfig import * #my plot settings
    ifile = sys.argv[1]
    if 'transpose' in sys.argv:
        transpose = True
    else:
        transpose = False

    nc2csv(ifile, transpose)

    
    figname = __file__.replace('.py', f'_{tt.today()}.png')
    if len(sys.argv) > 1 and 'savefig' in sys.argv:
        plt.savefig(figname)
        print('[saved]:', figname)
    tt.check(f'**Done**')
    #plt.show()
    
