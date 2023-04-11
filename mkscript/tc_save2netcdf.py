#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Wed Feb  5 11:37:37 EST 2020
import os, os.path, sys, datetime
#import xarray as xr, numpy as np, pandas as pd
#import matplotlib.pyplot as plt
import argparse
print()

# args setting
parser = argparse.ArgumentParser()
parser.add_argument('--model', help='model name')
parser.add_argument('--expname', help='experiment name')
parser.add_argument('--ens', help='ensemble members, e.g. 1:5')
parser.add_argument('--years', help='model years, e.g. 1:10 or 1981:2000')
args = parser.parse_args()
model = args.model
expname = args.expname
ens = args.ens
if ens:
    ens_start, ens_end = [int(s) for s in ens.split(':')]
years = args.years
if years:
    year_start, year_end = [int(s) for s in years.split(':')]

odir = os.getcwd()
idir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
    'script_templates')
model_template = 'FLOR'
expname_template = 'CTL1860_v201904_tigercpu_intelmpi_18_576PE'
ibasename = f'{model_template}.{expname_template}.tc_save2netcdf.py'
#ibasename = f'tc_save2netcdf.py'

# input template script
ifile = os.path.join(idir, ibasename)

# target script path
obasename = os.path.basename(ifile)
# modify the script name accordingly
if model:
    obasename = obasename.replace(model_template, model)
if expname:
    obasename = obasename.replace(expname_template, expname)
obasename = '.'.join(obasename.split('.')[-2:])
ofile = os.path.join(odir, obasename)
if os.path.exists(ofile):
    print('[exists]:', obasename)
    print()
    sys.exit()

# target script
with open(ifile) as fi:
    icontent = fi.read()
    print('[read]:', ifile)
    with open(ofile, 'w') as fo:
        t = datetime.datetime.now()
        ocontent = icontent.replace('#$datetime', t.strftime('#%Y-%m-%dT%H:%M:%S, %a')) # add time info to the script
        # modify the script content accordingly
        if model:
            ocontent = ocontent.replace(f"model = '{model_template}'", f"model = '{model}'")
        if expname:
            ocontent = ocontent.replace(f"expname = '{expname_template}'", f"expname = '{expname}'")
        if ens:
            ocontent = ocontent.replace(f"ens = None", f"ens = range({ens_start}, {ens_end}+1)")
        if years:
            ocontent = ocontent.replace(f"years = range(1, 11)", f"years = range({year_start}, {year_end}+1)")
        fo.write(ocontent)
        print('[created]:', obasename)

# change the file permissions to 755
os.chmod(ofile, 0o755)
print()
