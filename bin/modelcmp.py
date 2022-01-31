#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Wed Nov 20 11:03:26 EST 2019
import sys, os.path, os, datetime
import xarray as xr, numpy as np, pandas as pd
#import matplotlib.pyplot as plt
print()
 
if __name__ == '__main__':
    #tformat = '%Y-%m-%d %H:%M:%S'
    #t0 = datetime.datetime.now()
    #print('[start]:', t0.strftime(tformat))

    ifiles = sys.argv[1:]
    modelss = [list(xr.open_dataset(ifile).model.values) for ifile in ifiles]


    # models in common
    models_in_common = set(modelss[0]) 
    for models in modelss:
        models_in_common = models_in_common & set(models)
    models_in_common = list(models_in_common)
    models_in_common.sort()
    print(f'**{len(models_in_common):2d}** model(s) in common:')
    print(models_in_common)
    print()

    # models only in each ifile (not in models_in_common)
    for ifile,models in zip(ifiles, modelss):
        models_only_in_ifile = [m for m in models if m not in models_in_common]
        models_only_in_ifile.sort()
        print(f'**{len(models_only_in_ifile)}** model(s) only in {ifile}:')
        print(models_only_in_ifile)
        print()
    
    #t1 = datetime.datetime.now()
    #print('[total time used]:', f'{(t1-t0).seconds:,} seconds')
    #print('[end]:', t1.strftime(tformat))
    #print()
