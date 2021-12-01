#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Wed Jun 16 13:04:17 EDT 2021
if __name__ == '__main__':
    from misc.timer import Timer
    tt = Timer(f'start {__file__}')
import sys, os.path, os, glob, datetime
import xarray as xr, numpy as np, pandas as pd, matplotlib.pyplot as plt
#more imports
import geoxarray
#
if __name__ == '__main__':
    tt.check('end import')
#
#start from here
idir = os.path.dirname(__file__)
ifile = os.path.join(idir, 'ersst5_1979-2018.nc')
ds = xr.open_dataset(ifile)
da = ds.sst
func_anom = lambda x: x.groupby('time.month') - x.sel(time=slice('1981', '2010')).groupby('time.month').mean('time')

#nino3.4 index
nino34 = da.sel(lat=slice(-5, 5), lon=slice(360-170, 360-120)).geo.fldmean() \
    .pipe(func_anom) \
    .assign_attrs(units='K', long_name='Nino3.4 index')
ds['nino34'] = nino34

#indian ocean dipole mode index
func_west = lambda x: x.sel(lat=slice(-10,10), lon=slice(50,70)).geo.fldmean()
func_east = lambda x: x.sel(lat=slice(-10,0), lon=slice(90,110)).geo.fldmean()
west_minus_east = lambda x: func_west(x) - func_east(x)
iod = da.pipe(west_minus_east).pipe(func_anom).assign_attrs(units='K', long_name='Indian Ocean Diple Mode Index')
ds['iod'] = iod
    
if __name__ == '__main__':
    #from wyconfig import * #my plot settings
    
    #savefig
    if 'savefig' in sys.argv:
        figname = __file__.replace('.py', f'.png')
        wysavefig(figname)
    tt.check(f'**Done**')
    plt.show()
    
