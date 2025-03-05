#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Wed Mar 15 11:58:42 EDT 2023
if __name__ == '__main__':
    import sys,os
    from misc.timer import Timer
    tt = Timer(f'[{os.getcwd()}] start ' + ' '.join(sys.argv))
import sys, os.path, os, glob, datetime
import xarray as xr, numpy as np, pandas as pd, matplotlib.pyplot as plt
#more imports
wython = '/tigress/wenchang/wython'
if wython not in sys.path: sys.path.append(wython); print('added to python path:', wython)
#from misc import get_kws_from_argv
#
if __name__ == '__main__':
    tt.check('end import')
#
#start from here
def bootstrap(da, dim=None, nmc=1000, along_dim=None, seed=None, return_index=False):
    """bootstrap given samples (da) over the given dimension (dim) and MC size (nmc=1000).
        da: input DataArray;
        dim: apply bootstrap to this dim;
        along_dim: apply bootstrap for each element along this dim. e.g. bootstrap over the ens dim at each time point for a (ens, time) shape array
    """
    rng = np.random.default_rng(seed)
    if dim is None:
        dim = da.dims[0] #default is the first dim
    n = da[dim].size
    if along_dim is None:
        indx = xr.DataArray(rng.choice(n, size=(nmc, n)), dims=['mc', dim])
    else:
        n_along = da[along_dim].size
        indx = xr.DataArray(rng.choice(n, size=(nmc, n_along)), dims=['mc', along_dim])

    if return_index:
        return indx
    else:
        return da.isel({dim: indx})
        
        

 
 
if __name__ == '__main__':
    #from wyconfig import * #my plot settings
    if 'test' in sys.argv:
        from misc import get_kws_from_argv
        seed = get_kws_from_argv('seed')
        if seed is not None: seed = int(seed)
        da = xr.DataArray(np.random.randn(3,4), dims=['ens', 'time'])
        print('raw data:')
        print(da)
        print()

        print('index')
        print(bootstrap(da, dim='ens', nmc=2, seed=seed, return_index=True))

        print('bootstrap over dim ens')
        print(bootstrap(da, dim='ens', nmc=2))
        print()

        print('bootstrap over dim ens for every element along dim time')
        print(bootstrap(da, dim='ens', nmc=2, along_dim='time'))
        print()
    
    #savefig
    if 'savefig' in sys.argv or 's' in sys.argv:
        figname = __file__.replace('.py', f'.png')
        if 'overwritefig' in sys.argv or 'o' in sys.argv:
            wysavefig(figname, overwritefig=True)
        else:
            wysavefig(figname)
    tt.check(f'**Done**')
    print()
    if 'notshowfig' in sys.argv or 'n' in sys.argv:
        pass
    else:
        if 'plt' in globals(): plt.show()
    
