#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Thu Aug  8 11:18:09 EDT 2019

import xarray as xr
from .linregress_scipy import linregress as _linregress_scipy
from .linregress_numba import linregress as _linregress_numba



@xr.register_dataarray_accessor('linregress')
class LinearRegressAccessor(object):
    def __init__(self, da):
        self._obj = da
    
    #to be compatible with old version
    def on(self, *args, **kwargs):
        '''if numba_on is True (default):
            see see xlinregress.linregress_numba.linregress
        else:
            see xlinregress.linregress_scipy.linregress or xaddon.api.linregress'''
        numba_on = kwargs.pop('numba_on', True)
        if numba_on:
            return _linregress_numba(self._obj, *args, **kwargs)
        else:
            return _linregress_scipy(self._obj, *args, **kwargs)

    def scipy(self, *args, **kwargs):
        '''see xlinregress.linregress_scipy.linregress'''
        return _linregress_scipy(self._obj, *args, **kwargs)
        
    def numba(self, *args, **kwargs):
        '''see xlinregress.linregress_numba.linregress'''
        return _linregress_numba(self._obj, *args, **kwargs)

    def fast(self, *args, **kwargs):
        '''see xlinregress.linregress_numba.linregress'''
        return _linregress_numba(self._obj, *args, **kwargs)

    def wy(self, *args, **kwargs):
        '''see xlinregress.linregress_numba.linregress'''
        return _linregress_numba(self._obj, *args, **kwargs)
