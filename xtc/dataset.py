#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Fri May 22 16:52:24 EDT 2020
if __name__ == '__main__':
    from misc.timer import Timer
    tt = Timer(f'start {__file__}')
import sys, os.path, os, glob
import xarray as xr, numpy as np, pandas as pd
#import matplotlib.pyplot as plt
#more imports
#
if __name__ == '__main__':
    tt.check('end import')
#
#start from here
def load(dsname='IBTrACS'):
    '''load TC tracks dataset by its name. Default is IBTrACS.'''
    if dsname.lower() == 'ibtracs':
        ifile = '/tigress/wenchang/data/ibtracs/v04r00/analysis/v2/IBTrACS.ALL.v04r00.tracksByYear.1980-2021.nc'

    return xr.open_dataset(ifile)
 
 
if __name__ == '__main__':
    #from wyconfig import * #my plot settings
    tt.check(f'**Done**')
    
