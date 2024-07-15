#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Fri Mar  3 15:40:12 EST 2023
#2023-10-24: add input arg pfull and funcname selpfull (WY)
if __name__ == '__main__':
    import sys,os
    from misc.timer import Timer
    tt = Timer(f'[{os.getcwd()}] start ' + ' '.join(sys.argv))
import sys, os.path, os, glob, datetime
import xarray as xr, numpy as np, pandas as pd, matplotlib.pyplot as plt
#more imports
from misc import get_kws_from_argv
from .modelout import get_modelout_data, update_modelout_data
import geoxarray
from misc.landmask import whereland, whereocean
from misc.seasons import sel_season
#
if __name__ == '__main__':
    tt.check('end import')
#
#start from here
#input args
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
lonlatbox = get_kws_from_argv('lonlatbox', default=None) #required for funcname=fldmean; e.g. lonlatbox=190,240,-5,5, lon range is 0-360
if lonlatbox is not None:
    ss = lonlatbox.split(',') #e.g. lonlatbox=190,240,-5,5, lon range is 0-360
    lonmin,lonmax,latmin,latmax = float(ss[0]), float(ss[1]), float(ss[2]), float(ss[3])
lonlat = get_kws_from_argv('lonlat', default=None) #required for funcname=interp/selnearest; e.g. lonlat=190,240, lon range is 0-360
if lonlat is not None:
    ss = lonlat.split(',') #e.g. lonlat=190,240, lon range is 0-360
    lon0,lat0 = float(ss[0]), float(ss[1])
lonlat_name = get_kws_from_argv('lonlat_name', default=None) #optional. will be used in ofile name if not None
season = get_kws_from_argv('season', default=None) #required for funcname=seasonmean(,vpd)
pfull = get_kws_from_argv('pfull', default=None) #required for funcname=selpfull; units hPa; e.g. pfull=500
if pfull is not None: pfull = float(pfull) #from str to float

#funcname = get_kws_from_argv('funcname', default='glbmean')
funcname = get_kws_from_argv('funcname', default='glbmean')

#dict of popular pre-defined functions
funcs = dict()
funcs['none'] = lambda da: da.load() #get the raw data
#fldmean related
rename_xy = lambda da: da.rename(grid_xt='lon', grid_yt='lat') if 'grid_xt' in da.dims else da
funcs['glbmean'] = lambda da: da.load().geo.fldmean()
funcs['landmean'] = lambda da: da.load().pipe(whereland).geo.fldmean()
funcs['troplandmean'] = lambda da: da.load().pipe(whereland).pipe(rename_xy).sel(lat=slice(-30,30)).geo.fldmean()
funcs['oceanmean'] = lambda da: da.load().pipe(whereocean).geo.fldmean()
funcs['tropoceanmean'] = lambda da: da.load().pipe(whereocean).pipe(rename_xy).sel(lat=slice(-30,30)).geo.fldmean()
funcs['tropmean'] = lambda da: da.pipe(rename_xy).sel(lat=slice(-30,30)).load().geo.fldmean()
#funcs['trop10mean'] = lambda da: da.pipe(rename_xy).sel(lat=slice(-10,10)).load().geo.fldmean()
#funcs['trop20mean'] = lambda da: da.pipe(rename_xy).sel(lat=slice(-20,20)).load().geo.fldmean()
#funcs['trop40mean'] = lambda da: da.pipe(rename_xy).sel(lat=slice(-40,40)).load().geo.fldmean()
#funcs['trop50mean'] = lambda da: da.pipe(rename_xy).sel(lat=slice(-50,50)).load().geo.fldmean()
#funcs['trop60mean'] = lambda da: da.pipe(rename_xy).sel(lat=slice(-60,60)).load().geo.fldmean()
#funcs['trop70mean'] = lambda da: da.pipe(rename_xy).sel(lat=slice(-70,70)).load().geo.fldmean()
#funcs['trop80mean'] = lambda da: da.pipe(rename_xy).sel(lat=slice(-80,80)).load().geo.fldmean()
for latbound in range(10,81,10):
    funcs[f'trop{latbound}mean'] = lambda da: da.pipe(rename_xy).sel(lat=slice(-latbound,latbound)).load().geo.fldmean()
funcs['nhmean'] = lambda da: da.pipe(rename_xy).sel(lat=slice(0,None)).load().geo.fldmean()
funcs['shmean'] = lambda da: da.pipe(rename_xy).sel(lat=slice(None,0)).load().geo.fldmean()
funcs['fldmean'] = lambda da: da.pipe(rename_xy).sel(lon=slice(lonmin, lonmax), lat=slice(latmin, latmax)) \
    .load().geo.fldmean() #needs lonlatbox in sys.argv
funcs['landfldmean'] = lambda da: da.pipe(rename_xy).sel(lon=slice(lonmin, lonmax), lat=slice(latmin, latmax)).pipe(whereland) \
    .load().geo.fldmean() #needs lonlatbox in sys.argv
funcs['oceanfldmean'] = lambda da: da.pipe(rename_xy).sel(lon=slice(lonmin, lonmax), lat=slice(latmin, latmax)).pipe(whereocean) \
    .load().geo.fldmean() #needs lonlatbox in sys.argv
funcs['nino34'] = lambda da: da.pipe(rename_xy).sel(lon=slice(360-170, 360-120), lat=slice(-5, 5)) \
    .load().geo.fldmean() #nino3.4: 170-120W, 5S-5N: https://climatedataguide.ucar.edu/climate-data/nino-sst-indices-nino-12-3-34-4-oni-and-tni

#zonal mean
funcs['zonalmean'] = lambda da: da.pipe(rename_xy).load().mean('lon', keep_attrs=True)
funcs['zonaloceanmean'] = lambda da: da.pipe(rename_xy).load().pipe(whereocean).mean('lon', keep_attrs=True)
funcs['zonallandmean'] = lambda da: da.pipe(rename_xy).load().pipe(whereland).mean('lon', keep_attrs=True)
#annual mean
funcs['annualmean'] = lambda da: da.load().resample(time='AS').mean(keep_attrs=True)
#annual max
funcs['annualmax'] = lambda da: da.load().resample(time='AS').max(keep_attrs=True)
#season mean
funcs['seasonmean'] = lambda da: da.pipe(sel_season, season).load().resample(time='AS').mean(keep_attrs=True) #needs season in sys.argv


#region selection; needs lonlatbox in sys.argv
funcs['selregion'] = lambda da: da.pipe(rename_xy).sel(lon=slice(lonmin, lonmax), lat=slice(latmin, latmax)).load() #needs lonlatbox in sys.argv

#cell grid selection by interpolation; needs lonlat in sys.argv
funcs['interp'] = lambda da: da.pipe(rename_xy).interp(lon=lon0, lat=lat0).load()
#cell grid selection of the nearest; needs lonlat in sys.argv
funcs['selnearest'] = lambda da: da.pipe(rename_xy).sel(lon=lon0, lat=lat0, method='nearest').load()

#pfull selection by interpolation; needs pfull in sys.argv
funcs['selpfull'] = lambda da: da.interp(pfull=pfull).load()

#sea ice extent, daname=None
S = 4*np.pi*6370**2/1e6 #earth surface area, million km**2
units = '10**6 km**2'
funcs['sieGlb'] = lambda ds: (ds['EXT'].load()*ds['CELL_AREA'].load()*S).sum(['xt', 'yt']) \
    .assign_attrs(units=units, long_name='global sea ice extent')
funcs['sieNH'] = lambda ds: (ds['EXT'].load()*ds['CELL_AREA'].load()*S).sel(yt=slice(0,None)).sum(['xt', 'yt']) \
    .assign_attrs(units=units, long_name='NH sea ice extent')
funcs['sieSH'] = lambda ds: (ds['EXT'].load()*ds['CELL_AREA'].load()*S).sel(yt=slice(None,0)).sum(['xt', 'yt']) \
    .assign_attrs(units=units, long_name='SH sea ice extent')

#vapor pressure deficit (from Chiodi et al. 2021  https://doi.org/10.1029/2021GL092830)
def func_vpd(ds):
    """vapor pressure deficit (from Chiodi et al. 2021  https://doi.org/10.1029/2021GL092830)
    es = 6.109*np.exp(17.625*T/(T+243.04)) #units: hPa; T units is degC (not K!)
    vpd = es*(1 - RH/100) #units hPa; RH units is %"""
    t_ref = ds['t_ref'].load() #units degC
    rh_ref = ds['rh_ref'].load() #units %
    RH = rh_ref
    T = t_ref - 273.15 #K -> C
    es = 6.109*np.exp(17.625*T/(T+243.04)) #units: hPa
    vpd = es*(1-RH/100)
    vpd = vpd.pipe(sel_season, season).resample(time='AS').mean() #needs season in sys.argv
    vpd.attrs['units'] = 'hPa'
    return vpd
funcs['vpd'] = func_vpd

#amoc: from /tigress/wenchang/analysis/active_work/amoc/get_amoc.py
def func_amoc2d(ds):
    """AMOC mderdional mass transport (2d: depthxlat) calculated based on ty_trans from the yyyy0101.ocean.nc output
    see /tigress/wenchang/analysis/active_work/amoc/get_amoc.py"""
    #atlantic mask
    ifile = '/tigress/gvecchi/DATA/FOR_FLOR/atlantic.nc'
    mask = xr.open_dataset(ifile)['E551'].rename(GRIDLON_T='lon', GRIDLAT_T='lat') \
        .pipe(lambda x: x.assign_coords(lat=x.lat.values+0.5))
    da = ds['ty_trans'].load() \
        .rename(st_ocean='depth', yu_ocean='lat', xt_ocean='lon') \
        .pipe(lambda x: x.where(mask.assign_coords(lat=x.lat.values)>0)) \
        .sum('lon', keep_attrs=True).cumsum('depth', keep_attrs=True) \
        .resample(time='AS').mean('time', keep_attrs=True)
    return da
funcs['amoc2d'] = func_amoc2d
def func_amoc(ds):
    """AMOC time series from 2d AMOC mderidional mass transport: amoc2d.max(['depth', 'lat'])"""
    da = func_amoc2d(ds)
    return da.max(['depth', 'lat'], keep_attrs=True)
funcs['amoc'] = func_amoc


func = funcs[funcname]
print(f'func = {func}')
#change original funcname for use in output file name
if funcname in ('fldmean', 'landfldmean', 'oceanfldmean'):
    #funcname_output = f'fldmean.{lonmin:g}.{lonmax:g}.{latmin:g}.{latmax:g}' 
    funcname_output = f'{funcname}.{lonmin:g}_{lonmax:g}_{latmin:g}_{latmax:g}' 
    if lonlat_name is not None: funcname_output = funcname_output + f'.{lonlat_name}'
elif funcname == 'selregion':
    #funcname_output = f'region.{lonmin:g}.{lonmax:g}.{latmin:g}.{latmax:g}' 
    funcname_output = f'region.{lonmin:g}_{lonmax:g}_{latmin:g}_{latmax:g}' 
    if lonlat_name is not None: funcname_output = funcname_output + f'.{lonlat_name}'
elif funcname in ('interp', 'selnearest'):
    funcname_output = f'{funcname}.{lon0:g}_{lat0:g}' 
    if lonlat_name is not None: funcname_output = funcname_output + f'.{lonlat_name}'
elif funcname == 'seasonmean':
    funcname_output = f'{season}mean' 
elif funcname.startswith('sie'): #needs daname=None
    daname = None
    dsname = 'ice_month'
elif funcname == 'none':
    funcname_output = dsname
elif funcname in ('selpfull',):
    funcname_output = f'pfull{pfull:g}' 
elif funcname in ('vpd',):
    daname = None
    funcname_output = f'vpd_{season}mean' if season is not None else 'vpd_annualmean'
elif funcname in ('amoc', 'amoc2d'): #needs daname=None
    daname = None
    dsname = 'ocean'
else:
    funcname_output = funcname
#if daname is not None and dsname != 'atmos_month': #add dsname info to the output data file
if dsname != 'atmos_month': #add dsname info to the output data file
    funcname_output = dsname + '.' + funcname_output

 
if __name__ == '__main__':
    #from wyconfig import * #my plot settings
    if 'update' in sys.argv:
        #api: update_modelout_data(daname, model, expname, dsname='atmos_month', ens=None, func=None, funcname='wy', cleanup=True)
        da = update_modelout_data(daname, model, expname, dsname=dsname, ens=ens, func=func, funcname=funcname_output)
    else: 
        #api: get_modelout_data(daname, model, expname, dsname='atmos_month', ens=None, years=None, func=None, funcname='wy', ofile=None, savedata=True):
        da = get_modelout_data(daname, model, expname, dsname=dsname, ens=ens, years=years, func=func, funcname=funcname_output)
    
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
    
