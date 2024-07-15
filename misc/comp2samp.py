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
def comp2samp(da1, da2, dim=None, confidence=0.95, same_var=False):
    """compare the means of two samples and calculate the difference, p-value and uncertainty(error).
    For equal variance assumption: https://sphweb.bumc.bu.edu/otlt/mph-modules/bs/bs704_confidence_intervals/bs704_confidence_intervals5.html
    For unequal variance assumption (by default): https://en.wikipedia.org/wiki/Student%27s_t-test.

    return ds:
        ds = xr.Dataset(dict(
            x1m=x1m, x2m=x2m, s1=s1, s2=s2, n1=n1, n2=n2, dof=dof, pvalue=pvalue, x1m_minus_x2m=x1m_minus_x2m, err=err
            ))
    """
    #same_var = False
    #dim = 'time'
    #confidence = 0.95
    #np.random.seed(2022)
    #da1 = xr.DataArray(np.random.randn(50, 2)*2 +1, dims=[dim, 'lat'])
    #da2 = xr.DataArray(np.random.randn(100, 2)*2 +1, dims=[dim, 'lat'])
    if dim is None:
        dims_in_common = [d for d in da1.dims if d in da2.dims]
        assert len(dims_in_common)>0, 'input da1 and da2 must have dims in common'
        dim = dims_in_common[0]

    #sample sizes
    n1 = da1[dim].size
    n2 = da2[dim].size
    #sample means
    with xr.set_options(keep_attrs=True):
        x1m = da1.mean(dim)
        x2m = da2.mean(dim)
        #difference of the two means
        x1m_minus_x2m = x1m - x2m
    #sample variances
    s1 = da1.std(dim)
    s2 = da2.std(dim)
    s1s1 = s1*s1
    s2s2 = s2*s2
    if same_var: #https://sphweb.bumc.bu.edu/otlt/mph-modules/bs/bs704_confidence_intervals/bs704_confidence_intervals5.html
        #std of the pooled samples 
        s_p = np.sqrt( ( (n1-1)*s1s1 + (n2-1)*s2s2 )/(n1+n2-2) )
        #std of the difference of the two means
        s = s_p*np.sqrt( 1/n1 + 1/n2 )
        dof = n1 + n2 - 2
    else: #https://en.wikipedia.org/wiki/Student%27s_t-test
        #std of the difference of the two means
        s = np.sqrt( s1s1/n1 + s2s2/n2 )
        #degree of freedom
        dof = (s1s1/n1 + s2s2/n2)**2 \
            / ( (s1s1/n1)**2/(n1-1) + (s2s2/n2)**2/(n2-1) )
    #tvalue
    tvalue = x1m_minus_x2m/s
    #pvalue
    pvalue = ( 1 - _t_cdf( np.abs(tvalue), df=dof ) ) * 2
    #tvalue for the given confidence interval level
    t_c = _t_ppf(0.5+confidence/2, df=dof) #t value for given confidence interval level (e.g., 0.95 by default)
    #error 
    err = t_c * s
    if 'units' in da1.attrs:
        err.attrs['units'] = da1.attrs['units']

    #wrap to an Dataset
    ds = xr.Dataset(dict(
        x1m=x1m, x2m=x2m, s1=s1, s2=s2, n1=n1, n2=n2, dof=dof, pvalue=pvalue, x1m_minus_x2m=x1m_minus_x2m, err=err
        ))
    #print(ds)
    return ds

 
 
if __name__ == '__main__':
    #from wyconfig import * #my plot settings
    if 'test' in sys.argv:
        dim = 'time'
        np.random.seed(2022)
        da1 = xr.DataArray(np.random.randn(50, 2)*2 +1, dims=[dim, 'lat'])
        da2 = xr.DataArray(np.random.randn(100, 2)*2 +1, dims=[dim, 'lat'])
        ds = comp2samp(da1, da2, dim=dim, same_var=True)
        print('equal variance assumption')
        print(ds)
        ds = comp2samp(da1, da2, dim=dim, same_var=False)
        print('unequal variance assumption')
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
    
