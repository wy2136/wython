#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Fri Mar  6 10:29:28 EST 2020
import sys, os.path, os, datetime
#import xarray as xr, numpy as np, pandas as pd
#import matplotlib.pyplot as plt
#more imports
#
if __name__ == '__main__':
    print()
    today = datetime.date.today()
    today_s = today.strftime('%Y-%m-%d')
    tformat = '%Y-%m-%dT%H:%M:%S'
    t_start = datetime.datetime.now()
    print('[start]:', t_start.strftime(tformat))
    
#start from here
 
 
if __name__ == '__main__':
    t_end = datetime.datetime.now()
    print('[end]:', t_end.strftime(tformat))
    print('[total time used]:', f'{(t_end - t_start).seconds:,} seconds')
    print()
