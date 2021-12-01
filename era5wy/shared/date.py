#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Fri Mar  6 14:59:57 EST 2020
import sys, os.path, os, datetime
#import xarray as xr, numpy as np, pandas as pd
#import matplotlib.pyplot as plt
#more imports
import pandas as pd
#
if __name__ == '__main__':
    print()
    today = datetime.date.today()
    today_s = today.strftime('%Y-%m-%d')
    tformat = '%Y-%m-%dT%H:%M:%S'
    t_start = datetime.datetime.now()
    print('[start]:', t_start.strftime(tformat))
    
#start from here
def get_year_month_tuples(start='1979-01', end=None):
    '''return a list of (year, month) tuples starting from '1979-01' to the current (by default)'''
    #start = '1979-01'
    if end is None:
        end = datetime.date.today().strftime('%Y-%m') # end is current month
    dts = pd.date_range(start, end, freq='MS')
    year_months = [(d.year, d.month) for d in dts]
    #print(year_months)
    return year_months
 
if __name__ == '__main__':
    #
    if len(sys.argv)==1:
        start = '1979-01'
        end = None
    elif len(sys.argv)==2:
        start = sys.argv[1]
        end = None
    else:
        start, end = sys.argv[1:3]
    print(get_year_month_tuples(start=start, end=end))

    t_end = datetime.datetime.now()
    print('[end]:', t_end.strftime(tformat))
    print('[total time used]:', f'{(t_end - t_start).seconds:,} seconds')
    print()
