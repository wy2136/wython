'''
Extend the xarray.DataArray functionality by using the
 xarray.register_dataarray_accessor.

See:http://xarray.pydata.org/en/stable/internals.html#extending-xarray

Author: Wenchang Yang (yang.wenchang@uci.edu)
'''

import xarray as xr
try:
    from eofs.xarray import Eof
except ImportError:
    print('[Warning]: the eofs package is not installed.')

import geoplots
from geoplots.cartopy.api import cartoplot

from . import util
from . import interpolate # for the regrid method

# see http://xarray.pydata.org/en/stable/internals.html#extending-xarray
@xr.register_dataarray_accessor('geo')
class GeoAccessor(object):
    def __init__(self, da):
        self._obj = da

    def eof(self, *args, **kw):
        '''Perform the EOF analysis using the eofs package.'''
        try:
            return Eof(self._obj, *args, **kw)
        except:
            print('[Warning]: the eofs package is not installed.')
    def fldint(self, *args, **kw):
        '''Field integral. See geoxarray.util.fldint for description.'''
        da = self._obj
        # from . import util
        return util.fldint(da, *args, **kw)

    def fldmean(self, *args, **kw):
        '''See geoxarray.util.fldmean for description.'''
        da = self._obj
        # from . import util
        return util.fldmean(da, *args, **kw)

    def regrid(self, **kw):
        '''see geoxarray.interpolate.regrid for description'''
        return interpolate.regrid(self._obj, **kw)

    def roll_lon(self, *args, **kw):
        '''See geoxarray.util.roll_lon for description.'''
        da = self._obj
        return util.roll_lon(da, *args, **kw)

    def plot(self, *args, **kw):
        """Plot data on a map."""
        dims = self._obj.dims
        if len(dims)>2:
            raise ValueError('data array dimension is higher than 2.')
        try:
            dim_names = [self._obj[name].standard_name.lower()
                for name in list(self._obj.dims)]
        except:
            try:
                dim_names = [self._obj[name].long_name.lower()
                    for name in list(self._obj.dims)]
            except:
                dim_names = ['',]
        if ('lon' in dims or 'longitude' in dims
            or 'longitude' in dim_names)\
            and ('lat' in dims or 'latitude' in dims
            or 'latitude' in dim_names):
            return geoplots.geoplot(self._obj, *args, **kw)
        else:
            return geoplots.fxyplot(self._obj, *args, **kw)
    def geoplot(self, *args, **kw):
        return geoplots.geoplot(self._obj, *args, **kw)
    def fxyplot(self, *args, **kw):
        return geoplots.fxyplot(self._obj, *args, **kw)

    def mapplot(self, *args, **kw):
        """Plot a simple basemap."""
        return geoplots.mapplot(*args, **kw)

    def cartoplot(self, *args, **kws):
        '''Virulize data on basemap from cartopy: see geoplots.cartopy.api.cartoplot'''
        return cartoplot(self._obj, *args, **kws)
