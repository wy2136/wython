#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Tue Aug 13 10:50:49 EDT 2019

import xarray as xr

from .api import pearsonr as _pearsonr

@xr.register_dataarray_accessor('cc')
class CorrelationAccessor(object):
    def __init__(self, da):
        self._obj = da
    
    def pearsonr(self, *args, **kwargs):
        '''see xcorrelation.api.pearsonr'''
        return _pearsonr(self._obj, *args, **kwargs)

