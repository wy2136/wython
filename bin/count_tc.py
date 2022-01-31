#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Sat Mar 14 21:03:02 EDT 2020
import sys, os.path, os, datetime
#import xarray as xr, numpy as np, pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = (6, 6*9/16)
plt.rcParams['figure.dpi'] = 128
#more imports
import argparse
#
if __name__ == '__main__':
    print()
    today = datetime.date.today()
    today_s = today.strftime('%Y-%m-%d')
    tformat = '%Y-%m-%dT%H:%M:%S'
    t_start = datetime.datetime.now()
    print('[start]:', t_start.strftime(tformat))
    
#start from here
#ifile = '/projects/GEOCLIM/wenchang/MODEL_OUT/AM2.5C360/amipHadISST_tigercpu_intelmpi_18_1080PE/en01/analysis_lmh/cyclones_gav_ro110_330k/atmos_2018_2018/Harris.TC/lmh_TCtrack_ts_4x.dat.warm.h29_25.TS.world.20180101-20190101.txt'
parser = argparse.ArgumentParser()
parser.add_argument('-u', '--user', help='user name', default='wenchang')
parser.add_argument('-m', '--model', help='model name, e.g. FLOR, AM2.5C360', default='FLOR')
parser.add_argument('-e', '--expname', help='experiment name')
parser.add_argument('--ens', help='ensemble member')
parser.add_argument('-t', '--tklabel', help='tracking label, e.g. cyclones_gav_ro110_330k')
parser.add_argument('-s', '--storm_type', help='storm type, e.g. TS, allstorms', default='TS')
parser.add_argument('-b', '--basin', help='basin, e.g. NA, world', default='world')
args = parser.parse_args()
print(args)
user = args.user
#model = 'AM2.5C360'
model = args.model
#expname = 'amipHadISST_tigercpu_intelmpi_18_1080PE'
expname = args.expname
tklabel = args.tklabel#'cyclones_gav_ro110_330k' # tracking labelj
storm_type = args.storm_type
basin = args.basin
idir = os.path.join(f'/tigress/{user}/MODEL_OUT', model, expname)
if args.ens is None:
    ens = [int(s[2:]) for s in os.listdir(idir) if s.startswith('en')]
else:
    ens = [int(args.ens)] # specify ensemble member, e.g. --ens=1
if ens:
    ens.sort()
    for en in ens:
        print(f'en = {en:02d}')
        years = [int(s.split('_')[1]) 
            for s in os.listdir( os.path.join(idir, f'en{en:02d}', 'analysis_lmh', tklabel) )
            if s.startswith('atmos_')
            ]
        years.sort()
        #print(years)
        ifile = os.path.join(idir, 
            f'en{en:02d}', 
            'analysis_lmh', 
            tklabel, 
            'atmos_yyyy_yyyy', 
            'Harris.TC', 
            f'lmh_TCtrack_ts_4x.dat.warm.h*.{storm_type}.{basin}.????????-????????.txt')
        nstorms = [int( os.popen( f'grep "+++" {ifile.replace("yyyy", str(year))} | tail -n1' ).read().split("+++")[0] )
            if os.popen( f'grep "+++" {ifile.replace("yyyy", str(year))} | tail -n1' ).read()
            else 0
            for year in years
            ]
        #print(nstorms)
        print('year: nstorm')
        for year,n in zip(years, nstorms):
            print(f'{year:04d}: {n}')
            #plt.plot(year, n, marker='*')
            #plt.pause(0.1)
        plt.plot(years, nstorms, marker='.', label=f'en={en:02d}')
        plt.pause(0.1)
else:
    ens = None
    years = [int(s.split('_')[1]) 
        for s in os.listdir( os.path.join(idir, 'analysis_lmh', tklabel) )
        if s.startswith('atmos_')
        ]
    years.sort()
    #print(years)
    ifile = os.path.join(idir, 
        'analysis_lmh', 
        tklabel, 
        'atmos_yyyy_yyyy', 
        'Harris.TC', 
        f'lmh_TCtrack_ts_4x.dat.warm.h*.{storm_type}.{basin}.????????-????????.txt')
    nstorms = [int( os.popen( f'grep "+++" {ifile.replace("yyyy", str(year))} | tail -n1' ).read().split("+++")[0] )
        for year in years]
    #print(nstorms)
    print('year: nstorm')
    for year,n in zip(years, nstorms):
        print(f'{year:04d}: {n}')
    plt.plot(years, nstorms)
    plt.pause(0.1)
plt.legend()
plt.xlabel('year')
plt.ylabel(f'{basin} {storm_type} #')
plt.title(f'{model}.{expname}')
plt.tight_layout()
plt.pause(0.1)
print(args)
plt.show()
     
if __name__ == '__main__':
    t_end = datetime.datetime.now()
    print('[end]:', t_end.strftime(tformat))
    print('[total time used]:', f'{(t_end - t_start).seconds:,} seconds')
    print()
