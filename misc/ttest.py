#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Wed Sep 14 14:52:17 EDT 2022
if __name__ == '__main__':
    import sys
    from misc.timer import Timer
    tt = Timer('start ' + ' '.join(sys.argv))
import sys, os.path, os, glob, datetime
import xarray as xr, numpy as np, pandas as pd, matplotlib.pyplot as plt
#more imports
from scipy.stats import ttest_ind as _ttest_ind
#
if __name__ == '__main__':
    tt.check('end import')
#
#start from here
def ttest_ind(da1, da0, dim=None, **kws):
    """xarray wrapper of the scipy.stats.ttest_ind"""
    if dim is None:
        dim = [d for d in da1.dims if d in da0.dims][0]
    daa = da1.mean(dim) - da0.mean(dim)

    dim1 = f'{dim}1'
    da1 = da1.rename({dim: dim1})
    dim0 = f'{dim}0'
    da0 = da0.rename({dim: dim0})
    kws['axis'] = -1
    tvalue,pvalue = xr.apply_ufunc(_ttest_ind, da1, da0,
        input_core_dims=[[dim1], [dim0]],
        output_core_dims=[[],[]],
        kwargs=kws
        )
    return daa, pvalue


 
 
if __name__ == '__main__':
    #from wyconfig import * #my plot settings
    if 'test' in sys.argv:
        from scipy.stats import norm
        zz1 = norm.rvs(size=(30,2,2))
        zz0 = norm.rvs(size=(30,2,2))
        da1 = xr.DataArray(zz1, dims=('time', 'lat', 'lon'))
        da0 = xr.DataArray(zz0, dims=('time', 'lat', 'lon'))

        #test
        print('results from scipy:')
        zza = zz1.mean(axis=0) - zz0.mean(axis=0) 
        print(f'{zza = :}')
        t,p = _ttest_ind(da1, da0, axis=0)
        print(f'{p = }')
        t,p = _ttest_ind(da1, da0, axis=0, alternative='less')
        print(f'alternative=less: {p = }')

        print()
        print('results from wython:')
        daa, p = ttest_ind(da1, da0)
        print(f'{daa = }')
        print(f'{p = }')
        daa, p = ttest_ind(da1, da0, alternative='less')
        print(f'alternative=less: {p = }')
    
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
    
