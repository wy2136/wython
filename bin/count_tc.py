#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Sat Mar 14 21:03:02 EDT 2020
import sys, os.path, os, datetime, glob
#import xarray as xr, numpy as np, pandas as pd
import matplotlib.pyplot as plt
#plt.rcParams['figure.figsize'] = (6, 6*9/16)
#plt.rcParams['figure.dpi'] = 128
from wyconfig import *
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
parser.add_argument('-t', '--tklabel', help='tracking label, e.g. cyclones_gav_ro110_330k, default is automatic')
parser.add_argument('-s', '--storm_type', help='storm type, e.g. TS, allstorms, C15w', default='TS')
parser.add_argument('-b', '--basin', help='basin, e.g. NA, world', default='world')
args = parser.parse_args()
print(args)
user = args.user
#model = 'AM2.5C360'
model = args.model
#expname = 'amipHadISST_tigercpu_intelmpi_18_1080PE'
expname = args.expname
tklabel = args.tklabel#'cyclones_gav_ro110_330k' # tracking labelj
track_tags = {
    'FLOR': 'cyclones_gav_ro110_1C_330k',
    'FLORktc': 'cyclones_gav_ro110_1C_330k',
    'FLORktc2': 'cyclones_gav_ro110_1C_330k',
    'AM2.5': 'cyclones_gav_ro110_1C_330k',
    'AM2.5ktc': 'cyclones_gav_ro110_1C_330k',
    'AM2.5ktc2': 'cyclones_gav_ro110_1C_330k',
    'HIRAM': 'cyclones_gav_ro110_2p5C_330k',
    'AM2.5C360': 'cyclones_gav_ro110_330k',
    'AM4': 'cyclones_gav_ro110_1C_330k',
    'AM4_urban': 'cyclones_gav_ro250_p75C_550k',
}
if tklabel is None:
    tklabel = track_tags[model]
storm_type = args.storm_type
basin = args.basin
if model=='FLOR':
    idir = os.path.join(f'/tigress/{user}/MODEL_OUT', expname)
else:
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
    plt.legend()
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
    #nstorms = [int( os.popen( f'grep "+++" {ifile.replace("yyyy", str(year))} | tail -n1' ).read().split("+++")[0] )
    #    for year in years]
    #updated to take into count of duplicate txt files. WY2022-12-07
    nstorms = [int( os.popen( f'grep "+++" {glob.glob(ifile.replace("yyyy", str(year)))[-1]} | tail -n1' ).read().split("+++")[0] )
        if os.popen( f'grep "+++" {ifile.replace("yyyy", str(year))} | tail -n1' ).read()       
        else 0
        for year in years]
    #print(nstorms); sys.exit()
    print('year: nstorm')
    for year,n in zip(years, nstorms):
        print(f'{year:04d}: {n}')
    plt.plot(years, nstorms)
    plt.pause(0.1)
    plt.text(0.02, 0.95, f'mean storm #: {sum(nstorms)/len(nstorms):.3g}', transform=plt.gca().transAxes, va='top')
plt.xlabel('year')
plt.ylabel(f'{basin} {storm_type} #')
plt.title(f'{model}.{expname.split("_tigercpu_")[0]}')
#plt.tight_layout()
plt.pause(0.1)
print(args)
plt.show()
     
if __name__ == '__main__':
    t_end = datetime.datetime.now()
    print('[end]:', t_end.strftime(tformat))
    print('[total time used]:', f'{(t_end - t_start).seconds:,} seconds')
    print()
