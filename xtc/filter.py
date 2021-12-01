#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Fri Oct 16 15:16:50 EDT 2020
if __name__ == '__main__':
    from misc.timer import Timer
    tt = Timer(f'start {__file__}')
import sys, os.path, os, glob
import xarray as xr, numpy as np, pandas as pd
#import matplotlib.pyplot as plt
#more imports
#
if __name__ == '__main__':
    tt.check('end import')
#
#start from here
def selTS(ds, stormHour=72, wcHour=48, wcWindContHour=36, windthd=17, latMax=40): 
    '''given storm tracks dataset ds, and storm filter parameters stormHour, wcHour and wcWindContHour,
    return the filtered dataset of tropical storm tracks (TS)
    **input**:
        ds: tracks dataset
        stormHour(=72): storm minimum total life in hours
        wcHour(=48): warm core minimum accumulative hours
        wcWindContHour(=36): minimum continous hourf of both warm core and windmax>windthd
        windthd(=17): wind speed threshold in the wcWindContHour condition
        latMax(=40): latitude boundary for the initial track point
    **return**:
        ds_TS
    '''
    #lat range condition
    if latMax is None:
        latMax = 90.1
    L1 = np.abs(ds.lat.isel(stage=0).drop('stage')) < latMax # first appearance point within {latMax}S-{latMax}N
    L = L1

    #storm life condition
    if stormHour is not None:
        L2 = (ds.windmax>0).sum('stage') > stormHour/6 # total life hours >= {stormHours} hours; notice > instead of >= used, which means at least 13 track points are required if stormHours==72
        L = L & L2

    #warm core (WC) hour condition
    if wcHour is not None:
        L3 = (ds.tm>0).sum('stage') > wcHour/6 # warm core hours >= {wcHours} hours
        L = L & L3

    #WC & wind>windthd continuously hour condition
    if wcWindContHour is not None:
        L4 =  ( (ds.tm>0)&(ds.windmax>windthd) ).rolling(stage=wcWindContHour//6+1).sum().max('stage') == wcWindContHour//6+1 # both warm core and windmax>15.75 **continuously** >= 36
        L = L & L4

    return ds.where(L)
 
 
if __name__ == '__main__':
    from wyconfig import * #my plot settings
    # filtered tracks by the sorter script: /tigress/wenchang/analysis/TC/track_sorter_FLOR_fix99.py
    ifile = '/tigress/wenchang/analysis/TC/HIRAM/CTL1990s_v201910_tigercpu_intelmpi_18_540PE/netcdf/HIRAM.CTL1990s_v201910_tigercpu_intelmpi_18_540PE.tc_tracks.TS.0101-0150.nc'
    ds = xr.open_dataset(ifile)

    # now we filter the tracks by ourselves from the allstorms file
    ifile_s = '/tigress/wenchang/analysis/TC/HIRAM/CTL1990s_v201910_tigercpu_intelmpi_18_540PE/netcdf/HIRAM.CTL1990s_v201910_tigercpu_intelmpi_18_540PE.tc_tracks.allstorms.0101-0150.nc' 
    ds_s = xr.open_dataset(ifile_s)
    ntc_sorter = tc_count(ds).groupby('time.year').sum('time')
    ntc_filter = tc_count(ds_s.pipe(selTS)).groupby('time.year').sum('time')

    df = pd.DataFrame(dict(
        NTC_global_from_sorter=ntc_sorter,
        NTC_global_from_filter=ntc_filter))

    df.plot(style=['-', '--'])

    tt.check(f'**Done**')
    plt.show()
