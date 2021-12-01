#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Tue Apr 30 16:39:22 EDT 2019
import os, os.path, sys
import cdsapi
c = cdsapi.Client()

# params
data_name = '2m_temperature'
years = range(1979,2019)
months = range(1,13)

# function
def download(data_name, year, month):
    '''download data from ERA5 in the specified year and month'''
    ofile = f'era5.{data_name}.{year}-{month:02d}.nc'
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
        'time':[
            '00:00','01:00','02:00',
            '03:00','04:00','05:00',
            '06:00','07:00','08:00',
            '09:00','10:00','11:00',
            '12:00','13:00','14:00',
            '15:00','16:00','17:00',
            '18:00','19:00','20:00',
            '21:00','22:00','23:00'
        ]
    },
    ofile)    

# run the script
if __name__ == '__main__':
    for year in years:
        for month in months:
            download(data_name, year, month)
