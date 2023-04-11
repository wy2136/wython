'''author: Wenchang Yang (yang.wenchang@uci.edu)'''

import datetime
import numpy as np
from numpy import pi, ma
import xarray as xr
from xarray.ufuncs import cos
import pandas as pd
from netCDF4 import num2date

from .nputil import cal_grid_area

def num2time(num,units, calendar='standard'):
    '''Convert expression of time from "months since yyyy-mm-dd" into pandas DatetimeIndex.'''
    if units.lower().startswith('months since'):
        # get the yyyy-mm (or yyyy-m) string from units
        yyyy_mm = '-'.join( units.split()[2].split('-')[:2] )
        period0 = pd.Period(yyyy_mm)
        return pd.PeriodIndex(period0 + np.floor(num).astype('int'))\
            .to_timestamp()
    else:
        # daily data with non-standard calendar
        time = num2date(num, units, calendar=calendar)
        try:
            time = [datetime.datetime(*t.timetuple()[:3]) for t in time]
            print('[{} calendar]:'.format(calendar),
                'time = [datetime.datetime(*t.timetule()[:3]) for t in time]')
        except:
            pass
        return time


def fldmean(da, lon_name=None, lat_name=None):
    '''Compute field mean weighed by cos(lat).
    Parameters:
        da: xarray.DataArray
        lon_name: name of longitude, e.g. 'lon'
        lat_name: name of latitude, e.g. 'lat'
    Return:
        xarray.DataArray'''
    attrs_saved = da.attrs
    # default lon_name and lat_name
    dims = da.dims
    if lon_name is None:
        lon_name = [x for x in ('lon', 'longitude', 'Longitude', 'X', 'grid_xt')
                    if x in dims][0]
    if lat_name is None:
        lat_name = [y for y in ('lat', 'latitude', 'Latitude', 'Y', 'grid_yt')
                    if y in dims][0]

    # # default msk
    # dims_none_field = [dim for dim in dims if dim not in (lon_name, lat_name)]
    # kw = {k:0 for k in dims_none_field}
    # if msk is None:
    #     msk = da.isel(**kw).copy()
    # msk *= 0

    # weight: cos(lat*pi/180)
    wt = (da[lon_name]==da[lon_name]).astype('float') * cos(da[lat_name]*pi/180.)
    # wt += msk # consider mask
    # wt /= wt.sum() # normalize the weight

    # field mean
    da_mean = (wt * da).sum([lon_name, lat_name])
    da_mean /= (wt + da*0).sum([lon_name, lat_name])
    da_mean = da_mean.assign_attrs(attrs_saved)

    return da_mean

def fldint(da, lon_name=None, lat_name=None, r=6.371e6, normalized=False):
    '''Compute field integral.
    Parameters:
        da: xarray.DataArray
        lon_name: name of longitude, e.g. 'lon'
        lat_name: name of latitude, e.g. 'lat'
        normalized: bool, calculate the fldmean if True
    Return:
        xarray.DataArray'''
    # default lon_name and lat_name
    dims = da.dims
    if lon_name is None:
        lon_name = [x for x in ('lon', 'longitude', 'Longitude', 'X', 'grid_xt')
                    if x in dims][0]
    if lat_name is None:
        lat_name = [y for y in ('lat', 'latitude', 'Latitude', 'Y', 'grid_yt')
                    if y in dims][0]


    # grid area (dsigma): r**2 * cos(lat*pi/180) * (dlon*pi/180) * (dlat*pi/180)
    dsigma = da[lat_name] + da[lon_name]
    dsigma.values = cal_grid_area(da[lon_name].values,
        da[lat_name].values, r=r)

    # field integral
    da_int = (dsigma * da).sum([lon_name, lat_name])

    # calculate the fldmean
    if normalized:
        da_int /= (dsigma + da*0).sum([lon_name, lat_name])

    return da_int

def roll_lon(da, lon_name=None):
    '''Toggle the longitude between 180-centered and 0-centered.
    Longitude range must be either [0, 360) or [-180, 180).'''
    da = da.copy()
    if lon_name is None:
        lon_name = [s for s in ('lon', 'longitude', 'Longitude', 'X')
            if s in da.dims][0]
    lon = da[lon_name].data
    if np.any(lon>180) and not np.any(lon<0):
        lon[lon>=180] -= 360
        da[lon_name] = lon
    elif np.any(lon<0) and not np.any(lon>180):
        lon[lon<0] += 360
        da[lon_name] = lon
    else:
        raise ValueError('Longitude must be either 0~360 or -180~180.')
    kw = {lon_name: int(lon.size/2)}
    da_roll = da.roll(**kw)

    return da_roll
