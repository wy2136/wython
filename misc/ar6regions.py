#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Tue Jun 30 17:23:41 EDT 2020
# README: https://regionmask.readthedocs.io/en/stable/defined_scientific.html#ar6-regions
if __name__ == '__main__':
    from misc.timer import Timer
    tt = Timer(f'start {__file__}')
#import sys, os.path, os, glob
import xarray as xr, numpy as np, pandas as pd
#import matplotlib.pyplot as plt
#more imports
import regionmask
#
if __name__ == '__main__':
    tt.check('end import')
#
#start from here
ar6 = regionmask.defined_regions.ar6.all
def flagar6(da):
    """Given input DataArray with lon/lat info, return region flags of AR6 DataArray.
    AR6 regions: https://regionmask.readthedocs.io/en/stable/_images/plotting_ar6_all.png."""
    return ar6.mask(da)
 
 
if __name__ == '__main__':
    from wyconfig import * #my plot settings
    lon = np.arange(0, 360)
    lat = np.arange(-89, 90)
    da = xr.DataArray(np.zeros((lat.size, lon.size)), dims=['lat', 'lon'], coords=[lat, lon])
    grids = flagar6(da)
    grids.plot()
    tt.check(f'**Done**')
    plt.show()
    
