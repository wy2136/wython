#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Wed Oct 21 11:32:45 EDT 2020
if __name__ == '__main__':
    from misc.timer import Timer
    tt = Timer(f'start {__file__}')
#import sys, os.path, os, glob
#import xarray as xr, numpy as np, pandas as pd
#import matplotlib.pyplot as plt
#more imports
import xarray as xr
from .api import deflate_tracks as _deflate_tracks
from .api import selTS as _selTS
from .api import sel_seed as _sel_seed
from .api import count_tracks as _count_tracks
from .api import track_density as _track_density
from .api import trackplot as _trackplot
#
if __name__ == '__main__':
    tt.check('end import')
#
#start from here
@xr.register_dataset_accessor('tc')
class StormAccessor(object):
    def __init__(self, ds):
        self._obj = ds

    def deflate(self, *args, **kwargs):
        """see xtc.api.deflate_tracks"""
        return _deflate_tracks(self._obj, *args, **kwargs)

    def selTS(self, *args, **kwargs):
        """see xtc.api.selTS"""
        return _selTS(self._obj, *args, **kwargs)

    def sel_seed(self, *args, **kwargs):
        """see xtc.api.sel_seed"""
        return _sel_seed(self._obj, *args, **kwargs)

    def count(self, *args, **kwargs):
        """see xtc.api.count_tracks"""
        return _count_tracks(self._obj, *args, **kwargs)

    def density(self, *args, **kwargs):
        """see xtc.api.track_density"""
        return _track_density(self._obj, *args, **kwargs)

    def trackplot(self, *args, **kwargs):
        """see xtc.api.trackplot"""
        return _trackplot(self._obj, *args, **kwargs)
 
 
if __name__ == '__main__':
    #from wyconfig import * #my plot settings
    tt.check(f'**Done**')
    
