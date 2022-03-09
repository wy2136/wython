#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Mon Feb 21 13:19:58 EST 2022
# perturb IC by adding small "random" numbers to the temperature field of tile1
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
#ifile = 'fv_core.res.tile1.nc'
#ofile = 'tmp.nc'
#perturb_num = 0 # usually given as ensemble member # so that each ensemble member has unique perturbation dependent on this number
ifile, ofile, perturb_num = sys.argv[1:4]
perturb_num = float(perturb_num)

ds = xr.open_dataset(ifile)
ds['T'] += np.sin(ds['T'] + perturb_num) * 1e-10 #temperature field perturbation
if 'checksum' in ds['T'].attrs: #delete the checksum attrs so that no checksum in the fv_io_restart; otherwise, model fails in checksum
    del ds['T'].attrs['checksum']
encoding = {vname:{'_FillValue': None} for vname in list(ds.variables)}
ds.to_netcdf(ofile, encoding=encoding)
print('[saved]:', ofile)
 
 
if __name__ == '__main__':
    from wyconfig import * #my plot settings
    ds0 = xr.open_dataset(ifile)
    ds = xr.open_dataset(ofile)
    da = ds['T'] - ds0['T']
    
    da.isel(Time=0, zaxis_1=0).plot(robust=True)
    
    #savefig
    if len(sys.argv)>1 and 'savefig' in sys.argv[1:]:
        figname = __file__.replace('.py', f'.png')
        if 'overwritefig' in sys.argv[1:]:
            wysavefig(figname, overwritefig=True)
        else:
            wysavefig(figname)
    tt.check(f'**Done**')
    print()
    plt.show()
    
