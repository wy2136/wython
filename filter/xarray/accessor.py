'''
Filter accessor for xarray.

Author: Wenchang Yang (wenchang@princeton.edu)
'''

import xarray as xr
from . import butter

@xr.register_dataarray_accessor('filter_old')
class FilterAccessor(object):
    def __init__(self, da):
        self._obj = da

    def lowpass(self, *args, **kw):
        '''See filter.xarray.butter.lowpass for description.'''
        return butter.lowpass(self._obj, *args, **kw)

    def highpass(self, *args, **kw):
        '''See filter.xarray.butter.highpass for description.'''
        return butter.highpass(self._obj, *args, **kw)

    def bandpass(self, *args, **kw):
        '''See filter.xarray.butter.bandpass for description.'''
        return butter.bandpass(self._obj, *args, **kw)
