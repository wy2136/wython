#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Tue Aug 13 10:56:50 EDT 2019

import xarray as xr, numpy as np, pandas as pd
from scipy.stats import pearsonr as _corr_func

def pearsonr(da1, da2, dim=None):
    '''xarray-wrapped function of scipy.stats.pearsonr'''
    if dim is None:
        dim = [d for d in da1.dims if d in da2.dims][0]

    r, p = xr.apply_ufunc(_corr_func, da1, da2,
        input_core_dims=[[dim], [dim]],
        output_core_dims=[[], []],
        vectorize=True,
        dask='allowed')

    r.attrs['long_name'] = 'Pearson correlation coefficient'
    p.attrs['long_name'] = 'p-value'

    return xr.Dataset(dict(r=r, p=p))
