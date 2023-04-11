#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Tue Oct 18 12:14:44 EDT 2022
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
def _get_postp_files(idir, dsname='atmos_month'):
    """get all the nc files and years under the POSTP dir (idir) given the dsname(atmos_month by default)"""
    if not os.path.exists(idir):
        return
    ncfiles = [ncfile for ncfile in os.listdir(idir) if not ncfile.startswith('.') and ncfile.endswith('.nc')]
    if len(ncfiles)==0:
        return
    ncfiles.sort()
    year0, year1 = int(ncfiles[0][:4]), int(ncfiles[-1][:4])
    years = range(year0, year1+1)
    ifiles = [os.path.join(idir, f'{year:04d}0101.{dsname}.nc') for year in years]
    return ifiles, years

def get_modelout_files(model, expname, dsname='atmos_month', ens=None):
    """get all the modelout files and years under the POSTP dir (idir) given the model, expname, dsname(atmos_month by default) and ens (None by default) """
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
    #model output from tigress
    tigress_result = _get_postp_files(idir, dsname=dsname) #model output files, None if not exist

    #model output from scratch
    idir = idir.replace('/tigress/wenchang/MODEL_OUT', '/home/wenchang/scratch') \
        .replace(f'{expname}', f'work/{expname}')
    if model in ('FLOR',):
        idir = idir.replace('home/wenchang/scratch', 'home/wenchang/scratch/FLOR')
    if ens is not None:
        idir = idir.replace(f'en{ens:02d}/', '') \
            .replace('_tigercpu_', f'_e{ens}_tigercpu_')
    scratch_result = _get_postp_files(idir, dsname=dsname)

    if scratch_result is None: #data not in work dir either
        idir = idir.replace('home/wenchang/scratch','home/wenchang/sGEOCLIM/wenchang')
        scratch_result = _get_postp_files(idir, dsname=dsname)

    #merge results from both tigress and scratch
    if tigress_result is None:
        if scratch_result is None: #both None
            return
        else: #only scratch
            ifiles, years = scratch_result
            return ifiles, years
    else:
        if scratch_result is None: #only tigress
            ifiles, years = tigress_result
            return ifiles, years
        else: #both tigress and scratch have output files
            ifiles_tigress, years_tigress = tigress_result
            ifiles_scratch, years_scratch = scratch_result
            #ifiles and years that in scratch but not in tigress
            ifiles_scratch_delta = [ifile for (ifile,year) in zip(ifiles_scratch, years_scratch) if year not in years_tigress]
            years_scratch_delta = [year for (ifile,year) in zip(ifiles_scratch, years_scratch) if year not in years_tigress]

            ifiles = ifiles_tigress + ifiles_scratch_delta
            years = list(years_tigress) + list(years_scratch_delta)

    #restrict years if specified
    return ifiles, years

def _get_modelout_data(daname, model, expname, dsname='atmos_month', ens=None, years=None, func=None, funcname='wy', ofile=None, savedata=True):
    """get model output data given daname, model, expname, ens(None or Int), years(None), func(none) and funcname('wy'), and save to ofile(None).
    expect non-ensemble output or single ensemble member output.
    If daname is None, func will be applied to Dataset(ds). Otherwise, func is applied to DataArray(da, or ds[daname])."""
    #default func
    if func is None:
        func = lambda x: x.load()
    #ifiles
    ifiles_all, years_all = get_modelout_files(model=model, expname=expname, dsname=dsname, ens=ens)
    if years is None: #sel all available years for process
        ifiles_p = ifiles_all
        years_p = years_all
    elif type(years)==str and years.startswith('first'): #sel first few years
        if years == 'first': #first year
            ifiles_p = ifiles_all[0:1]
            years_p = years_all[0:1]
        else: #first few years
            n = int(years[5:]) #e.g., 'first10' -> n = 10
            ifiles_p = ifiles_all[0:n]
            years_p = years_all[0:n]
    elif type(years)==str and years.startswith('last'): #sel last few years
        if years == 'last': #last year
            ifiles_p = ifiles_all[-1:]
            years_p = years_all[-1:]
        else: #last few years
            n = int(years[4:]) #e.g., 'last10' -> n = 10
            ifiles_p = ifiles_all[-n:]
            years_p = years_all[-n:]
    else: #sel subset of years
        ifiles_p = [ifile for (ifile, year) in zip(ifiles_all, years_all) if year in years]
        years_p = [year for (ifile, year) in zip(ifiles_all, years_all) if year in years]
        
    print('ifiles:')
    print(f'{ifiles_p[0]}\n  to\n{ifiles_p[-1]}')
    print('years =', years_p)

    #ofile
    if ofile is None:
        if ens is None:
            ofile = f'{daname}_{model}_{expname}_{years_p[0]:04d}-{years_p[-1]:04d}_{funcname}.nc'
        else:
            ofile = f'{daname}_{model}_{expname}_ens{ens:02d}_{years_p[0]:04d}-{years_p[-1]:04d}_{funcname}.nc'
        if daname is None:
            ofile = ofile.replace(f'{daname}_', f'{funcname}_').replace(f'_{funcname}.nc', '.nc')
        if funcname is None:
            ofile = ofile.replace(f'_{funcname}.nc', '.nc')
    if os.path.exists(ofile):
        da = xr.open_dataarray(ofile)
        print('[loaded]:', ofile)
        return da

    #processing data
    das = []
    nfiles = len(ifiles_p)
    for ii,ifile in enumerate(ifiles_p, start=1):
        print(f'[{ii:03d} of {nfiles:03d}]: {ifile}', daname, funcname)
        if daname is None:
            da = xr.open_dataset(ifile).pipe(func)
        else:
            da = xr.open_dataset(ifile)[daname]
            attrs = da.attrs
            da = da.pipe(func)
        das.append(da)
    print('concatenating over time...')
    if 'Time' in da.dims:
        da = xr.concat(das, dim='Time').rename(Time='time') #time dim name is Time for dsname=atmos_scalar: change it to time
    else:
        da = xr.concat(das, dim='time')

    if daname is not None:
        da.attrs = attrs #keep the attrs

    #units convert for precip, evap, ...: kg/m^2/s -> mm/day
    if daname in ('precip', 'evap', 'prec_conv', 'prec_ls'):
        da = da.pipe(lambda x: x*24*3600).assign_attrs(units='mm/day')
        print('units convert: kg/m^2/s -> mm/day')
    if 'grid_xt' in da.dims:
        da = da.rename(grid_xt='lon')
        print('rename: grid_xt -> lon')
    if 'grid_yt' in da.dims:
        da = da.rename(grid_yt='lat')
        print('rename: grid_yt -> lat')

    if savedata:
        #save data
        print('saving...')
        name = funcname if daname is None else daname
        ds = da.to_dataset(name=name)
        encoding = {name: {'zlib': True, 'complevel': 1}}
        ds.to_netcdf(ofile, encoding=encoding)
        print('[saved]:', ofile)
    
    return da

def _get_modelout_data_ens(daname, model, expname, dsname='atmos_month', ens=None, years=None, func=None, funcname='wy', ofile=None, savedata=True):
    """get model output data given daname, model, expname, ens(None or Int), years(None), func(none) and funcname('wy'), and save to ofile(None).
    expect ensemble output"""
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
    
    #process
    das = []
    for ii in ens:
        print(f'{ii:02d} of {nens:02d}:')
        da = _get_modelout_data(daname=daname, model=model, expname=expname, dsname=dsname,
            ens=ii, years=years, func=func, funcname=funcname, savedata=False)
        das.append(da)
    print('concatenating over ens...')
    da = xr.concat(das, dim=pd.Index(ens, name='ens'))
    
    #savedata
    if savedata:
        print('saving...')
        ds = da.to_dataset(name=daname)
        encoding = {daname: {'zlib': True, 'complevel': 1}}
        ds.to_netcdf(ofile, encoding=encoding)
        print('[saved]:', ofile)
    return da

def get_modelout_data(daname, model, expname, dsname='atmos_month', ens=None, years=None, func=None, funcname='wy', ofile=None, savedata=True):
    """higher level wrap on _get_modelout_data (for non-ens or single-ens output) and _get_modelout_data_ens (for ens output)"""
    if ens is None or type(ens) is int:
        return _get_modelout_data(daname=daname, model=model, expname=expname, dsname=dsname,
            ens=ens, years=years, func=func, funcname=funcname, ofile=ofile, savedata=savedata)
    else:
        return _get_modelout_data_ens(daname=daname, model=model, expname=expname, dsname=dsname,
            ens=ens, years=years, func=func, funcname=funcname, ofile=ofile, savedata=savedata)

def update_modelout_data(daname, model, expname, dsname='atmos_month', ens=None, func=None, funcname='wy', cleanup=True):
    """get data from the still running experiment; used cached result if exists to speed up. 
    if cleanup == False, delete the cached result and redo the process from scratch."""
    print(model, expname, dsname, daname, funcname)
    #data already processed before
    if ens is None:
        s = f'{daname}_{model}_{expname}_????-????_{funcname}.nc'
    else:
        s = f'{daname}_{model}_{expname}_ens{ens:02d}_????-????_{funcname}.nc'
    ifiles = glob.glob(s)
    #print(ifiles); sys.exit()
    if ifiles:
        ifiles.sort()
        da = xr.open_mfdataset(ifiles)[daname].load()
        year_start_cached = da.time.dt.year[0].item()
        year_end_cached = da.time.dt.year[-1].item()
        da_ = da
        if cleanup is True and len(ifiles)>1: #save to a new single data file and clean up the cached results
            ofile = s.replace('????-????', f'{year_start_cached:04d}-{year_end_cached:04d}')
            da.to_dataset().to_netcdf(ofile)
            print('[saved]:', ofile)
            for ifile in ifiles:
                os.remove(ifile)
                print('[old cache removed]:', ifile)
            #da = get_modelout_data(daname=daname, model=model, expname=expname, dsname=dsname, ens=ens, func=func, funcname=funcname)
            #return da
    else:
        da = get_modelout_data(daname=daname, model=model, expname=expname, dsname=dsname, ens=ens, func=func, funcname=funcname)
        return da
    _, years = get_modelout_files(model=model, expname=expname, dsname=dsname, ens=ens)
    if year_end_cached >= years[-1]: #no update
        da = da_
        print('[loaded]:', s)
    else:
        da = get_modelout_data(daname=daname, model=model, expname=expname, dsname=dsname, ens=ens, func=func, funcname=funcname,
            years=range(year_end_cached+1, years[-1]+1))
        da = xr.concat([da_, da], dim='time')
    print()
    return da


if __name__ == '__main__':
    #test
    if 'test' in sys.argv:
        from wyconfig import * #my plot settings
        model = 'CM2.1p1'
        expname = 'CTL1860_1pct2xCO2_tigercpu_intelmpi_18_80PE'
        if 'funcds' in sys.argv:
            #global sea ice area (normalized by Earth area)
            daname = None
            dsname = 'ice_month'
            func = lambda ds: (ds['EXT']*ds['CELL_AREA']).sum(['xt', 'yt'])
            funcname = 'glbIceFrac'
            da = update_modelout_data(daname=daname, model=model, expname=expname, dsname=dsname, func=func, funcname=funcname)
        else: #gmst
            import geoxarray
        
            daname = 't_surf'
            func = lambda da: da.load().geo.fldmean()
            funcname = 'gmst'
            
            #get data over specified years
            years = range(101,121)
            da = get_modelout_data(daname=daname, model=model, expname=expname, years=years, func=func, funcname=funcname)
            print()
            
            #get all available data. use cached result
            da = update_modelout_data(daname=daname, model=model, expname=expname, func=func, funcname=funcname)
            
            #concat cached result
            da = update_modelout_data(daname=daname, model=model, expname=expname, func=func, funcname=funcname)

        da.plot()
    else:#show ifiles given model,expname and dsname
        from misc import get_kws_from_argv
        model = get_kws_from_argv('model', 'CM2.1p1')
        expname = get_kws_from_argv('expname', 'CTL1860_1pct2xCO2_tigercpu_intelmpi_18_80PE')
        dsname = get_kws_from_argv('dsname', 'atmos_month')
        r = get_modelout_files(model=model, expname=expname, dsname=dsname)
        if r is None:
            print('No files found for', model, expname, dsname)
        elif r is not None:
            ifiles, years = r
            print('years =', years)
            print(ifiles[0])
            print('    to')
            print(ifiles[-1])
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
    if 'notshowfig' in sys.argv or 'nf' in sys.argv:
        pass
    else:
        plt.show()
    
