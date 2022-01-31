#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Sat Jan  9 00:10:17 EST 2021
if __name__ == '__main__':
    from misc.timer import Timer
    tt = Timer(f'start {__file__}')
import sys, os.path, os, glob
import xarray as xr, numpy as np, pandas as pd
#import matplotlib.pyplot as plt
#more imports
import geoxarray
from geoplots import mapplot
#
if __name__ == '__main__':
    tt.check('end import')
#
#start from here
if len(sys.argv) < 2:
    daname = 't_surf'
else:
    daname = sys.argv[1]
cwd = os.getcwd()
print('cwd:', cwd)
ifiles = os.path.join(cwd, 'work/POSTP/*.atmos_month.nc')
if not glob.glob(ifiles):
    ifiles = os.path.join(cwd, 'POSTP/*.atmos_month.nc')
if not glob.glob(ifiles):
    ifiles = os.path.join(cwd, '*.atmos_month.nc')
print('ifiles:', ifiles)
da = xr.open_mfdataset(ifiles)[daname]
units = da.attrs['units']
print(f'{daname}[{units}] loading ...')
da.load() 
 
if __name__ == '__main__':
    from wyconfig import * #my plot settings
    #figname = __file__.replace('.py', f'_{tt.today()}.png')
    plt.figure()
    long_name = f'global mean {daname}'
    da_ = da.groupby('time.year').mean('time').geo.fldmean()
    da_.assign_attrs(long_name=long_name, units=units).plot(marker='o', fillstyle='none')
    year = da_.year[-1].item() # last year
    plt.axvline(year, color='gray', ls='--')

    plt.figure()
    da_ = da.isel(time=slice(-12, None)).mean('time').assign_attrs(units=units).plot.contourf(levels=20)
    mapplot(coastlines_color='gray')
    plt.title(f'year = {year:04d}')
    
    #plt.savefig(figname)
    #print('[saved]:', figname)
    tt.check(f'**Done**')
    plt.show()
    
