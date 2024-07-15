#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Thu Sep 14 16:06:08 EDT 2023
# get TC counts given model and expname
#wy2024-02-14: add param basin (None by default to get results from all basins); specify the basin name to only for a single basin
# wy2024-02-13: add the kws_selTC parameter to get TC tracks from the 'allstorms' files
if __name__ == '__main__':
    import sys,os
    from misc.timer import Timer
    tt = Timer(f'[{os.getcwd()}] start ' + ' '.join(sys.argv))
import sys, os.path, os, glob, datetime
import xarray as xr, numpy as np, pandas as pd, matplotlib.pyplot as plt
#more imports
wython = '/tigress/wenchang/wython'
if wython not in sys.path: sys.path.append(wython); print('added to python path:', wython)
from misc import get_kws_from_argv
from xtc import tc_tracks, tc_basins, tc_count, tc_density, tc_ace, tc_ace_density
from xtc.filter import selTS
#
if __name__ == '__main__':
    tt.check('end import')
#start from here
track_tags = {
    'FLOR': 'cyclones_gav_ro110_1C_330k',
    'FLORktc': 'cyclones_gav_ro110_1C_330k',
    'FLORktc2': 'cyclones_gav_ro110_1C_330k',
    'AM2.5': 'cyclones_gav_ro110_1C_330k',
    'AM2.5ktc': 'cyclones_gav_ro110_1C_330k',
    'AM2.5ktc2': 'cyclones_gav_ro110_1C_330k',
    'HIRAM': 'cyclones_gav_ro110_2p5C_330k',
    'HIRAMktc2': 'cyclones_gav_ro110_2p5C_330k',
    'AM2.5C360': 'cyclones_gav_ro110_330k',
    'AM2.5C360ktc2': 'cyclones_gav_ro110_330k',
    'AM4': 'cyclones_gav_ro110_1C_330k',
    'AM4_urban': 'cyclones_gav_ro250_p75C_550k',
}
def getTC(model, expname, ens=None, storm_type='TS', return_monthly=False, minWindmax=None, basin=None, **kws_selTS): 
    """
    get TC counts given model and expname, e.g.
    model = 'AM2.5'
    expname = 'amipLMR2019SST0850ic_tigercpu_intelmpi_18_540PE'
    ens = None (default)
    storm_type = 'TS' (default), or 'allstorms'
    retun_monthly = False #by default return yearly values
    """
    #nc encoding
    dnames_float32 = ('lat', 'lon', 'windmax', 'slp', 'tm')
    dnames_int32 = ('month', 'day', 'hour', 'year', 'storm', 'stage') #+ ds['lat'].dims
    if ens is not None: dnames_int32 = dnames_int32 + ('en',)
    encoding = {
        dname: {'dtype': 'float32', 'zlib': True, 'complevel': 1}
        if dname in dnames_float32
        else {'dtype': 'int32', 'zlib': True, 'complevel': 1}
        for dname in dnames_float32 + dnames_int32
    }
    assert ens is None or type(ens)==int, 'ens must be either None or int'
    track_tag = track_tags[model]#'cyclones_gav_ro110_1C_330k' for FLOR and 'cyclones_gav_ro110_2p5C_330k' for HIRAM
    n_storms_bound = None# 200 if storm_type == 'TS' else 10000 # 10000 for TC seed; 200 for TC
    if storm_type == 'TS' and minWindmax is None: minWindmax = 17
    #get years in modelout
    idir = f'/tigress/wenchang/MODEL_OUT/{model}/{expname}/analysis_lmh/{track_tag}'
    if model == 'FLOR': idir = idir.replace(f'/{model}', '')
    if ens is not None: idir = idir.replace(f'/{expname}', f'/{expname}/en{ens:02d}')
    years_in_modelout = [int( d.split('_')[-1] ) for d in os.listdir(idir)]
    years_in_modelout.sort()
    years = years_in_modelout
    
    #get TC tracks first
    ofile = f'tc_tracks.{storm_type}.{model}.{expname}.{years[0]:04d}-{years[-1]:04d}.nc'
    if ens is not None: ofile = ofile.replace(f'.{expname}.', f'.{expname}.ens{ens:02d}.')
    #first check if there are any cached tracks nc files
    s = ofile.replace(f'{years[0]:04d}-{years[-1]:04d}', '????-????') #e.g. tc_tracks.TS.AM2.5.amipLMR2019SST0850ic_tigercpu_intelmpi_18_540PE.ens01.????-????.nc
    ifiles = glob.glob(s)
    if len(ifiles) < 1: #no cached files found, make the tracks ncfile from scratch
        ds = tc_tracks(expname=expname, years=years, ens=ens, model=model,
            track_tag=track_tag, storm_type=storm_type, n_storms_bound=n_storms_bound)
        # save to netcdf
        ds.to_netcdf(ofile, encoding=encoding)
        print('[Saved]:', ofile)
    else: #load the cached files and check if there's any update
        ifiles.sort()
        ds = xr.open_mfdataset(ifiles).load()
        print('[loaded]:', ifiles)
        #get the start/end year from the cached tracks nc files
        year_start_cached  = ds.year.values[0]
        year_end_cached = ds.year.values[-1]
        if len(ifiles) > 1: #concat multiple cached ncfiles into a single one
            ofile = s.replace('????-????', f'{year_start_cached:04d}-{year_end_cached:04d}') 
            # save to netcdf
            ds.to_netcdf(ofile, encoding=encoding)
            print('[Saved]:', ofile)
            for ifile in ifiles:
                os.remove(ifile)
                print('[old cache removed]:', ifile)
        if year_end_cached < years[-1]: #need update
            ds_update = tc_tracks(expname=expname, years=range(year_end_cached+1, years[-1]+1), ens=ens, model=model,
                track_tag=track_tag, storm_type=storm_type, n_storms_bound=n_storms_bound)
            ofile_update = s.replace('????-????', f'{year_end_cached+1:04d}-{years[-1]:04d}') 
            # save to netcdf
            ds_update.to_netcdf(ofile_update, encoding=encoding)
            print('[Saved]:', ofile_update)
            #concat ds and ds_update
            ds = xr.concat([ds, ds_update], dim='year') 

    if storm_type == 'allstorms': ds = selTS(ds, **kws_selTS)
    # TC # counts in global domain and each basin
    if basin is None:
        basins = ('global', 'NA', 'EP', 'WP', 'NI', 'SI', 'AU', 'SP', 'SA')
    else:
        basins = (basin,)
    n_tc = { basin: tc_count(ds, basin=basin, ws=minWindmax)
        for basin in basins} # dict comprehension
    ds_counts = xr.Dataset(n_tc)
    if return_monthly: 
        return ds_counts

    ds_counts_yearly = ds_counts.groupby('time.year').sum('time')
    #dnames = ('global', 'NA', 'EP', 'WP', 'NI', 'SI', 'AU', 'SP', 'SA')
    dnames = basins
    encoding = {dname: {'dtype': 'int32'}
        for dname in dnames + ds_counts_yearly[dnames[0]].dims}
    for dname in dnames:
        ds_counts_yearly[dname].attrs['long_name'] = f'{dname} yearly TC #'

    return ds_counts_yearly

if __name__ == '__main__':
    from wyconfig import * #my plot settings
    model = get_kws_from_argv('model', 'AM2.5')
    expname = get_kws_from_argv('expname', 'CTL1990s_tigercpu_intelmpi_18_540PE')
    ens = get_kws_from_argv('ens', None)
    if ens is not None: ens = int(ens)
    minWindmax = get_kws_from_argv('minWindmax', None)
    if minWindmax is not None: minWindmax = float(minWindmax)
    basin = get_kws_from_argv('basin', 'NA')

    ds = getTC(model=model, expname=expname, ens=ens, minWindmax=minWindmax)
    ds[basin].plot()
    
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
    
