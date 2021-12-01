#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Tue Nov 30 17:17:02 EST 2021
if __name__ == '__main__':
    from misc.timer import Timer
    tt = Timer(f'start {__file__}')
import sys, os.path, os, glob, datetime
import xarray as xr, numpy as np, pandas as pd, matplotlib.pyplot as plt
#more imports
import pyleoclim as pyleo
from tqdm import tqdm
from .correlation_yyx import correlation_yyx
#
if __name__ == '__main__':
    tt.check('end import')
#
#start from here
def correlation_yyxx(dayy, daxx, **kws):
    """given xr.DataArray dayy(>1D,usually 2D) and daxx(>1D, usually 2D), calculate the correlation 
    along the common dim using pyleoclim.MultipleSeries.correlation"""
    mute_pbar = kws.pop('mute_pbar', True)#mute the progress bar of inner loops by default

    #get dims info (common dim and other dims)
    dims_common = [d for d in dayy.dims if d in daxx.dims] #common dims
    assert len(dims_common) == 1, 'more than 1 common dims are found'
    dim = dims_common[0]
    dims_other_xx = list(daxx.dims)
    dims_other_xx.remove(dim) #dims in daxx that are not the common dim

    #stack dims_other of daxx
    daxx_stack = daxx.stack(sxx=dims_other_xx)

    #loop correlation calculation
    dss = []
    for ii in tqdm(range(daxx_stack.sxx.size)):
        _ds = correlation_yyx(dayy, daxx_stack.isel(sxx=ii, drop=True), mute_pbar=mute_pbar, **kws) 
        dss.append(_ds)
    ds = xr.concat(dss, dim='sxx').assign_coords(sxx=daxx_stack.sxx).unstack()
    
    return ds

 
 
if __name__ == '__main__':
    from wyconfig import * #my plot settings
    from xdata import ds
    ds_ = ds.isel(time=slice(11,None,12)).groupby('time.year').mean('time').sel(lat=0, drop=True)
    dayy = ds_.sst.isel(lon=slice(0,2)).rename(lon='lonyy')
    daxx = ds_.sst.isel(lon=slice(0,4)).rename(lon='lonxx')
    rr = correlation_yyxx(dayy, daxx)
    rr.r.plot()
    rr.signif.where(rr.signif==1).plot.contourf(colors='none', hatches=['///'], add_colorbar=False)

    plt.figure()
    rr.r.plot()
    rr.signif_fdr.where(rr.signif_fdr==1).plot.contourf(colors='none', hatches=['///'], add_colorbar=False)

    
    #savefig
    if 'savefig' in sys.argv:
        figname = __file__.replace('.py', f'.png')
        wysavefig(figname)
    tt.check(f'**Done**')
    plt.show()
    
