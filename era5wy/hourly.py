#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Fri Mar  6 10:30:42 EST 2020
import sys, os.path, os, datetime
#import xarray as xr, numpy as np, pandas as pd
#import matplotlib.pyplot as plt
#more imports
import cdsapi
c = cdsapi.Client()
#
if __name__ == '__main__':
    print()
    today = datetime.date.today()
    today_s = today.strftime('%Y-%m-%d')
    tformat = '%Y-%m-%dT%H:%M:%S'
    t_start = datetime.datetime.now()
    print('[start]:', t_start.strftime(tformat))
    
#start from here
def download(data_name, year, month, ofile=None, do_4xdaily=False):
    '''download data from ERA5 in the specified year and month'''
    if ofile is None:
        ofile = f'era5.{data_name}.{year}-{month:02d}.nc'
        if do_4xdaily:
            ofile = ofile.replace(data_name, data_name+'.4xdaily')
    time = [
        '00:00','01:00','02:00','03:00','04:00','05:00',
        '06:00','07:00','08:00','09:00','10:00','11:00',
        '12:00','13:00','14:00','15:00','16:00','17:00',
        '18:00','19:00','20:00','21:00','22:00','23:00'
        ]
    if do_4xdaily:
        time = time[0::6]
    if os.path.exists(ofile):
        print('[exists]:', ofile)
        return
    c.retrieve(
    'reanalysis-era5-single-levels',
    {
        'product_type':'reanalysis',
        'format':'netcdf',
        'variable':data_name,
        'year':f'{year}',
        'month':f'{month:02d}',
        'day':[
            '01','02','03',
            '04','05','06',
            '07','08','09',
            '10','11','12',
            '13','14','15',
            '16','17','18',
            '19','20','21',
            '22','23','24',
            '25','26','27',
            '28','29','30',
            '31'
        ],
        'time':time
    },
    ofile) 
 
if __name__ == '__main__':
    #script
    data_name = '2m_temperature'
    year, month = 1979, 1
    download(data_name, year=year, month=month)
    t_end = datetime.datetime.now()
    print('[end]:', t_end.strftime(tformat))
    print('[total time used]:', f'{(t_end - t_start).seconds:,} seconds')
    print()
