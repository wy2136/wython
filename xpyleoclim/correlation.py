#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Tue Nov 30 17:17:02 EST 2021
if __name__ == '__main__':
    from misc.timer import Timer
    tt = Timer(f'start {__file__}')
import sys, os.path, os, glob, datetime
import xarray as xr, numpy as np, pandas as pd, matplotlib.pyplot as plt
#more imports
from .correlation_yx import correlation_yx
from .correlation_yyx import correlation_yyx
from .correlation_yyxx import correlation_yyxx
#
if __name__ == '__main__':
    tt.check('end import')
#
#start from here
def correlation(da1, da2, **kws):
    """given xr.DataArray da1(1D or >1D) and da2(1D or >1D), calculate the correlation 
    along the common dim using pyleoclim.Series.correlation or pyleoclim.MultipleSeries.correlation.
    
    For possbile kws, see:
    https://pyleoclim-util.readthedocs.io/en/latest/core/ui.html#pyleoclim.core.ui.MultipleSeries.correlation
    """

    if da1.ndim==1 and da2.ndim==1: #both input arrays are 1D
        return correlation_yx(da1, da2, **kws)
    elif da1.ndim>1 and da2.ndim>1: #both input arrays are >1D
        return correlation_yyxx(da1, da2, **kws)
    else: #one is 1D and the other is >1D
        if da2.ndim>da1.ndim:
            da1,da2 = da2,da1 #swap to ensure da1 is >1D
        return correlation_yyx(da1, da2, **kws)
        
if __name__ == '__main__':
    from wyconfig import * #my plot settings
    from xdata import ds
    ds_ = ds.isel(time=slice(11,None,12)).groupby('time.year').mean('time')
    
    #test correlation_yx
    print('\n##correlation of Dec IOD and NINO3.4:\n')
    da1 = ds_.iod
    da2 = ds_.nino34
    rr = correlation(da1, da2, returnx=False, seed=0)
    print('result in pylceoclim format')
    print(rr)
    rr = correlation(da1, da2, returnx=True, seed=0)
    print('result in xarray format')
    print(rr)

    #test correlation_yyx
    da1 = ds_.sst.sel(lat=slice(-2,2)).sel(lon=slice(180,360))
    da2 = ds_.nino34
    print('\n##correlation of Dec Nino3.4 and tropical SST:\n')
    print('signif')
    rr = correlation(da1, da2, seed=0)
    rr.r.plot()
    rr.signif.where(rr.signif==1).plot.contourf(colors='none', hatches=['///'], add_colorbar=False)
    #change the order of args and expect the same result
    print('signif_fdr and swap input arrays')
    plt.figure()
    rr = correlation(da2, da1, seed=0)
    rr.r.plot()
    rr.signif_fdr.where(rr.signif_fdr==1).plot.contourf(colors='none', hatches=['///'], add_colorbar=False)

    #test correlation_yyxx
    print('\n##>1D array against >1D array')
    da1 = ds_.sel(lat=0, drop=True).sst.isel(lon=slice(0,2)).rename(lon='lon1')
    da2 = ds_.sel(lat=0, drop=True).sst.isel(lon=slice(0,4)).rename(lon='lon2')
    rr = correlation(da1, da2)
    plt.figure()
    rr.r.plot()
    rr.signif.where(rr.signif==1).plot.contourf(colors='none', hatches=['///'], add_colorbar=False)

    #savefig
    if 'savefig' in sys.argv:
        figname = __file__.replace('.py', f'.png')
        wysavefig(figname)
    tt.check(f'**Done**')
    plt.show()
    
