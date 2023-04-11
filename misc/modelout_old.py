#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Thu Apr 28 12:26:29 EDT 2022
if __name__ == '__main__':
    import sys
    from misc.timer import Timer
    tt = Timer('start ' + ' '.join(sys.argv))
import sys, os.path, os, glob, datetime
import xarray as xr, numpy as np, pandas as pd, matplotlib.pyplot as plt
#more imports
import geoxarray
#
if __name__ == '__main__':
    tt.check('end import')
#
#start from here
def get_modelout_files(model, expname, dsname='atmos_month', years=None, ens=None):
    """get list of model output files given daname, model, expname, and optionally, dsname, years, ens. """
    #daname = 'netrad_toa'
    #dsname = 'atmos_month'
    #model = 'AM2.5'
    #expname = 'CTL1990s_tigercpu_intelmpi_18_540PE'
    if ens is None:
        idir = os.path.join('/tigress/wenchang/MODEL_OUT', model, expname, 'POSTP')
    else:
        idir = os.path.join('/tigress/wenchang/MODEL_OUT', model, expname, f'en{ens:02d}', 'POSTP')
    if model in ('FLOR',):
        idir = idir.replace(f'{model}/', '')
    if not os.path.exists(idir): #data not in modelout dir; maybe in work dir
        idir = idir.replace('/tigress/wenchang/MODEL_OUT', '/home/wenchang/scratch') \
            .replace(f'{expname}', f'work/{expname}')
        if model in ('FLOR',):
            idir = idir.replace('home/wenchang/scratch', 'home/wenchang/scratch/FLOR')
        if ens is not None:
            idir = idir.replace(f'en{ens:02d}/', '') \
                .replace('_tigercpu_', f'_e{ens}_tigercpu_')
        if not os.path.exists(idir): #data not in work dir either
            idir = idir.replace('home/wenchang/scratch','home/wenchang/sGEOCLIM/wenchang')
            if not os.path.exists(idir): #data not in GEOCLIM scratch either
                return
    #get the year range based on all files under the POSTP dir
    if years is None:
        ncfiles = [ncfile for ncfile in os.listdir(idir) if not ncfile.startswith('.') and ncfile.endswith('.nc')]
        ncfiles.sort()
        year0, year1 = int(ncfiles[0][:4]), int(ncfiles[-1][:4])
        years = range(year0, year1+1)
    ifiles = [os.path.join(idir, f'{year:04d}0101.{dsname}.nc') for year in years]

    return ifiles, years

def _get_modelout_data(daname, model, expname, func=None, funcname='wy', ofile=None, loop_files=True, verbose=True, precheck=False, savedata=True, **kws):
    """get model data given daname, func_process and parameters from get_modelout_files."""
    #default func
    if func is None:
        func = lambda x: x
    #default loop_files
    if loop_files is None:
        if model in ('AM2.5C360',):
            loop_files = True
        else:
            loop_files = False
    #ifiles
    ifiles, years = get_modelout_files(model, expname, **kws)
    if verbose:
        print('ifiles:')
        #for ifile in ifiles:
        #    print(ifile)
        print(f'{ifiles[0]}\n  to\n{ifiles[-1]}')
        #print(f'{years = }')
        print('years =', years)
    if precheck:
        return

    #ofile
    if ofile is None:
        ofile = f'{daname}_{model}_{expname}_{years[0]:04d}-{years[-1]:04d}_{funcname}.nc'
    if os.path.exists(ofile):
        da = xr.open_dataarray(ofile)
        print('[loaded]:', ofile)
        return da

    #processing data
    if loop_files:
        das = []
        nfiles = len(ifiles)
        for ii,ifile in enumerate(ifiles, start=1):
            print(f'[{ii:03d} of {nfiles:03d}]: {ifile}', daname, funcname)
            da = xr.open_dataset(ifile)[daname]
            attrs = da.attrs
            da = da.pipe(func)
            das.append(da)
        print('concatenating over time...')
        da = xr.concat(das, dim='time')
    else:
        print('loading...')
        da = xr.open_mfdataset(ifiles)[daname]
        attrs = da.attrs
        da = da.pipe(func)

    da.attrs = attrs #keep the attrs
    #precip units convert: kg/m^2/s -> mm/day
    if daname == 'precip':
        da = da.pipe(lambda x: x*24*3600).assign_attrs(units='mm/day')
        print('precip units: kg/m^2/s -> mm/day')
    if 'grid_xt' in da.dims:
        da = da.rename(grid_xt='lon')
        print('rename: grid_xt -> lon')
    if 'grid_yt' in da.dims:
        da = da.rename(grid_yt='lat')
        print('rename: grid_yt -> lat')
    #save data
    if savedata:
        print('saving...')
        ds = da.to_dataset(name=daname)
        encoding = {daname: {'zlib': True, 'complevel': 1}}
        ds.to_netcdf(ofile, encoding=encoding)
        print('[saved]:', ofile)

    return da

def get_modelout_data_ens(daname, model, expname, ens, years, func=None, funcname='wy', ofile=None, **kws):
    """get model data given daname, model, expname, ens, years, func and parameters from get_modelout_data."""
    if func is None:
        func = lambda x: x
    nens = len(list(ens))
    #ofile
    if ofile is None:
        if nens>1:
            ofile = f'{daname}_{model}_{expname}_{nens}ens_{years[0]:04d}-{years[-1]:04d}_{funcname}.nc'
        else:
            ofile = f'{daname}_{model}_{expname}_ens{list(ens)[0]:02d}_{years[0]:04d}-{years[-1]:04d}_{funcname}.nc'
    if os.path.exists(ofile):
        da = xr.open_dataarray(ofile)
        print('[loaded]:', ofile)
        return da
    else:
        das = []
        for en in ens:
            print(f'{en:02d} of {nens:02d}:')
            da = _get_modelout_data(daname, model, expname, years=years, func=func, funcname=funcname, savedata=False, ens=en, **kws)
            das.append(da)
        print('concatenating over ens...')
        da = xr.concat(das, dim=pd.Index(ens, name='ens'))
        #savedata
        print('saving...')
        ds = da.to_dataset(name=daname)
        encoding = {daname: {'zlib': True, 'complevel': 1}}
        ds.to_netcdf(ofile, encoding=encoding)
        print('[saved]:', ofile)

        return da

def get_modelout_data(**kws):
    """higher level wrap on _get_modelout_data (for non-ens output) and get_modelout_data_ens (for ens output)"""
    ens = kws.pop('ens', None)
    if ens is None:
        return _get_modelout_data(**kws)
    else:
        return get_modelout_data_ens(ens=ens, **kws)
        
 
if __name__ == '__main__':
    #from wyconfig import * #my plot settings
    model = 'AM2.5'
    expname = 'CTL1990s_tigercpu_intelmpi_18_540PE'
    if len(sys.argv)>1: model = sys.argv[1]
    if len(sys.argv)>2: expname = sys.argv[2]
    get_modelout_data('t_surf', model, expname, precheck=True)
    
    #savefig
    if len(sys.argv)>1 and 'savefig' in sys.argv[1:]:
        figname = __file__.replace('.py', f'.png')
        if 'overwritefig' in sys.argv[1:]:
            wysavefig(figname, overwritefig=True)
        else:
            wysavefig(figname)
    tt.check(f'**Done**')
    print()
    #plt.show()
    
