#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Tue Jun 30 17:23:41 EDT 2020
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
land = regionmask.defined_regions.natural_earth.land_110
def flagland(da):
    """Given input DataArray with lon/lat info, return landflag DataArray (1 over land and 0 over ocean)"""
    #rename grid names from GFDL GCMs
    if 'grid_xt' in da.dims:
        da = da.rename(grid_xt='lon')
    if 'grid_yt' in da.dims:
        da = da.rename(grid_yt='lat')
    lmask = land.mask(da)
    landflag = (lmask + 1).fillna(0)
    return landflag

def whereland(da):
    """keep values over land and leave NaNs over ocean"""
    #rename grid names from GFDL GCMs
    if 'grid_xt' in da.dims:
        da = da.rename(grid_xt='lon')
    if 'grid_yt' in da.dims:
        da = da.rename(grid_yt='lat')
    return da.where(flagland(da)>0.5)
def whereocean(da):
    #rename grid names from GFDL GCMs
    if 'grid_xt' in da.dims:
        da = da.rename(grid_xt='lon')
    if 'grid_yt' in da.dims:
        da = da.rename(grid_yt='lat')
    """keep values over ocean and leave NaNs over land"""
    return da.where(flagland(da)<0.5)
 
 
if __name__ == '__main__':
    from wyconfig import * #my plot settings
    lon = np.arange(0, 360)
    lat = np.arange(-89, 90)
    da = xr.DataArray(np.zeros((lat.size, lon.size)), dims=['lat', 'lon'], coords=[lat, lon])
    landflag = flagland(da)

    plt.figure()
    landflag.plot()
    plt.title('land flag (1 over land; 0 over ocean)')
    
    plt.figure()
    da.where(landflag>0.5).plot()
    plt.title('land only (ocean mask)')

    plt.figure()
    da.where(landflag<0.5).plot()
    plt.title('ocean only (land mask)')

    tt.check(f'**Done**')
    plt.show()
    
