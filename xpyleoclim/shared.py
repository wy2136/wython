#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Wed Dec  1 13:38:20 EST 2021
if __name__ == '__main__':
    from misc.timer import Timer
    tt = Timer(f'start {__file__}')
#import sys, os.path, os, glob, datetime
import xarray as xr, numpy as np, pandas as pd, matplotlib.pyplot as plt
#more imports
import pyleoclim as pyleo
#
if __name__ == '__main__':
    tt.check('end import')
#
#start from here
def da2series(da):
    """convert xr.DataArray to pyleoclim.Series"""
    assert da.ndim == 1, 'input array must be 1D'
    dim = da.dims[0]
    try:
        ts = pyleo.Series(time=da[dim].values, value=da.values)
    except TypeError:
        ts = pyleo.Series(time=range(da.size), value=da.values)
    return ts

 
 
if __name__ == '__main__':
    #from wyconfig import * #my plot settings
    
    #savefig
    if 'savefig' in sys.argv:
        figname = __file__.replace('.py', f'.png')
        wysavefig(figname)
    tt.check(f'**Done**')
    plt.show()
    
