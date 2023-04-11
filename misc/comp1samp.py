#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Fri Nov 18 12:28:25 EST 2022
if __name__ == '__main__':
    import sys
    from misc.timer import Timer
    tt = Timer('start ' + ' '.join(sys.argv))
import sys, os.path, os, glob, datetime
import xarray as xr, numpy as np, pandas as pd, matplotlib.pyplot as plt
#more imports
from scipy import stats
#
if __name__ == '__main__':
    tt.check('end import')
#
#start from here
def _t_cdf(x, df):
    """xarray version of scipy.stats.t.cdf"""
    return xr.apply_ufunc(stats.t.cdf, x, df)
def _t_ppf(x, df):
    """xarray version of scipy.stats.t.ppf"""
    return xr.apply_ufunc(stats.t.ppf, x, df)
def comp1samp(da, dim=None, confidence=0.95, same_var=False):
    """compare the mean of the input sample and 0 and calculate the difference, p-value and uncertainty(error).
    see: https://sphweb.bumc.bu.edu/otlt/mph-modules/bs/bs704_confidence_intervals/BS704_Confidence_Intervals3.html
    see: https://en.wikipedia.org/wiki/Student%27s_t-test
    """
    #same_var = False
    #dim = 'time'
    #confidence = 0.95
    #np.random.seed(2022)
    #da = xr.DataArray(np.random.randn(50, 2)*1 + 0, dims=[dim, 'lat'])
    if dim is None:
        dim = da.dims[0]

    #sample sizes
    n = da[dim].size
    #sample means
    with xr.set_options(keep_attrs=True):
        xm = da.mean(dim)
    #std of the sample
    sx = da.std(dim)
    #std of the mean
    s = sx/np.sqrt(n)
    #degree of freedom
    dof = n - 1
    #tvalue
    tvalue = xm/s
    #pvalue
    pvalue = ( 1 - _t_cdf( np.abs(tvalue), df=dof ) ) * 2
    #tvalue for the given confidence interval level
    t_c = _t_ppf(0.5+confidence/2, df=dof) #t value for given confidence interval level (e.g., 0.95 by default)
    #error 
    err = t_c * s
    if 'units' in da.attrs:
        err.attrs['units'] = da.attrs['units']

    #wrap to an Dataset
    ds = xr.Dataset(dict(
        xm=xm, sx=sx, n=n, dof=dof, pvalue=pvalue, err=err
        ))
    #print(ds)
    return ds

 
 
if __name__ == '__main__':
    #from wyconfig import * #my plot settings
    if 'test' in sys.argv:
        dim = 'time'
        np.random.seed(2022)
        da = xr.DataArray(np.random.randn(50, 2)*2, dims=[dim, 'lat'])
        ds = comp1samp(da, dim=dim)
        print(ds)
    
    #savefig
    if 'savefig' in sys.argv or 's' in sys.argv:
        figname = __file__.replace('.py', f'.png')
        if 'overwritefig' in sys.argv or 'o' in sys.argv:
            wysavefig(figname, overwritefig=True)
        else:
            wysavefig(figname)
    tt.check(f'**Done**')
    print()
    if 'notshowfig' in sys.argv:
        pass
    else:
        plt.show()
    
