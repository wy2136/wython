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
#
if __name__ == '__main__':
    tt.check('end import')
#
#start from here
def correlation_yx(day, dax, **kws):
    """given xr.DataArray day(1D) and dax(1D), calculate the correlation 
    along the common dim using pyleoclim.Series.correlation"""
    returnx = kws.pop('returnx', True)

    assert day.ndim==1 and dax.ndim==1, 'both input arrays must be 1D'
    assert day.dims[0] == dax.dims[0], 'both input arrays must share a common dim'
    dim = dax.dims[0]

    #create pyleoclim.Series for day and dax
    y = pyleo.Series(time=day[dim].values, value=day.values)
    x = pyleo.Series(time=dax[dim].values, value=dax.values)

    #do the calculation
    result = y.correlation(x, **kws)
    if not returnx: #return pyleoclim.core.ui.CorrEns instead of xr.Dataset
        return result

    #convert results to xr.DataArray
    #correlation r
    r = xr.DataArray(result.r)
    #pvalue p
    p = xr.DataArray(result.p)
    #bool signif
    signif = xr.DataArray(result.signif)
    
    #create xr.Dataset to save the result
    ds = xr.Dataset(dict(r=r, p=p, signif=signif))

    return ds
 
if __name__ == '__main__':
    from wyconfig import * #my plot settings
    from xdata import ds
    ds_ = ds.isel(time=slice(11,None,12)).groupby('time.year').mean('time')
    day = ds_.iod
    dax = ds_.nino34
    print('correlation of Dec IOD and NINO3.4:\n')
    rr = correlation_yx(day, dax, returnx=False, seed=0)
    print(rr)

    rr = correlation_yx(day, dax, returnx=True, seed=0)
    print(rr)


    
    #savefig
    if 'savefig' in sys.argv:
        figname = __file__.replace('.py', f'.png')
        wysavefig(figname)
    tt.check(f'**Done**')
    plt.show()
    
