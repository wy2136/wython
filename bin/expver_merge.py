#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Sun Oct 16 15:30:11 EDT 2022
if __name__ == '__main__':
    import sys
    from misc.timer import Timer
    tt = Timer('start ' + ' '.join(sys.argv))
import sys, os.path, os, glob, datetime
import xarray as xr, numpy as np, pandas as pd, matplotlib.pyplot as plt
#more imports
#
if __name__ == '__main__':
    tt.check('end import')
#
#start from here
#ifile = 'era5.total_precipitation.2022-08.nc.raw'
#ifile = 'era5.2m_temperature_max.2022-12.nc.raw'
ifile = sys.argv[1]
if not ifile.endswith('.nc.raw'):
    print('input file must end with .nc.raw')
    sys.exit()
ofile = ifile.replace('.nc.raw', '.nc')
if os.path.exists(ofile) and 'o' not in sys.argv:
    print('[exists]:', ofile)
    sys.exit()
da = xr.open_dataarray(ifile)
da1 = da.sel(expver=1) #ERA5
da5 = da.sel(expver=5) #ERA5T near realtime

da_merge = da1.where(da1*0==0, other=da5) #take the non-NaN values from both ERA5 and ERA5T
ds = da_merge.to_dataset()
ds.to_netcdf(ofile)
print('[saved]:', ofile)
 
 
if __name__ == '__main__':
    #from wyconfig import * #my plot settings
    
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
    
