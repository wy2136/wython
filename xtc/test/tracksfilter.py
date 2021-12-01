#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Fri Sep 18 17:02:17 EDT 2020
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
# filtered tracks by the sorter script: /tigress/wenchang/analysis/TC/track_sorter_FLOR_fix99.py
ifile = '/tigress/wenchang/analysis/TC/HIRAM/CTL1990s_v201910_tigercpu_intelmpi_18_540PE/netcdf/HIRAM.CTL1990s_v201910_tigercpu_intelmpi_18_540PE.tc_tracks.TS.0101-0150.nc'
ds = xr.open_dataset(ifile)

# now we filter the tracks by ourselves from the allstorms file
ifile_s = '/tigress/wenchang/analysis/TC/HIRAM/CTL1990s_v201910_tigercpu_intelmpi_18_540PE/netcdf/HIRAM.CTL1990s_v201910_tigercpu_intelmpi_18_540PE.tc_tracks.allstorms.0101-0150.nc'
ds_s = xr.open_dataset(ifile_s)
L1 = np.abs(ds_s.lat.isel(stage=0).drop('stage'))<40 # first appearance point within 40S-40N
L2 = (ds_s.windmax>0).sum('stage')>72/6 # total life >= 72 hours; notice > instead of >= used, which means at least 13 track points are required
L3 = (ds_s.tm>0).sum('stage')>48/6 # warm core life >= 48 hours
L4 =  ( (ds_s.tm>0)&(ds_s.windmax>15.75) ).rolling(stage=36//6+1).sum().max('stage') == 36//6+1 # both warm core and windmax>15.75 **continuously** >= 36 hours
L = L1 & L2 & L3 & L4

ntc_sorter = tc_count(ds).groupby('time.year').sum('time')
ntc_filter = tc_count(ds_s.where(L)).groupby('time.year').sum('time')

df = pd.DataFrame(dict(
    NTC_global_from_sorter=ntc_sorter,
    NTC_global_from_filter=ntc_filter))

if __name__ == '__main__':
    from wyconfig import * #my plot settings
    df.plot()

    tt.check(f'**Done**')
    #plt.show()
