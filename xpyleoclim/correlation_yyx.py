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
from .shared import da2series
#
if __name__ == '__main__':
    tt.check('end import')
#
#start from here
def correlation_yyx(dayy, dax, **kws):
    """given xr.DataArray dayy(>1D) and dax(1D), calculate the correlation 
    along the common dim using pyleoclim.MultipleSeries.correlation"""
    returnx = kws.pop('returnx', True)

    dim = dax.dims[0]
    dims_other = list(dayy.dims)
    dims_other.remove(dim) #dims in dayy that is the common dim

    #stack dims_other of dayy
    dayy_stack = dayy.stack(s=dims_other)
    #select along the stack dim where all values along the common dim are valid (not NaN)
    isValid = np.logical_not( np.isnan(dayy_stack).any(dim) )
    dayy_valid = dayy_stack.isel(s=isValid)
    
    #create pyleoclim.Series for dax and pyleoclim.MultipleSeries for dayy
    x = da2series(dax)#x = pyleo.Series(time=dax[dim].values, value=dax.values)
    ts_list = []
    for ii in range(dayy_valid.s.size):
        ts = da2series(dayy_valid.isel(s=ii))#ts = pyleo.Series(time=dayy_valid[dim].values, value=dayy_valid.isel(s=ii).values)
        ts_list.append(ts)
    yy = pyleo.MultipleSeries(ts_list)

    #do the calculation
    result = yy.correlation(x, **kws)
    if not returnx: #return pyleoclim.core.ui.CorrEns instead of xr.Dataset
        return result

    #convert results to xr.DataArray
    #correlation r
    zz = isValid*0 + np.nan # initialize
    zz[isValid.values] = result.r
    r = xr.DataArray(zz, dims='s', coords=[isValid.s]).unstack()
    r.attrs['long_name'] = 'correlation coefficient'
    #pvalue p
    zz = isValid*0 + np.nan # initialize
    zz[isValid.values] = result.p
    p = xr.DataArray(zz, dims='s', coords=[isValid.s]).unstack()
    p.attrs['long_name'] = 'p-value'
    #bool signif
    zz = isValid*0 + np.nan # initialize
    zz[isValid.values] = result.signif
    signif = xr.DataArray(zz, dims='s', coords=[isValid.s]).unstack()
    #bool signif_fdr
    zz = isValid*0 + np.nan # initialize
    zz[isValid.values] = result.signif_fdr
    signif_fdr = xr.DataArray(zz, dims='s', coords=[isValid.s]).unstack()
    
    #create xr.Dataset to save the result
    ds = xr.Dataset(dict(r=r, p=p, signif=signif, signif_fdr=signif_fdr))

    return ds

 
 
if __name__ == '__main__':
    from wyconfig import * #my plot settings
    from xdata import ds
    ds_ = ds.isel(time=slice(11,None,12)).groupby('time.year').mean('time')
    dayy = ds_.sst.sel(lat=slice(-10,10))
    dax = ds_.nino34
    print('\ncorrelation of Nino3.4 and tropical SST:\n')
    rr = correlation_yyx(dayy, dax, seed=0) 
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
    
