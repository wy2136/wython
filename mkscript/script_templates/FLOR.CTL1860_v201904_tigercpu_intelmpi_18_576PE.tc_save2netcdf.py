#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
#$datetime
if __name__ == '__main__':
    from misc.timer import Timer
    tt = Timer(f'start {__file__}')
import os, os.path, sys
import xarray as xr, numpy as np

from xtc import tc_tracks, tc_basins, tc_count, tc_density, tc_ace, tc_ace_density

model = 'FLOR'
expname = 'CTL1860_v201904_tigercpu_intelmpi_18_576PE'
years = range(1, 11)
ens = None
if ens is not None:
    nens = len(ens)
track_tags = {'FLOR': 'cyclones_gav_ro110_1C_330k',
    'AM2.5': 'cyclones_gav_ro110_1C_330k',
    'HIRAM': 'cyclones_gav_ro110_2p5C_330k',
    'AM2.5C360': 'cyclones_gav_ro110_330k',
    'AM4': 'cyclones_gav_ro110_1C_330k',
    'AM4_urban': 'cyclones_gav_ro250_p75C_550k',
}
track_tag = track_tags[model]#'cyclones_gav_ro110_1C_330k' for FLOR and 'cyclones_gav_ro110_2p5C_330k' for HIRAM
storm_type = 'TS'# possible options: 'TS', 'C15w', 'allstorms'
n_storms_bound = 200 # 10000 for TC seed; 200 for TC
if storm_type == 'TS':
    minMaxWindspeed = 17
else:
    minMaxWindspeed = None
do_track_density = True
do_ace = False 
thisjob = f'{expname}, years={years[0]:04d}-{years[-1]:04d}, ens={ens}, model={model}, storm_type={storm_type}, track_tag={track_tag}'
print('[start]:', thisjob)

# TC tracks
#ofile = f'{model}.{expname}.tc_tracks.{storm_type}.{years[0]:04d}-{years[-1]:04d}.nc'
ofile = f'tc_tracks.{storm_type}.{years[0]:04d}-{years[-1]:04d}.nc'
if ens is not None:
    ofile = ofile.replace(f'.{storm_type}.', f'.{storm_type}.nens{nens}.')
if not os.path.exists(ofile):
    ds = tc_tracks(expname=expname, years=years, ens=ens, model=model,
        track_tag=track_tag, storm_type=storm_type, n_storms_bound=n_storms_bound)

    # save to netcdf
    dnames_float32 = ('lat', 'lon', 'windmax', 'slp', 'tm')
    dnames_int32 = ('month', 'day', 'hour') + ds['lat'].dims
    encoding = {dname: {'dtype': 'float32', 'zlib': True, 'complevel': 1}
        if dname in dnames_float32
        else {'dtype': 'int32', 'zlib': True, 'complevel': 1}
        for dname in dnames_float32 + dnames_int32}
    ds.attrs['note'] = thisjob
    ds.to_netcdf(ofile, encoding=encoding)
    print('[Saved]:', ofile)
else:
    print('[Exists]:', ofile)
    ds = xr.open_dataset(ofile)

# TC # counts in global domain and each basin
#ofile = f'{model}.{expname}.tc_counts.{storm_type}.{years[0]:04d}-{years[-1]:04d}.nc'
ofile = f'tc_counts.{storm_type}.{years[0]:04d}-{years[-1]:04d}.nc'
if ens is not None:
    ofile = ofile.replace(f'.{storm_type}.', f'.{storm_type}.nens{nens}.')
if minMaxWindspeed is not None:
    ofile = ofile.replace(f'.{storm_type}.', f'.{storm_type}{minMaxWindspeed}.')
if not os.path.exists(ofile):
    basins = ('global', 'NA', 'EP', 'WP', 'NI', 'SI', 'AU', 'SP', 'SA')
    n_tc = { basin: tc_count(ds, basin=basin, ws=minMaxWindspeed)
        for basin in basins} # dict comprehension
    ds_counts = xr.Dataset(n_tc)

    # save to netcdf
    dnames = basins + ds_counts['global'].dims
    encoding = {dname: {'dtype': 'int32'}
        for dname in dnames}
    ds_counts.attrs['note'] = thisjob
    ds_counts.to_netcdf(ofile, encoding=encoding)
    print('[Saved]:', ofile)
else:
    print('[Exists]:', ofile)
# monthly to yearly
ofile_yearly = ofile.replace('.nc', '.yearly.nc')
if not os.path.exists(ofile_yearly):
    if 'ds_counts' not in globals():
        ds_counts = xr.load_dataset(ofile)
    ds_counts_yearly = ds_counts.groupby('time.year').sum('time')
    dnames = ('global', 'NA', 'EP', 'WP', 'NI', 'SI', 'AU', 'SP', 'SA')
    encoding = {dname: {'dtype': 'int32'}
        for dname in dnames + ds_counts_yearly['global'].dims}
    for dname in dnames:
        ds_counts_yearly[dname].attrs['long_name'] = f'{dname} yearly TC #'
    ds_counts_yearly.attrs['note'] = thisjob
    ds_counts_yearly.to_netcdf(ofile_yearly, encoding=encoding)
    print('[Saved]:', ofile_yearly)
else:
    print('[Exists]:', ofile_yearly)


# TC track density
if do_track_density:
    #ofile = f'{model}.{expname}.tc_density.{storm_type}.{years[0]:04d}-{years[-1]:04d}.nc'
    ofile = f'tc_density.{storm_type}.{years[0]:04d}-{years[-1]:04d}.nc'
    if ens is not None:
        ofile = ofile.replace(f'.{storm_type}.', f'.{storm_type}.nens{nens}.')
    if minMaxWindspeed is not None:
        ofile = ofile.replace(f'.{storm_type}.', f'.{storm_type}{minMaxWindspeed}.')
        ds_ = ds.where(ds.windmax.max('stage')>minMaxWindspeed)
    else:
        ds_ = ds
    if not os.path.exists(ofile):
        density = tc_density(ds_, lowpass_on=True, genesis_on=False)
        if minMaxWindspeed is None: 
            #genesis location is the first track point
            genesis_density = tc_density(ds_, lowpass_on=True, genesis_on=True) 
        else: 
            #genesis location is the first track point of >minMaxWindspeed and warm core
            genesis_density = tc_density(ds_, lowpass_on=True, genesis_on=True, genesis_condition=(ds.windmax>minMaxWindspeed)&(ds.tm>0))
        ds_density = xr.Dataset(dict(density=density,
                                density_g=genesis_density))

        # save to netcdf
        encoding = {dname: {'dtype': 'int32', 'zlib': True, 'complevel': 1}
            if dname in ['time',]
            else {'dtype': 'float32', 'zlib': True, 'complevel': 1}
            for dname in ['time', 'lat', 'lon', 'density', 'density_g']}
        ds_density.attrs['note'] = thisjob
        ds_density.to_netcdf(ofile, encoding=encoding)
        print('[Saved]:', ofile)
    else:
        print('[Exists]:', ofile)
    # monthly to yearly
    ofile_yearly = ofile.replace('.nc', '.yearly.nc')
    if not os.path.exists(ofile_yearly):
        if 'ds_density' not in globals():
            ds_density = xr.load_dataset(ofile)
        ds_density_yearly = ds_density.groupby('time.year').sum('time')
        # save to netcdf
        ds_density_yearly['density'].attrs['long_name'] = 'TC density'
        ds_density_yearly['density'].attrs['units'] = 'TC days per year per 10x10deg box'
        ds_density_yearly['density_g'].attrs['long_name'] = 'TC genesis density'
        ds_density_yearly['density_g'].attrs['units'] = 'TC genesis # per year per 10x10deg box'
        dnames_float = ('density', 'density_g', 'lat', 'lon')
        dnames_int = ('year', 'en') if 'en' in ds_density_yearly.dims else ('year',)
        encoding = {dname: {'dtype': 'int32', 'zlib': True, 'complevel': 1}
            if dname in dnames_int
            else  {'dtype': 'float32', 'zlib': True, 'complevel': 1}
            for dname in dnames_float + dnames_int}
        ds_density_yearly.attrs['note'] = thisjob
        ds_density_yearly.to_netcdf(ofile_yearly, encoding=encoding)
        print('[Saved]:', ofile_yearly)
    else:
        print('[Exists]:', ofile_yearly)

# TC ACE
if do_ace:
    # TC ACE in global domain and each basin
    #ofile = f'{model}.{expname}.tc_ace.{storm_type}.{years[0]:04d}-{years[-1]:04d}.nc'
    ofile = f'tc_ace.{storm_type}.{years[0]:04d}-{years[-1]:04d}.nc'
    if ens is not None:
        ofile = ofile.replace(f'.{storm_type}.', f'.{storm_type}.nens{nens}.')
    if minMaxWindspeed is not None:
        ofile = ofile.replace(f'.{storm_type}.', f'.{storm_type}{minMaxWindspeed}.')
        ds_ = ds.where(ds.windmax.max('stage')>minMaxWindspeed)
    else:
        ds_ = ds
    if not os.path.exists(ofile):
        basins = ('global', 'NA', 'EP', 'WP', 'NI', 'SI', 'AU', 'SP', 'SA')
        ace = { basin: tc_ace(ds_, basin=basin)
            for basin in basins} # dict comprehension
        ds_ace = xr.Dataset(ace)

        # save to netcdf
        encoding = None
        ds_ace.attrs['note'] = thisjob
        ds_ace.to_netcdf(ofile, encoding=encoding)
        print('[Saved]:', ofile)
    else:
        print('[Exists]:', ofile)
    # monthly to yearly
    ofile_yearly = ofile.replace('.nc', '.yearly.nc')
    if not os.path.exists(ofile_yearly):
        if 'ds_ace' not in globals():
            ds_ace = xr.load_dataset(ofile)
        ds_ace_yearly = ds_ace.groupby('time.year').sum('time', keep_attrs=True)
        encoding = None
        ds_ace_yearly.attrs['note'] = thisjob
        ds_ace_yearly.to_netcdf(ofile_yearly, encoding=encoding)
        print('[Saved]:', ofile_yearly)
    else:
        print('[Exists]:', ofile_yearly)

    # TC ACE density
    ofile = f'{model}.{expname}.tc_ace_density.{storm_type}.{years[0]:04d}-{years[-1]:04d}.nc'
    if ens is not None:
        ofile = ofile.replace(f'.{storm_type}.', f'.{storm_type}.nens{nens}.')
    if minMaxWindspeed is not None:
        ofile = ofile.replace(f'.{storm_type}.', f'.{storm_type}{minMaxWindspeed}.')
        ds_ = ds.where(ds.windmax.max('stage')>minMaxWindspeed)
    else:
        ds_ = ds
    if not os.path.exists(ofile):
        ace_density = tc_ace_density(ds_, lowpass_on=False)
        ds_ace_density = xr.Dataset(dict(ace_density=ace_density))

        # save to netcdf
        encoding = {dname: {'dtype': 'int32', 'zlib': True, 'complevel': 1}
            if dname in ['time',]
            else {'dtype': 'float32', 'zlib': True, 'complevel': 1}
            for dname in ['time', 'lat', 'lon', 'ace_density']}
        ds_ace_density.attrs['note'] = thisjob
        ds_ace_density.to_netcdf(ofile, encoding=encoding)
        print('[Saved]:', ofile)
    else:
        print('[Exists]:', ofile)
    # monthly to yearly
    ofile_yearly = ofile.replace('.nc', '.yearly.nc')
    if not os.path.exists(ofile_yearly):
        if 'ds_ace_density' not in globals():
            ds_ace_density = xr.load_dataset(ofile)
        ds_ace_density_yearly = ds_ace_density.groupby('time.year').sum('time')
        # save to netcdf
        ds_ace_density_yearly['ace_density'].attrs['long_name'] = 'ACE density'
        ds_ace_density_yearly['ace_density'].attrs['units'] = 'm**2 s**-2 * 6hrs per year per 1x1deg box'
        dnames_float = ('ace_density', 'lat', 'lon')
        dnames_int = ('year', 'en') if 'en' in ds_ace_density_yearly.dims else ('year',)
        encoding = {dname: {'dtype': 'int32', 'zlib': True, 'complevel': 1}
            if dname in dnames_int
            else  {'dtype': 'float32', 'zlib': True, 'complevel': 1}
            for dname in dnames_float + dnames_int}
        ds_ace_density_yearly.attrs['note'] = thisjob
        ds_ace_density_yearly.to_netcdf(ofile_yearly, encoding=encoding)
        print('[Saved]:', ofile_yearly)
    else:
        print('[Exists]:', ofile_yearly)

print('[done]:', thisjob)

if __name__ == '__main__':
    tt.check('**done**')
