# -*- coding: utf-8 -*-
"""
@author: yang
"""
from __future__ import print_function

import numpy as np
from netCDF4 import Dataset
import pandas as pd
import webbrowser
from . import data_lib
from . import data_lib_management
from .data_lib_management import *
from .ingrid_operators import get_months

#
# #### general functions
def num2time(num,units):
    '''Convert expression of time from days/months since ... into pandas PeriodIndex.'''
    if units.lower().startswith('months since'):
        period = pd.Period(units.split()[2][:7])
    elif units.lower().startswith('days since'):
        period = pd.Period(units.split()[2])
    else:
        period = None
    return pd.PeriodIndex(period + np.floor(num).astype('int')).to_datetime()
#
# ######## read data into memory
# from netCDF4 import Dataset
def goto(data):
    '''Open the url in a web browser. The data can be a url, a data name or a dataset name.'''
    url = get_url(data)
    webbrowser.open(url)
def open_data(data,*args, **kwargs):
    '''Return the netCDF4.Dataset object. The data can be a url, a data chain or a data name.'''
    url = get_url(data)
    if url.startswith('http://') and 'columbia.edu' in url and not url.endswith('/dods'):
        url += '/dods'
    dataObj = Dataset(url,*args,**kwargs)
    return dataObj
def look(data):
    '''Get a summary for the data. The data can be a url, a data chain or a data name.'''
    with open_data(data=data) as dataObj:
        vnames = dataObj.variables.keys()
        for vname in vnames:
            if hasattr(dataObj.variables[vname],'units'):
                units = dataObj.variables[vname].units
            else:
                units = 'N/A'
            print(
                vname,
                list(
                    zip(dataObj.variables[vname].dimensions,
                    dataObj.variables[vname].shape)
                ),
                '; ', units)
def readnames(data):
    '''Get the list of variable names in the data.'''
    with open_data(data=data) as dataObj:
        vnames = list(dataObj.variables.keys())
    return vnames
def readunits(data,vname=None):
    '''Read variable units. The default vname is the last variable name.'''
    with open_data(data=data) as dataObj:
        if vname is None:
            vnames = list(dataObj.variables.keys())
            vname = vnames[-1]
        if hasattr(dataObj.variables[vname],'units'):
            units = dataObj.variables[vname].units
        else:
            units = 'N/A'
    return units
def read(data,vname=None):
    '''Read data into memory as ndarray or dictionary of ndarrays. '''
    with open_data(data=data) as dataObj:
        vnames = list(dataObj.variables.keys())
        if vname is None:
            vname = vnames[-1]
            zz = dataObj.variables[vname][:]
        elif vname=='all':
            zz = dict()
            for v in vnames:
                zz[v] = dataObj.variables[v][:]
        else:
            zz = dataObj.variables[vname][:]
        return zz
# -------- easy to use read functions
def readall(data):
    return read(data,vname='all')
def readlon(data):
    vnames = readnames(data)
    vname = [v for v in ['X','lon','longitude'] if v in vnames][0]
    return read(data,vname=vname)
def readlat(data):
    vnames = readnames(data)
    vname = [v for v in ['Y','lat','latitude'] if v in vnames][0]
    return read(data,vname=vname)
def readt(data):
    vnames = readnames(data)
    vname = [v for v in ['T','time','time'] if v in vnames][0]
    n = read(data,vname=vname)
    units = readunits(data,vname=vname)
    return num2time(n,units)
#
# ######## high-level read functions
def readXYclim(dname='gpcp',season='annual',yearRange=(1979,2008),xgrid=(0,360,2),ygrid=(-88,88,2),isSquared=False, isDaily=False):
    # initialize
    months = get_months(season)
    N = len(months)
    tRange = (months[0]+' '+str(yearRange[0]),months[-1]+' '+str(yearRange[1]))
    dataurl = get_data(dname)
    if dataurl is None:
        dataurl = dname
    print (dataurl,'\n',season,tRange,xgrid,ygrid)

    # retrive data
    url = ( dataurl + range('T',*tRange)
        + runningAverage('T',N) + step('T',12)
        + average('T')
        + grid('X',*xgrid) + grid('Y',*ygrid)
        )
    if isSquared:
        url = url.replace(average('T'),dup()+mul()+average('T'))
        print ('squred')
    if isDaily:
        url = url.replace(dataurl, dataurl+'/monthlyAverage')
        print('monthlyAverage is used on daily data.')
    print('\n'+url)
    print ('...\n')
    zz = read(url)
    xx = readlon(url)
    yy = readlat(url)

    return zz,xx,yy
