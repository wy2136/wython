#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Mon Aug 19 10:32:34 EDT 2019
import os, os.path, sys
import xarray as xr, numpy as np

from xtc import tc_tracks, tc_basins, tc_count, tc_density, tc_ace, tc_ace_density

if os.path.exists('params.py'):
    from params import expname, years, ens, model, track_tag, storm_type，n_storms_bound
else:
    print('**no params file found**')
    sys.exit()
# expname = 'CTL1860_newdiag_tigercpu_intelmpi_18_576PE'
# years = range(1, 11)
# ens = None
# model = 'FLOR'
# track_tag = None#'cyclones_gav_ro110_1C_330k' for FLOR and 'cyclones_gav_ro110_2p5C_330k' for HIRAM
# storm_type = 'TS'#'C15w'
# n_storms_bound = 200
do_ace = True
do_track_density = True
thisjob = f'{expname}, years={years[0]:04d}-{years[-1]:04d}, ens={ens}, model={model}, storm_type={storm_type}'
print('[start]:', thisjob)

# TC tracks
ofile = f'tc_tracks.{storm_type}.{years[0]:04d}-{years[-1]:04d}.nc'
if not os.path.exists(ofile):
    ds = tc_tracks(expname=expname, years=years, ens=ens, model=model,
        track_tag=track_tag, storm_type=storm_type, n_storms_bound=n_storms_bound)

    # save to netcdf
    dnames_float32 = ('lat', 'lon', 'vmax', 'slp', 'tm')
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
ofile = f'tc_counts.{storm_type}.{years[0]:04d}-{years[-1]:04d}.nc'
if not os.path.exists(ofile):
    basins = ('global', 'NA', 'EP', 'WP', 'NI', 'SI', 'AU', 'SP', 'SA')
    n_tc = { basin: tc_count(ds, basin=basin)
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
    ofile = f'tc_density.{storm_type}.{years[0]:04d}-{years[-1]:04d}.nc'
    if not os.path.exists(ofile):
        density = tc_density(ds, lowpass_on=True, genesis_on=False)
        genesis_density = tc_density(ds, lowpass_on=True, genesis_on=True)
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
    ofile = f'tc_ace.{storm_type}.{years[0]:04d}-{years[-1]:04d}.nc'
    if not os.path.exists(ofile):
        basins = ('global', 'NA', 'EP', 'WP', 'NI', 'SI', 'AU', 'SP', 'SA')
        ace = { basin: tc_ace(ds, basin=basin)
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
    ofile = f'tc_ace_density.{storm_type}.{years[0]:04d}-{years[-1]:04d}.nc'
    if not os.path.exists(ofile):
        ace_density = tc_ace_density(ds, lowpass_on=False)
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
