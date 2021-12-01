#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Tue Oct 20 23:35:29 EDT 2020
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
def storm_deflate(ds):
    """
    deflate NaNs along the 'storm' dimension given the input storm tracks dataset
    """
    n_max = ds.lat.isel(stage=0).count('storm').max().item() # max # of storms per year, the length of the new storm dimension
    #print(n_max)
    ds_deflate = ds.isel(storm=slice(0, n_max)).astype('float32') + np.nan # initialize the deflated dataset
    if 'en' in ds.dims: # ds has 'en' dimension
        for en in ds.en.values:
            for year in ds.year.values:
                #print(f'en = {en:2d}; year = {year:4d}')
                L = ds.lat.sel(en=en, year=year).isel(stage=0, drop=True).notnull() # logic indexes of none nan
                #print(L)
                n_storms = L.sum().item() # number of storms in the year
                for data_name in list(ds.data_vars):
                    #print(data_name)
                    da = ds[data_name].sel(en=en, year=year).isel(storm=L.values) # deflate nans along the storm dimension
                    ds_deflate[data_name].loc[dict(en=en, year=year, storm=slice(1, n_storms))] = da.values
    else:
        for year in ds.year.values:
            #print(f'en = {en:2d}; year = {year:4d}')
            L = ds.lat.sel(year=year).isel(stage=0, drop=True).notnull() # logic indexes of none nan
            #print(L)
            n_storms = L.sum().item() # number of storms in the year
            for data_name in list(ds.data_vars):
                #print(data_name)
                da = ds[data_name].sel(year=year).isel(storm=L.values) # deflate nans along the storm dimension
                ds_deflate[data_name].loc[dict(year=year, storm=slice(1, n_storms))] = da.values
    
    return ds_deflate
 
 
if __name__ == '__main__':
    from wyconfig import * #my plot settings
    from xtc import tc_count
    from xtc.filter import storm_filter
    if 'ds_deflate' not in globals():
        ifile = '/tigress/wenchang/analysis/TC/HIRAM/amipHadISST_tigercpu_intelmpi_18_540PE/netcdf/HIRAM.amipHadISST_tigercpu_intelmpi_18_540PE.tc_tracks.allstorms.1971-2018.nc'
        ds = xr.open_dataset(ifile)
        ds = storm_filter(ds)
        ds_deflate = storm_deflate(ds)
        ntc = tc_count(ds)
        ntc_ = tc_count(ds_deflate)
    ntc.mean('en').groupby('time.year').sum('time').plot(label='raw')
    ntc_.mean('en').groupby('time.year').sum('time').plot(label='deflated', ls='--')
    plt.legend()
    
    tt.check(f'**Done**')
    plt.show()
    
