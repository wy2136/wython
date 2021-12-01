#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Sun Aug 18 20:29:15 EDT 2019
from matplotlib import path
import xarray as xr, numpy as np
from cftime import DatetimeNoLeap

from .basins import tc_basins

def tc_count(ds, basin=None, ws=None):
    '''count monthly TC # in a given basin.
    **input**:
        basin: can be one of 'NA', 'EP', 'WP', 'NI', 'SI', 'AU', 'SP', 'SA'. If basin is None, count the global TC #.
        ws: max wind speed threshold. Default is None (no max wind speed threshold is applied).
    **return**:
        n_tc
    '''
    if basin is None:
        basin = 'global'
    
    if ws is not None:
        ds = ds.where(ds.windmax.max('stage')>ws)

    #  da_month
    # keep only the first point for each track (stage=0)
    da_month = ds.month.isel(stage=0, drop=True)

    if basin != 'global': # for a specific basin instead of global
        # basin domain
        basins = tc_basins()
        iregion = basins.map_keys(basin)
        basin_domain = path.Path(basins.coords[iregion])

        # TC genesis locations as pair of lon/lat points
        ds_genesis = ds.isel(stage=0, drop=True)
        saved_shape = ds_genesis.lon.shape
        lon = ds_genesis.lon.data.ravel()
        lon[lon<0] = lon[lon<0]+360 # make sure lon is within [0,360]
        lat = ds_genesis.lat.data.ravel()
        points = np.array([lon, lat]).transpose()
        # find points with the basin domain
        in_the_basin = basin_domain.contains_points(points).reshape(saved_shape)
        # mask only values within the basin
        da_month = da_month.where(in_the_basin)

    # use vectorize-version of numpy.histogram to count TC # for each month
    n_tc, _bins = xr.apply_ufunc(np.histogram, da_month,
                                input_core_dims=[['storm']],
                                output_core_dims=[['mon'], ['edge']],
                                vectorize=True,
                                kwargs={'bins': np.arange(0.5, 12.6, 1)}
                               )
    n_tc['mon'] = np.arange(1, 13)

    # flatten dims ('year', 'mon') to ('time',)
    n_tc = n_tc.stack(time=('year', 'mon'))
    n_tc['time'] = [DatetimeNoLeap(yyyy, mm, 1)
                        for yyyy,mm in zip(n_tc.year.data, n_tc.mon.data)]

    n_tc.attrs['long_name'] = f'{basin} monthly TC #'
    n_tc = n_tc.rename('N_TC')

    return n_tc
