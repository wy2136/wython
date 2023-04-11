#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Fri Sep 30 17:04:36 EDT 2022
# note: used for FLOR/AM.25; for HIRAM, use /tigress/wenchang/MODEL_OUT/FLOR_pkbk.nc; CM2.1/AM2.1 has pk/bk in model output.
if __name__ == '__main__':
    import sys
    from misc.timer import Timer
    tt = Timer('start ' + ' '.join(sys.argv))
import sys, os.path, os, glob, datetime
import xarray as xr, numpy as np, pandas as pd, matplotlib.pyplot as plt
from misc.shell import run_shell
from misc import get_kws_from_argv
#more imports
#
if __name__ == '__main__':
    tt.check('end import')
#
#start from here
idir = '/tigress/wenchang/MODEL_OUT'
model = 'FLOR'
model = get_kws_from_argv('model', model) ###
expname = 'CTL1990_v201905_tigercpu_intelmpi_18_576PE'
expname = get_kws_from_argv('expname', expname) ###
ens = None
ens = get_kws_from_argv('ens', ens) ###
if model != 'FLOR':
    idir = os.path.join(idir, model)
idir = os.path.join(idir, expname)
if ens is not None:
    idir = os.path.join(idir, f'en{ens}')
#ofile = f'{model}.{expname}.pkbk.nc'
ofile = f'pkbk.nc'
if os.path.exists(ofile):
    #run_shell(f'ncdump {ofile}')
    print('[exists]:', ofile)
    sys.exit()
if model == 'HIRAM':
    os.symlink('/tigress/wenchang/MODEL_OUT/FLOR_pkbk.nc', ofile) #use FLOR default pkbk for HIRAM (should work if experiments from HIRAM are not cold started
    print(f'use the pkbk file for {model}: /tigress/wenchang/MODEL_OUT/FLOR_pkbk.nc')
    sys.exit()

#phalf
ifiles = glob.glob(f'{idir}/POSTP/*.atmos_month.nc')
ifiles.sort()
ifile = ifiles[-1]
#ds = xr.open_dataset('/tigress/wenchang/MODEL_OUT/CTL1990_v201905_tigercpu_intelmpi_18_576PE/POSTP/10000101.atmos_month.nc')
print('ifile =', ifile)
ds = xr.open_dataset(ifile)
phalf = ds.phalf

#pk(from ak) and bk
ifiles = glob.glob(f'{idir}/RESTART/*.tar')
ifiles.sort()
ifile = ifiles[-1]
restart_file = ifile
print('restart_file =', restart_file)
#run_shell('tar -xvf /tigress/wenchang/MODEL_OUT/CTL1990_v201905_tigercpu_intelmpi_18_576PE/RESTART/10000101.tar')
if not os.path.exists('wytmp'):
    os.mkdir('wytmp')
    print('[dir created]: wytmp')
run_shell(f'tar -xvf {restart_file} -C ./wytmp/')
ds = xr.open_dataset('./wytmp/fv_core.res.nc')
print('ds =', ds)
pk = ds.ak.squeeze().drop('Time').rename(xaxis_1='phalf').assign_coords(phalf=phalf.values).rename('pk')
pk.attrs = {'units': 'Pa'}
bk = ds.bk.squeeze().drop('Time').rename(xaxis_1='phalf').assign_coords(phalf=phalf.values)
bk.attrs = {'units': '1'}

ds = xr.Dataset(dict(pk=pk, bk=bk))
ds.attrs['note'] = f'{model} {expname}'
encoding = {vv: {'dtype': 'float32', '_FillValue': None} for vv in ['pk', 'bk']}
encoding['phalf'] = {'_FillValue': None}
ds.to_netcdf(ofile, encoding=encoding)
print('[saved]:', ofile)

#run_shell('rm *.res*')
run_shell(f'ncdump {ofile}')

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
