#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Sun Aug 18 20:29:15 EDT 2019
import xarray as xr, numpy as np, pandas as pd
import cftime 

from .basins import tracks_in_basin

def tc_ace(ds, basin=None):
    '''Monthly ACE over a given basin.
    **input**:
        ds: tracks dataset.
        basin: basin str from 'NA', 'EP', 'WP', 'NI', 'SI', 'AU', 'SP', 'SA'.
    **return**:
        ace: ace DataArray'''
    if basin is None or basin == 'global':
        basin = 'global'
        windmax = ds.windmax
    else:
        inBasin = tracks_in_basin(ds, basin)
        windmax = ds.windmax.where(inBasin)
    months = range(1, 13)
    das = []
    for m in months: # group by month
        da = windmax.where(ds.month.isel(stage=0)==m) \
            .pipe(lambda x: x*x) \
            .sum(['storm', 'stage'])
        das.append(da)
    da = xr.concat(das, dim=pd.Index(months, name='mon'))

    # convert dimensions ('year', 'mon') to ('time',)
    da = da.stack(time=('year', 'mon'))
    da['time'] = [cftime.DatetimeProlepticGregorian(year, mon, 1) 
                  for year,mon in zip(da.year.data, da.mon.data)]
    da.attrs['long_name'] = f'{basin} accumulated cyclone energy'
    da.attrs['units'] = 'm**2 s**-2'

    return da
    
def _histogram2d_weighted(lat, lon, windmax, bins, range):
    '''A variant of numpy.histogram when input is lat/lon, which has ndim of 1 or 2, and weighted by windmax**2'''
    H, _dump1, _dump2 =  np.histogram2d(lat.ravel(),
                                        lon.ravel(),
                                        weights=windmax.ravel()**2,
                                        bins=bins, range=range)
    return H

def tc_ace_density(ds, lowpass_on=False):
    '''Use numpy.histogram2d to estimate TC ACE density.

    Input: ds, TC information Dataset.
    Return: TC ACE density DataArray.'''

    # lat/lon bins, centers and ranges
    lat_bins = np.arange(-90, 91, 1)
    lon_bins = np.arange(0, 361, 1)
    lat_centers = lat_bins[0:-1] + 0.5
    lon_centers = lon_bins[0:-1] + 0.5
    lat_range = (lat_bins[0], lat_bins[-1])
    lon_range = (lon_bins[0], lon_bins[-1])

    # extract data from ds
    input_core_dims = [['storm', 'stage'], ['storm', 'stage'], ['storm', 'stage']]
    monvec = np.arange(1, 13)
    das = []
    for mon in monvec:
        da = xr.apply_ufunc(_histogram2d_weighted,
                            ds.lat.where(ds.month==mon),
                            ds.lon.where(ds.month==mon),
                            ds.windmax.where(ds.month==mon),
                            input_core_dims=input_core_dims,
                            output_core_dims=[['lat', 'lon']],
                            vectorize=True,
                            kwargs={'bins': [lat_bins, lon_bins],
                                    'range': [lat_range, lon_range]
                                    }
                            )
        # da has a dims of ('year', 'lat', 'lon') or ('en', 'year', 'lat', 'lon')
        da['lat'] = lat_centers
        da['lon'] = lon_centers
        das.append(da)
    da = xr.concat(das, dim=pd.Index(monvec, name='mon'))
    da = da.stack(time=('year', 'mon'))
    da['time'] = [cftime.DatetimeProlepticGregorian(yyyy, mm, 1)
        for yyyy,mm in zip(da.year.data, da.mon.data)] # da now has dims: ('lat', 'lon', 'time') or ('en', 'lat', 'lon', 'time')
    da = da.stack(z=('lat', 'lon')).unstack() # da now has dims: ('time', 'lat', 'lon') or ('en', 'time', 'lat', 'on')
    da.attrs['units'] = 'm**2 s**-2 * 6hrs per month per 1x1deg box'
    da.attrs['long_name'] = 'accumulated cyclone energy'

    # count in a larger lat/lon box (10 deg by 10 deg)
    if lowpass_on:
        W = 10 # rolling window size
        R = W//2 # half of the window size, or the radius
        da = xr.concat([da.isel(lon=slice(-R, None)), da, da.isel(lon=slice(0, R))], dim='lon') \
            .rolling(lon=W, center=True).sum().isel(lon=slice(R, -R)) \
            .rolling(lat=W, center=True).sum() \
            .assign_coords(lat=lat_bins[0:-1], lon=lon_bins[0:-1]) \
            .isel(lat=slice(1, None))
        da = da.pipe(lambda x: x/4).assign_attrs({'units': 'm**2 s**-2 * 6hrs per month per 10x10deg box'})

    return da

