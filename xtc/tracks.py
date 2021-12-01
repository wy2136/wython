#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Fri May 17 23:10:38 EDT 2019
#wy2021-05-17: add boolean param hour24 tc_read and tc_tracks; default is True to be compatible with old versions; if False, hour 00 will be used and track points at the end of the year will appear in the begining of the next year, e.g. 2000-12-31:24 -> 2001-01-01:00
import datetime, glob
import numpy as np, xarray as xr, pandas as pd

def tc_read(ifile, n_storms_bound=None, hour24=True):
    '''Extract TC information from txt file and convert to Dataset.

    Input: ifile, tc txt file, e.g. /tigress/wenchang/MODEL_OUT/CTL1860_noleap_tigercpu_intelmpi_18_576PE/analysis_lmh/cyclones_gav_ro110_1C_330k/atmos_11_11/Harris.TC/lmh_TCtrack_ts_4x.dat.warm.h29_25.TS.world.20110101-20120101.txt
    Return: xr.Dataset
    '''
    # e.g. ifile = '/tigress/wenchang/MODEL_OUT/CTL1860_noleap_tigercpu_intelmpi_18_576PE/analysis_lmh/cyclones_gav_ro110_1C_330k/atmos_11_11/Harris.TC/lmh_TCtrack_ts_4x.dat.warm.h29_25.TS.world.20110101-20120101.txt'

    # length of the storm dimension
    if n_storms_bound is None:
        n_storms_bound = 200

    # columns of the txt file
    names = ('time', 'lon', 'lat', 'slp', 'windmax', 'tm')

    # use pandas to read the txt file
    df = pd.read_csv(ifile, sep='\s+', names=names)
    L = np.array(['+++' in t for t in df.time]) # select lines of summary
    isummaries = df.index[L]
    istarts = isummaries + 1 # indices of storm starts
    iends = np.hstack( ( isummaries[1:]-1, df.index[-1])) # indices of storm ends

    # save each variable associated the storms into a 2D ndarray
    shape = (n_storms_bound, 120) # n_storms, n_steps(6-hourly)
    lat = np.zeros(shape) + np.nan
    lon = np.zeros(shape) + np.nan
    windmax = np.zeros(shape) + np.nan
    slp = np.zeros(shape) + np.nan
    tm = np.zeros(shape) + np.nan
    month = np.zeros(shape) + np.nan
    day = np.zeros(shape) + np.nan
    hour = np.zeros(shape) + np.nan
    # loop over all storms
    for i, (istart, iend) in enumerate(zip(istarts, iends)):
        nsteps = min(iend + 1 - istart, shape[1]) # number of steps along the track of a storm, sometimes greater than the specified number of steps shape[1]
        ilocs = slice(istart, istart+nsteps)
        lat[i, :nsteps] = df.iloc[ilocs]['lat']
        lon[i, :nsteps] = df.iloc[ilocs]['lon']
        windmax[i, :nsteps] = df.iloc[ilocs]['windmax']
        slp[i, :nsteps] = df.iloc[ilocs]['slp']
        tm[i, :nsteps] = df.iloc[ilocs]['tm']
        time = pd.Index([ datetime.datetime(year=2000,
                                            month=int(s[-6:-4]),
                                            day=int(s[-4:-2]),
                                            hour=int(s[-2:]))
                        for s in df.iloc[ilocs]['time'] ])
        if hour24:# hours in the format of 06/12/18/24
            time = time.shift(-1, 'H') # shift the time by 1 hour earlier to avoid problems associated with time boundary
            hour[i, :nsteps] = time.hour + 1
        else: #hours in the format of 00/06/12/18
            hour[i, :nsteps] = time.hour
        month[i, :nsteps] = time.month
        day[i, :nsteps] = time.day

    # wrap ndarray into DataArray
    dims = ('storm', 'stage')
    storm = xr.DataArray(np.arange(1, shape[0]+1))
    stage = xr.DataArray(np.arange(shape[1])*6,
                        attrs={'units': 'hours from genesis'})
    coords = [storm, stage]
    lat = xr.DataArray(lat, dims=dims, coords=coords,
                      attrs={'long_name': 'latitude',
                            'units': 'degree north'})
    lon = xr.DataArray(lon, dims=dims, coords=coords,
                      attrs={'long_name': 'longitude',
                            'units': 'degree east'})
    windmax = xr.DataArray(windmax, dims=dims, coords=coords,
                      attrs={'long_name': 'max wind speed',
                            'units': 'm/s'})
    slp = xr.DataArray(slp, dims=dims, coords=coords,
                      attrs={'long_name': 'sea level pressure',
                            'units': 'hPa'})
    tm = xr.DataArray(tm, dims=dims, coords=coords,
                      attrs={'long_name': '300-500hPa air temperature',
                            'units': 'K'})
    month = xr.DataArray(month, dims=dims, coords=coords)
    day = xr.DataArray(day, dims=dims, coords=coords)
    hour = xr.DataArray(hour, dims=dims, coords=coords)

    # wrap DataArray into Dataset
    ds = xr.Dataset(dict(lat=lat, lon=lon,
                         windmax=windmax, slp=slp, tm=tm,
                         month=month, day=day, hour=hour))

    return ds

def _tc_file(expname, year, en=None, track_tag=None, model='FLOR', username='wenchang', storm_type='TS'):
    '''get the tc txt file based on some specified parameters.
    Input:
        expname:
        year:
        en(=None)
        model(='FLOR')
        username(='wenchang')
    Return: filename'''
    if expname in ('era5', 'ERA5'):
        pdir = f'/tigress/{username}/data/era5'
    else:
        if model in ('FLOR', 'flor'):
            pdir = f'/tigress/{username}/MODEL_OUT/{expname}'
        else:
           pdir = f'/tigress/{username}/MODEL_OUT/{model}/{expname}'
        if en is not None:
            pdir = f'{pdir}/en{en:02d}'

    if track_tag is None:
        if model.upper() == 'HIRAM':
            track_tag = 'cyclones_gav_ro110_2p5C_330k'
        elif model.startswith('AM4'):
            track_tag = 'cyclones_gav_ro250_p75C_550k'
        else:
            track_tag = 'cyclones_gav_ro110_1C_330k'

    txtfile = f'{pdir}/analysis_lmh/{track_tag}/atmos_{year}_{year}/Harris.TC/lmh_TCtrack_ts_4x.dat.warm.h*.{storm_type}.world.*.txt'

    return glob.glob(txtfile)[0]

def tc_tracks(expname, years, ens=None, track_tag=None, model='FLOR', username='wenchang', storm_type='TS', n_storms_bound=200, hour24=True):
    '''construct tc dataset based on expname, years, ens, model, username, ...'''
#     username = 'wenchang'
#     expname = 'CTL1860_noleap_tigercpu_intelmpi_18_576PE'
#     years = range(11, 41)
#     expname = 'Agung_PI_ens_noleap'

    if isinstance(years, int):
        years = (years,)
    if isinstance(ens, int):
        ens = (ens,)

    if ens is None:
        ds_years = []
        print(f'years {years[0]:04d}-{years[-1]:04d}:')
        for year in years:
            print(year, end='; ')
            ifile = _tc_file(expname=expname, year=year, model=model, track_tag=track_tag, username=username, storm_type=storm_type)
            ds_years.append(tc_read(ifile, n_storms_bound=n_storms_bound, hour24=hour24))
        print('year end')
        ds = xr.concat(ds_years, dim=pd.Index(years, name='year'))
    else: # ens is given
        ds_ens = []
        print(f'ens {ens[0]:02d}-{ens[-1]:02d}:')
        for en in ens:
            print(f'en = {en:02d}')
            ds_years = []
            print(f'years {years[0]:04d}-{years[-1]:04d}:')
            for year in years:
                print(year, end='; ')
                ifile = _tc_file(expname=expname, year=year, en=en, model=model, track_tag=track_tag, username=username, storm_type=storm_type)
                ds_years.append(tc_read(ifile, n_storms_bound=n_storms_bound, hour24=hour24))
            print('year end')
            ds_ens.append( xr.concat(ds_years, dim=pd.Index(years, name='year')) )
        print('ensemble end')
        ds = xr.concat(ds_ens, dim=pd.Index(ens, name='en'))

    return ds
