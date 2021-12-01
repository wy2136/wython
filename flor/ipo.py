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

def cal_ipo_index(da, dimx='grid_xt', dimy='grid_yt'):
    '''calculate IPO index from surface temperature (t_surf)'''
    new_dims = {dimx: 'lon', dimy: 'lat'}
    CP = dict(lon=slice(170, 360-90), lat=slice(-10, 10)) # central tropical Pacific
    NP = dict(lon=slice(140, 360-145), lat=slice(25, 45)) # north Pacific
    SP = dict(lon=slice(150, 360-160), lat=slice(-50,-15)) # south Pacific

    ncfile = os.path.join(cwd, 'data', 'CTL1860.00010101.atmos_month.land_mask.nc')
    land_frac = xr.open_dataset(ncfile).land_mask.rename(new_dims) # land fraction 0(water)-1(land)

    # rename dims of lon and lat
    if dimx != 'lon' or dimy != 'lat':
        da = da.rename(new_dims)
    
    da = da.where(land_frac<0.5) # select ocean grids 

    # calculate the index
    ts = ( da.sel(lon=CP['lon'], lat=CP['lat']).geo.fldmean()
        - da.sel(lon=NP['lon'], lat=NP['lat']).geo.fldmean()/2
        - da.sel(lon=SP['lon'], lat=SP['lat']).geo.fldmean()/2
        )

    # remove climatology
    ts = ts.groupby('time.month') - ts.groupby('time.month').mean('time')
   
    return ts
