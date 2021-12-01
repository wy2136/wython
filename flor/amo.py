#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Thu Oct 25 17:22:50 EDT 2018
import os.path
import xarray as xr

cwd, this_file = os.path.split(__file__)

## test
#da = xr.open_dataarray('data/CTL1860.atmos_month.t_surf.nc')
#dimx, dimy = 'grid_xt', 'grid_yt'
#if True:

def cal_amo_index(da, dimx='grid_xt', dimy='grid_yt'):
    '''calculate AMO index from surface temperature (t_surf)'''
    new_dims = {dimx: 'lon', dimy: 'lat'}
    NA = dict(lon=slice(360-80, 360), lat=slice(0, 60)) # North Atlantic

    ncfile = os.path.join(cwd, 'data', 'CTL1860.00010101.atmos_month.land_mask.nc')
    land_frac = xr.open_dataset(ncfile).land_mask.rename(new_dims) # land fraction 0(water)-1(land)

    # rename dims of lon and lat
    if dimx != 'lon' or dimy != 'lat':
        da = da.rename(new_dims)

    # select ocean grids
    da = da.where(land_frac<0.5) 

    # calculate the index
    ts = da.sel(lon=NA['lon'], lat=NA['lat']).geo.fldmean()

    # remove climatology
    ts = ts.groupby('time.month') - ts.groupby('time.month').mean('time')
   
    return ts
