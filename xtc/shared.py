#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Fri May 22 16:12:18 EDT 2020
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
def windscale(windspeed):
    '''convert wind speeds to intensity scales (Saffir–Simpson hurricane wind scale: https://en.wikipedia.org/wiki/Saffir–Simpson_scale):
    0-17m/s: -1 (tropical depression);
    17-33m/s: 0 (tropical storm);
    33-43m/s: 1 (Cat 1 hurricane);
    43-50m/s: 2 (Cat 2 hurricane);
    50-58m/s: 3 (Cat 3 hurricane);
    58-70m/s: 4 (Cat 4 hurricane);
    >=70m/s:  5 (Cat 5 hurricane).
    '''
    w = windspeed
    wscale = w * 0
    if not isinstance(wscale, xr.DataArray):
        wscale = xr.DataArray(wscale)
    wscale.load() #
    
    #assign values according to wind speed range
    wscale.values[w<=17]         = -1
    #wscale.values[(w>17)&(w<33)] = 0 #this is the value of initial assignment
    wscale.values[(w>33)&(w<43)] = 1
    wscale.values[(w>43)&(w<50)] = 2
    wscale.values[(w>50)&(w<58)] = 3
    wscale.values[(w>58)&(w<70)] = 4
    wscale.values[(w>=70)]       = 5

    #add some meta info
    long_name = 'Saffir–Simpson hurricane wind scale'
    note = '-1: tropical depression; 0: tropical storm; 1-5: cat1-5 hurricanes'
    labels = 'TD, TS, C1, C2, C3, C4, C5'
    wscale = wscale.assign_attrs(long_name=long_name, note=note, labels=labels)
    
    return wscale
 
if __name__ == '__main__':
    #from wyconfig import * #my plot settings
    tt.check(f'**Done**')
    
