#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Fri May 17 23:11:08 EDT 2019
import xarray as xr, numpy as np, pandas as pd
from cftime import DatetimeNoLeap
from itertools import product

def _histogram2d(lat, lon, bins, range):
    '''A variant of numpy.histogram when input is lat/lon, which has ndim of 1 or 2'''
    H, _dump1, _dump2 =  np.histogram2d(lat.ravel(),
                                        lon.ravel(),
                                        bins=bins, range=range)
    return H

def tc_density(ds, lowpass_on=True, genesis_on=False, W=10, genesis_condition=None, tcdays_on=True):
    '''Use numpy.histogram2d to estimate TC density or TC genesis density.

    Input 
    ------
        ds, TC information Dataset.
        lowpass_on: default is True.
        genesis_on: default is False.
        W: rolling window size in lowpass, default is 10.
        genesis_condition: e.g. (ds.windmax>17)&(ds.tm>0)
    
    Return
    ------
        TC density DataArray.'''
    # ds = tc_get('CTL1860_noleap_tigercpu_intelmpi_18_576PE', range(11,21))
    # lowpass_on = False
    # genesis_on = True

    # lat/lon bins, centers and ranges
    lat_bins = np.arange(-90, 91, 1)
    lon_bins = np.arange(0, 361, 1)
    lat_centers = lat_bins[0:-1] + 0.5
    lon_centers = lon_bins[0:-1] + 0.5
    lat_range = (lat_bins[0], lat_bins[-1])
    lon_range = (lon_bins[0], lon_bins[-1])

    # extract data from ds
    if genesis_on:
        if genesis_condition is None:
            ds = ds.isel(stage=0, drop=True)
        else:
            ds = ds.isel(stage=genesis_condition.argmax('stage')).drop('stage')
        input_core_dims = [['storm'], ['storm']]
    else:
        input_core_dims = [['storm', 'stage'], ['storm', 'stage']]
    monvec = np.arange(1, 13)
    das = []
    for mon in monvec:
        da = xr.apply_ufunc(_histogram2d,
                            ds.lat.where(ds.month==mon),
                            ds.lon.where(ds.month==mon),
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
    da['time'] = [DatetimeNoLeap(yyyy, mm, 1)
        for yyyy,mm in zip(da.year.data, da.mon.data)] # da now has dims: ('lat', 'lon', 'time') or ('en', 'lat', 'lon', 'time')
    da = da.stack(z=('lat', 'lon')).unstack() # da now has dims: ('time', 'lat', 'lon') or ('en', 'time', 'lat', 'on')
    da.attrs['units'] = '# per month per 1x1deg box'
    if genesis_on:
        da.attrs['long_name'] = 'TC genesis density'
    else:
        da.attrs['long_name'] = 'TC density'

    # count in a larger lat/lon box (10 deg by 10 deg)
    if lowpass_on:
        #W = 10 # rolling window size
        R = W//2 # half of the window size, or the radius
        da = xr.concat([da.isel(lon=slice(-R, None)), da, da.isel(lon=slice(0, R))], dim='lon') \
            .rolling(lon=W, center=True).sum().isel(lon=slice(R, -R)) \
            .rolling(lat=W, center=True).sum()
        if W%2 == 0: #W is an even number
            da = da.assign_coords(lat=lat_bins[0:-1], lon=lon_bins[0:-1]) \
                .isel(lat=slice(1, None))
        if genesis_on:
            da.attrs['units'] = f'# per month per {W}x{W}deg box'
        else:
            if tcdays_on:
                # convert units of 6 or 3 hours to days
                dt = ds.stage.isel(stage=1).item() - ds.stage.isel(stage=0).item() #time interval for each track (6 hours by default; 3 hours for IBTrACS)
                da = da.pipe(lambda x: x*dt/24).assign_attrs({'units': f'TC days per month per {W}x{W}deg box'})
            else:
                da.attrs['units'] = f'# per month per {W}x{W}deg box'

    return da
