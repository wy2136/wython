'''author: Wenchang Yang (yang.wenchang@uci.edu)'''


import xarray as xr
from .util import num2time
try:
    from netCDF4 import num2date
except:
    pass

def open_dataset(datafile, **kw):
    '''Variant of xarray.open_dataset and xarray.open_mfdataset'''
    try:
        ds = xr.open_dataset(datafile, **kw)
        return ds
    except ValueError:
        ds = xr.open_dataset(datafile, decode_times=False, **kw)
        tname = [s for s in ['T', 'time', 'Time', 'TIME'] if s in list(ds.dims)][0]
        if hasattr(ds[tname], 'units'):
            tunits = ds[tname].units
            try:
                calendar = ds[tname].calendar
            except:
                calendar = 'standard'
            ds[tname].values = num2time(ds[tname].values, units=tunits,
                calendar=calendar)
            ds[tname].attrs['old units'] = ds[tname].attrs.pop('units')
        print('[decode_times=False]: times is decoded externally.')
        return ds
    except OSError:
        try:
            ds = xr.open_mfdataset(datafile, **kw)
            print('[xarray.open_mfdataset] is used.')
            return ds
        except ValueError:
            ds = xr.open_mfdataset(datafile, decode_times=False, **kw)
            tname = [s for s in ['T', 'time', 'Time', 'TIME'] if s in list(ds.dims)][0]
            if hasattr(ds[tname], 'units'):
                tunits = ds[tname].units
                ds[tname].values = num2time(ds[tname].values, units=tunits)
                ds[tname].attrs['old units'] = ds[tname].attrs.pop('units')
            print('[xarray.open_mfdataset] is used.')
            print('[decode_times]: False')
            return ds
