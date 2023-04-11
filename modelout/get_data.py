#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Fri Mar  3 15:40:12 EST 2023
if __name__ == '__main__':
    import sys,os
    from misc.timer import Timer
    tt = Timer(f'[{os.getcwd()}] start ' + ' '.join(sys.argv))
import sys, os.path, os, glob, datetime
import xarray as xr, numpy as np, pandas as pd, matplotlib.pyplot as plt
#more imports
from misc import get_kws_from_argv
from misc.modelout import get_modelout_data, update_modelout_data
import geoxarray
from misc.landmask import whereland, whereocean
#
if __name__ == '__main__':
    tt.check('end import')
#
#start from here
daname = get_kws_from_argv('daname', default=None)
model = get_kws_from_argv('model', default=None)
expname = get_kws_from_argv('expname', default=None)
dsname = get_kws_from_argv('dsname', default='atmos_month')
years = get_kws_from_argv('years', default=None)
if years is not None:
    if ':' in years: #year range, e.g. years=1980:2000
        ss = years.split(':')
        year_start = int(ss[0])
        year_stop = int(ss[-1])
        years = range(year_start, year_stop+1)
    else: #specify one year, e.g years=2000
        years = [int(years),]
ens = get_kws_from_argv('ens', default=None)
if ens is not None:
    if ':' in ens: #ens range, e.g. ens=1:5
        ss = ens.split(':')
        ens_start = int(ss[0])
        ens_stop = int(ss[-1])
        ens = range(ens_start, ens_stop+1)
    elif ',' in ens: #ens list e.g. ens=0,11,13,15
        ss = ss.split(',')
        ens = [int(s) for s in ss]
    else: #specify one ens, e.g ens=2
        ens = [int(ens),]
lonlatbox = get_kws_from_argv('lonlatbox', default=None) #required for funcname=fldmean
if lonlatbox is not None:
    ss = lonlatbox.split(',') #e.g. lonlatbox=190,240,-5,5, lon range is 0-360
    lonmin,lonmax,latmin,latmax = float(ss[0]), float(ss[1]), float(ss[2]), float(ss[3])
funcname = get_kws_from_argv('funcname', default='glbmean')

#dict of popular pre-defined functions
funcs = dict()
#fldmean related
rename_xy = lambda da: da.rename(grid_xt='lon', grid_yt='lat') if 'grid_xt' in da else da
funcs['glbmean'] = lambda da: da.load().geo.fldmean()
funcs['landmean'] = lambda da: da.load().pipe(whereland).geo.fldmean()
funcs['oceanmean'] = lambda da: da.load().pipe(whereocean).geo.fldmean()
funcs['nhmean'] = lambda da: da.pipe(rename_xy).sel(lat=slice(0,None)).load().geo.fldmean()
funcs['shmean'] = lambda da: da.pipe(rename_xy).sel(lat=slice(None,0)).load().geo.fldmean()
funcs['fldmean'] = lambda da: da.pipe(rename_xy).sel(lon=slice(lonmin, lonmax), lat=slice(latmin, latmax)).load().geo.fldmean() #needs lonlatbox in sys.argv

#region selection
funcs['selregion'] = lambda da: da.pipe(rename_xy).sel(lon=slice(lonmin, lonmax), lat=slice(latmin, latmax)).load() #needs lonlatbox in sys.argv

#sea ice extent, daname=None
S = 4*np.pi*6370**2/1e6 #earth surface area, million km**2
units = '10**6 km**2'
funcs['sieGlb'] = lambda ds: (ds['EXT'].load()*ds['CELL_AREA'].load()*S).sum(['xt', 'yt']) \
    .assign_attrs(units=units, long_name='global sea ice extent')
funcs['sieNH'] = lambda ds: (ds['EXT'].load()*ds['CELL_AREA'].load()*S).sel(yt=slice(0,None)).sum(['xt', 'yt']) \
    .assign_attrs(units=units, long_name='NH sea ice extent')
funcs['sieSH'] = lambda ds: (ds['EXT'].load()*ds['CELL_AREA'].load()*S).sel(yt=slice(None,0)).sum(['xt', 'yt']) \
    .assign_attrs(units=units, long_name='SH sea ice extent')

func = funcs[funcname]
print(f'func = {func}')
#change original funcname for use in output file name
if funcname == 'fldmean':
    funcname = f'fldmean.{lonmin}.{lonmax}.{latmin}.{latmax}' 
elif funcname == 'selregion':
    funcname = f'region.{lonmin:.0f}.{lonmax:.0f}.{latmin:.0f}.{latmax:.0f}' 
elif funcname.startswith('sie'): #needs daname=None
    daname = None
    dsname = 'ice_month'

if 'update' in sys.argv:
    #api: update_modelout_data(daname, model, expname, dsname='atmos_month', ens=None, func=None, funcname='wy', cleanup=True)
    da = update_modelout_data(daname, model, expname, dsname=dsname, ens=ens, func=func, funcname=funcname)
else: 
    #api: get_modelout_data(daname, model, expname, dsname='atmos_month', ens=None, years=None, func=None, funcname='wy', ofile=None, savedata=True):
    da = get_modelout_data(daname, model, expname, dsname=dsname, ens=ens, years=years, func=func, funcname=funcname)
    
 
 
if __name__ == '__main__':
    #from wyconfig import * #my plot settings
    
    #savefig
    if 'savefig' in sys.argv or 's' in sys.argv:
        figname = __file__.replace('.py', f'.png')
        if 'overwritefig' in sys.argv or 'o' in sys.argv:
            wysavefig(figname, overwritefig=True)
        else:
            wysavefig(figname)
    tt.check(f'**Done**')
    print()
    if 'notshowfig' in sys.argv or 'n' in sys.argv:
        pass
    else:
        if 'plt' in globals(): plt.show()
    
