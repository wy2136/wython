#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Tue Mar 17 14:27:11 EDT 2020
import sys, os.path, os, datetime
import xarray as xr, numpy as np, pandas as pd
#import matplotlib.pyplot as plt
#more imports
#
if __name__ == '__main__':
    print()
    today = datetime.date.today()
    today_s = today.strftime('%Y-%m-%d')
    tformat = '%Y-%m-%dT%H:%M:%S'
    t_start = datetime.datetime.now()
    print('[start]:', t_start.strftime(tformat))
    
# land mask data
_this_dir, _this_basename = os.path.split(__file__)
_ifile = os.path.join(_this_dir, 'data', 'FLOR.land_mask.nc')
land_mask = xr.open_dataset(_ifile)['land_mask']

#start from here
def get_landflag(ds):
    '''Get land flag (land fraction of the cell grid near given lon/lat).
    Input:
    ------
    ds: TC tracking dataset(inside includes lon and lat)
        e.g. ds = xr.open_dataset('/tigress/wenchang/data/ibtracs/v04r00/analysis/ibtracs.tracks.1980-2018.nc')

    Return:
    -------
    land_flag: xr.DataArray with same dims as ds.lon/ds.lat.
    '''
    this_dir, this_basename = os.path.split(__file__)
    ifile = os.path.join(this_dir, 'data', 'FLOR.land_mask.nc')
    land_mask = xr.open_dataset(ifile)['land_mask']
    landflag = land_mask.sel(lon=ds.lon.pipe(np.remainder, 360),
        lat=ds.lat, method='nearest', drop=True) + ds.lon*0 # add ds.lon*0 makes sure nan input gives nan output

    return landflag

if __name__ == '__main__':
    ds = xr.open_dataset('/tigress/wenchang/data/ibtracs/v04r00/analysis/ibtracs.tracks.1980-2018.nc')
    landflag = get_landflag(ds)
    t_end = datetime.datetime.now()
    print('[end]:', t_end.strftime(tformat))
    print('[total time used]:', f'{(t_end - t_start).seconds:,} seconds')
    print()
