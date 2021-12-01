#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Fri Oct 16 15:16:50 EDT 2020
if __name__ == '__main__':
    from misc.timer import Timer
    tt = Timer(f'start {__file__}')
import sys, os.path, os, glob
import xarray as xr, numpy as np, pandas as pd
#import matplotlib.pyplot as plt
#more imports
from .mask import get_landflag
#
if __name__ == '__main__':
    tt.check('end import')
#
#start from here
def sel_seed(ds, oceanHour=12, latMax=30): 
    '''given allstorms tracks dataset ds, and storm filter parameters oceanHour and latMax,
    return the filtered dataset of TC seeds. 
    **input**:
        ds: tracks dataset
        oceanHour(=12): total life hours over ocean grids
        latMax(=30): latitude boundary for the initial track point
    **return**:
        ds_seed
    '''
    #lat range condition
    if latMax is None:
        latMax = 90.1
    L1 = np.abs(ds.lat.isel(stage=0).drop('stage')) < latMax # first appearance point within {latMax}S-{latMax}N

    # ocean hour condition
    L2 = get_landflag(ds).pipe(lambda x: x<0.5).sum('stage') > oceanHour//6

    L = L1&L2

    return ds.where(L)
 
 
if __name__ == '__main__':
    from wyconfig import * #my plot settings
    # now we filter the tracks by ourselves from the allstorms file
    ifile = '/tigress/wenchang/analysis/TC/HIRAM/CTL1990s_v201910_tigercpu_intelmpi_18_540PE/netcdf/HIRAM.CTL1990s_v201910_tigercpu_intelmpi_18_540PE.tc_tracks.allstorms.0101-0150.nc' 
    ds = xr.open_dataset(ifile)


    tt.check(f'**Done**')
    #plt.show()
