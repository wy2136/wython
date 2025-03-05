#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Mon Jan 13 02:40:35 PM EST 2025
if __name__ == '__main__':
    import sys,os
    try:
        from misc.timer import Timer
        tt = Timer(f'[{os.getcwd()}] start ' + ' '.join(sys.argv))
    except:
        pass
import sys, os.path, os, glob, datetime
#import xarray as xr, numpy as np, pandas as pd, matplotlib.pyplot as plt
import pandas as pd, numpy as np
#more imports
wython = '/tigress/wenchang/wython'
if wython not in sys.path: sys.path.append(wython); print('added to python path:', wython)
from misc import get_kws_from_argv
#
if __name__ == '__main__':
    try:
        tt.check('end import')
    except:
        pass
#
#start from here
npes_per_node = get_kws_from_argv('npes_per_node', 112)
npes_per_node = int(npes_per_node)
#ocean_npes
ocean_npes = get_kws_from_argv('ocean_npes', 0)
ocean_npes = int(ocean_npes)
#grids
grids_default = 'C360'
grids= get_kws_from_argv('grids', grids_default)
grids = grids.upper()
if grids == 'C360':
    #C360: 360 = 2**3 * 3**2 * 5**1
    I = 3
    J = 2
    K = 1
elif grids == 'C180':
    #C180: 180 = 2**2 * 3**2 * 5**1
    I = 2
    J = 2
    K = 1
elif grids == 'C192':
    #C192: 192 = 2**6 * 3**1 * 5**0
    I = 6
    J = 1
    K = 0
elif grids == 'C96':
    #C192: 96 = 2**5 * 3**1 * 5**0
    I = 5 
    J = 1
    K = 0
ivec = range(0, I*2+1)
jvec = range(0, J*2+1)
kvec = range(0, K*2+1)

min_npes = 500
max_npes = 5000

iis = []
jjs = []
kks = []
npess = []
for kk in kvec:
    for jj in jvec:
        for ii in ivec:
            npes= 2**ii * 3**jj * 5**kk * 2 * 3 + ocean_npes
            if npes >= min_npes and npes<=max_npes:
                print(f'ii = {ii}; jj = {jj}; kk = {kk}; npes = {npes}')
                iis.append(ii)
                jjs.append(jj)
                kks.append(kk)
                npess.append(npes)

df = pd.DataFrame(dict(ii=iis, jj=jjs, kk=kks, npes=npess))
df = df.sort_values(by='npes')
df['nodes'] = df['npes']/npes_per_node
df = df.set_index(np.array(range(1,df.npes.size+1)))
print()
print(df)
#ofile = __file__.replace('.py', f'__{grids}_{npes_per_node}pes_per_node.csv')
ofile = f'npes_fv3_{grids}_{npes_per_node}pes_per_node.csv'
if ocean_npes > 0: ofile = ofile.replace('.csv', f'_ocean{ocean_npes}pes.csv')
df.to_csv(ofile, float_format='%.2f', sep='\t')
print('[saved]:', ofile)
 
 
if __name__ == '__main__':
    #from wyconfig import * #my plot settings
    
    #savefig
    if 'savefig' in sys.argv or 's' in sys.argv:
        figname = __file__.replace('.py', f'.png')
        if 'overwritefig' in sys.argv or 'o' in sys.argv:
            wysavefig(figname, overwritefig=True)
        else:
            wysavefig(figname)
 
    try:
        tt.check(f'**Done**')
    except:
        pass
    print()
    if 'notshowfig' in sys.argv or 'n' in sys.argv:
        pass
    else:
        if 'plt' in globals(): plt.show()
    
