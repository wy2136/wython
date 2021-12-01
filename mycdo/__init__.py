# -*- coding: utf-8 -*-
"""
Created on Wed Feb 04, 2015
 
@author: Wenchang Yang 
This module is the python interface to the command line tool of Climate Data Operators (CDO). Each CDO operator is wrapped into a string in a list, and the chain of CDO operators is realized by first adding these individual list together to form a long list and then tranforming the long list into a CDO command string. For example,

    get_ifile('data.nc') --> ['data.nc']
    sel(name='sst') --> ['-selname,sst']
    stat('tim','mean') --> ['-timmean']
    
and

    get_cdocmd( get_ifile('data.nc') + sel(name='sst') + stat('tim','mean'), ofile1='sst_timmean.nc' )
    -->
    'cdo -timmean -selname,sst data.nc sst_timmean.nc'
    
Now we can use the os.system function to run the CDO command:

    os.system('cdo -timmean -selname,sst data.nc sst_timmean.nc')

The module is designed such that it can take full advantage of the CDO chain operators. 

The module requires the CDO command tool as well as python module Numpy,netCDF4 and Pandas. The module also has the capability to manipulate data on a remote server as long as: 
    1) (required) The remote server has installed the CDO tools (required).
    2) (optional) The remote server has the mycdo python module (e.g. in /home/wenchay/mypython/mycdo.py) 
    3) (optional) The remote server user home path has a python file named .cdo_dump.py with content as:
            import sys
            sys.path.append(mycdo_module_dir)
            import mycdo as mc
            mc.dump('tmp.nc')
"""
from __future__ import print_function

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

import os, os.path
import tempfile
from netCDF4 import Dataset
import pandas as pd
import numpy as np
import shutil
import glob
import subprocess

# parameters
_server='wenchay@engey.ess.uci.edu'
_userHome='/home/wenchay/'

# 
# ######## functions that wrap cdo operators into strings in a list
# ---- input file
def get_ifile(ifile):
    '''Return a list with the ifile as the element. The ifile can be a string or list.'''
    if type(ifile) is list:
        return ifile
    else:
        fname = ifile
        if not os.path.exists(fname) and not fname.startswith('/'):
            fname = _userHome + fname
        return [fname]
def get_ifiles(ifile):
    '''Same as the function get_ifile except that the file name include unix-style wildcards.'''
    fname = get_ifile(ifile)[0]
    fname = '\'' + fname + '\''
    return [fname]
def at_local(ifile):
    '''Condition on whether the ifile is on local machine or on the remote server.'''
    if type(ifile) is str:
        fname = ifile
    else:
        fname = ifile[0]
    if fname.startswith("'") and fname.endswith("'"):
        fname = fname[1:-1]
    if glob.glob(fname) or os.uname()[1] in _server:
        return True
    else:
        return False
# ---- file operations
# ---- selection
def get_sel_param_name_list():
    '''Get a list of parameter names used for the sel* operator.'''
    return ['name','stdname','param','code',
            'level','levidx','grid','zaxis','ltype','tabnum',
            'timestep','year','seas','mon','day','hour','time',
            'date','smon',
            'lonlatbox','indexbox'
            ]
def get_select_param_name_list():
    '''Get a list of parameter names used for the select operator.'''
    return ['name','param','code',
            'level','levidx','ltype',
            'minute','hour','day','month','year','timestep','timestep_of_year']
def sel(**kwargs):
    '''CDO sel* operators. Input arguments are key-value pairs with keys from the return of function get_sel_param_name_list(), and values are all string types with format similar to the CDO command.'''
    chain = list()
    for key in [key for key in kwargs.keys() if key in get_sel_param_name_list()]:
        chain += [ '-sel'+key+','+kwargs[key] ]
    if not chain:
        print ('Please choose proper input arguments with keys from:\n',
            get_sel_param_name_list()
        )
        return
    return chain
def select(**kwargs):
    '''CDO select operators. Input arguments are key-value pairs with keys from the return of function get_sel_param_name_list(), and values are all string types with format similar to the CDO command.\nFunction select can manipulate multiple files while sel* can only operate on a single file.'''
    chain = list()
    cmd = '-select'
    
    # generate the select commands
    for key in [key for key in kwargs.keys() 
            if key in get_select_param_name_list()]:
        cmd += ',' + key + '=' + kwargs[key]
    if cmd=='-select':
        print ('''Please choose proper input arguments listed in the return of function get_select_param_name_list():\n''',
            get_select_param_name_list())
        return
    else:
        chain = [cmd]
    
    # generate the sel* commands after the select
    for key in [key for key in kwargs.keys() 
            if key not in get_select_param_name_list()
            and key in get_sel_param_name_list()]:
            chain += [ '-sel'+key+','+kwargs[key] ]
    
    return chain

# ---- conditional selection
# ---- comparison
# ---- modification
def get_change_param_name_list():
    '''Get a list of parameter names used for the ch* operator'''
    return ['code','param',
            'name','unit','level','levelc','levelv']
def get_set_param_name_list():
    '''Get a list of parameter names used for the set* operator.'''
    return ['parttabp','partabn','partab','code','param',
            'name','unit','level','ltype',
            'date','time','day','mon','year','tunits',
            'taxis','treftime','calendar'
            'grid','gridtype','gridarea',
            'zaxis',
            'gatt','gatts',
            'clonlatbox','cindexbox',
            'missval','ctomiss','misstoc','rtomiss','vrange']
def change(param,old,new):
    if param in get_change_param_name_list():
        return [ '-ch'+param+','+old+','+new ]
    else:
        print ('Please choose proper input parameters from the return of function get_change_param_name_list():\n',get_change_param_name_list())
def enlarge(grid):
    return [ '-enlarge,'+grid ]
def invertlat():
    return [ '-invertlat' ]
def invertlev():
    return [ '-invertlev' ]
def set(**kwargs):
    chain = list()
    for key in [key for key in kwargs.keys() if key in get_set_param_name_list()]:
        chain += [ '-set'+key+','+kwargs[key] ]
    if not chain:
        print ('Please choose proper input arguments with keys from:\n' \
            ,get_sel_param_name_list())
        return
    return chain
def shifttime(timeString):
    return [ '-shifttime,'+timeString ]
# ---- arithmetic
def arith(operator,ifile1=None,ifile2=None):
    chain = ['-'+operator ]
    if ifile1 is not None:
        chain = get_ifile(ifile1) + chain
    if ifile2 is not None:
        chain = get_ifile(ifile2) + chain
    return chain
def expr(expression):
    return [ '-expr,' + '\'' + expression + '\'' ]
# ---- statistics
def get_stat_param_name_list():
    '''return the list of list of dimension names.'''
    return [
        ['zon','zonal','lon','longitude','longitudinal','x'],
        ['mer','meridional','lat','latitude','latitudinal','y'],
        ['fld','field'],
        ['vert','vertical'],
        ['tim','time'],
        ['year','yearly'],
        ['seas','season','seasonal'],
        ['mon','month','monthly'],
        ['day','daily'],
        ['hour','hourly'],
        ['ymon','multi-year monthly'],
        ['yday','multi-year daily'],
        ['run','running']
        ]
def stat(overDimension='time',statName='mean',N=None,ifile=None):
    # get the dimension name
    s = overDimension.lower()
    dimension = [par_list for par_list in get_stat_param_name_list() if s in par_list][0][0]
    # statistics name
    if statName.lower()=='percentile':
        statName = 'pctl'
        
    cmd =  dimension + statName
    # running statistics with a num of points parameter
    if dimension=='run':
        cmd += ','+str(N)
        
    # whether to combine the operator and the ifile or not
    chain = [ '-'+cmd ]
    if ifile is not None:
        chain = get_ifile(ifile) + chain
    
    return chain
def stat_pctl(ifile,N,overDimension='time'):
    '''percentile over time or similar dimension that needs three ifiles'''
    return get_ifile(ifile) + stat(overDimension,'max') \
            + get_ifile(ifile) + stat(overDimension,'min') \
            + get_ifile(ifile) + stat(overDimension,'pctl,'+str(N))
# ---- correlation
def cor(dim='tim'):
    '''Correlation coefficients.Dimension can be tim or fld. '''
    chain = list();
    chain += [ '-' + dim + 'cor' ]
    return chain
def covar(dim='tim'):
    '''Covariance. Dimension can be tim or fld. '''
    chain = list();
    chain += ['-' + dim + 'covar' ]
    return chain
# ---- regression
def regress():
    return [ '-regres' ]
def detrend():
    return [ '-detrend' ]
# ---- EOFs
# ---- interpolation
# ---- transformation
# ---- import/export
# ---- miscellaneous
# ---- climate indices
# 
# ######## low-level functions
# ---- convert the chain of cdo operators to a command string that can be executed in shell
def get_cdocmd(chain,ofile1=None,ofile2=None):
    '''Transforms the chain of operators into a string that is executable in Shell.\n\nchain is a list representing chains of operators.'''
    if ofile1 is None:
        ofile = ''
    else:
        ofile = ofile1
    if ofile2 is not None:
        ofile += ' ' + ofile2
    if len(chain)==1:
        cdocmd = 'cdo pardes ' + chain[0]
    else:
        cdocmd = 'cdo ' + ' '.join(chain[-1::-1]) + ' ' + ofile
    return cdocmd
# ---- run system commands
def run_command(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,**kwargs):
    if type(cmd) is str:
        cmd = cmd.split()
    p = subprocess.Popen(cmd,stdout=stdout,stderr=stderr,**kwargs)
    stdout,stderr = p.communicate()
    exitCode = p.returncode
    if exitCode:
        print (stderr)
    else:
        print (stdout)
    return exitCode
# ---- communicate with the remote server
def run_cdo_remote(cdocmd=None,server=_server,otxtfile='.tmp.txt'):
    sshcmd = "ssh -t " + server +  ' "' \
        + cdocmd \
        + " > " + otxtfile \
        + '" '
    print ('\n','-'*10, 'Connecting to server ...\n',sshcmd)
    if os.system(sshcmd)==0:
        with tempfile.NamedTemporaryFile(suffix='.txt') as tmp:
            copycmd = "scp " + server + ":~/" + otxtfile + ' '  + tmp.name
            print ('\n','-'*10,'Download and show what has been shown on remote server screen ...\n',copycmd)
            if os.system(copycmd)==0: # scp the result file to the local temp file
                return os.system('cat ' + tmp.name)
def download_datafile(datafile_remote='.tmp.nc',server=_server):
    tmp = tempfile.NamedTemporaryFile(suffix='.nc')
    copycmd = "scp " + server + ":~/" + datafile_remote + ' '  + tmp.name
    print ('\n','-'*10,'Download data file on remote server ...\n',copycmd)
    os.system(copycmd)
    return tmp
# ---- convert the chain of cdo operators into python file objects
def get_data_file_obj(chain):
    '''Generates a temporary file object pointing to the output netcdf file. \n\nchain can be a list of cdo commands or a string of input file name.'''
    if type(chain) is str:
        datafile = chain
        if at_local(datafile): # data is at local
            tmp = open(datafile)
        else: # data is at remote server
            datafile = get_ifile(chain)[0]
            tmp = download_datafile(datafile_remote=datafile,server=_server)
    elif type(chain) is list:
        if at_local(chain): # data is at local
            tmp = tempfile.NamedTemporaryFile(suffix='.nc')
            cdocmd = get_cdocmd(chain,ofile1=tmp.name)
            print ('\n','-'*10,'Running cdo ...')
            print (cdocmd)
            os.system(cdocmd)
        else: # data is at remote server
            if run_cdo_remote( cdocmd=get_cdocmd(chain,ofile1='.tmp.nc'),server=_server )==0:
                tmp = download_datafile(datafile_remote='.tmp.nc',server=_server)
    return tmp
# 
# ######## high-level functions
# ---- query information about the ifile or modified ifile
def get_show_param_name_list():
    '''Get a list of parameter names used for the show* operator.'''
    return ['format','code',
            'name','stdname',
            'level','ltype',
            'year','mon','date','time','timestamp'
            ]
def get_des_param_name_list():
    '''Get a list of paramerter name used for the show* operator.'''
    return ['par','grid','zaxis','vct']
def info(ifile):
    '''Equivalent to the cdo operator infon.'''
    ifile = get_ifile(ifile)
    cdocmd = 'cdo infon ' + ' '.join(ifile[-1::-1])
    if at_local(ifile):
        return run_command(cdocmd)
    else:
        return run_cdo_remote(cdocmd=cdocmd)
def sinfo(ifile):
    '''Equivalent to the cdo operator sinfon.'''
    ifile = get_ifile(ifile)
    cdocmd = 'cdo sinfon ' + ' '.join(ifile[-1::-1])
    if at_local(ifile):
        return run_command(cdocmd)
    else:
        return run_cdo_remote(cdocmd=cdocmd)
def show(ifile,param='par'):
    cdocmd = ' '.join( get_ifile(ifile)[-1::-1] )
    if param in get_show_param_name_list():
         cdocmd = 'cdo show' + param + ' ' + cdocmd
    elif param in get_des_param_name_list():
        cdocmd = 'cdo ' + param + 'des ' + cdocmd
    else:
        print ('Please choose proper params from the return of function get_show_param_name_list() or the function get_des_param_name_list():\n',get_show_param_name_list(),'\n or \n',get_des_param_name_list())
        return
    if at_local(ifile):
        return run_command(cdocmd)
    else:
        return run_cdo_remote(cdocmd)
def look(chain):
    '''Dump a local netcdf file, or dump a remote netcdf file and then download the results. \n\n The input argument chain can be either a string (netcdf file name) or a list representing a chain of cdo operators.'''
    if at_local(chain):
        with get_data_file_obj(chain) as tmp:
            # dump the output netcdf file
            print ('\n','-'*10,'Data file information:...')
            filesize = os.path.getsize(tmp.name); units = 'B'
            if filesize > 10000:
                filesize /= 1000; units = 'K'
                if filesize > 10000:
                    filesize /= 1000; units = 'M'
            print (tmp.name+': ',str(filesize) + units)
            with Dataset(tmp.name) as ncobj:
                vnames = ncobj.variables.keys()
                for vname in vnames:
                    if hasattr(ncobj.variables[vname],'units'):
                        units = ncobj.variables[vname].units
                    else:
                        units = 'units N/A'
                    print (vname, zip(ncobj.variables[vname].dimensions,
                            ncobj.variables[vname].shape),
                            '; ', units)
    else:# not at_local(chain)
        try:
            if type(chain) is str or ( type(chain) is list and len(chain)==1 ):
                fname = get_ifile(chain)[0]
                cdocmd = "ln -sfn " + fname + " ~/.tmp.nc && python .cdo_dump.py && rm ~/.tmp.nc"
            else:
                cdocmd = get_cdocmd(chain,output='.tmp.nc') + " && python .cdo_dump.py "
            run_cdo_remote(cdocmd=cdocmd)
        except:
            ifile = get_ifile(chain)
            cdocmd = 'cdo sinfon ' + ' '.join( ifile[-1::-1] )
            run_cdo_remote(cdocmd=cdocmd)
# ---- save result data file into ofile
def save(chain,ofile1=None,ofile2=None):
    '''save the final netcdf file to the output file.'''
    if ofile1 is not None:
        if at_local(chain):
            cdocmd = get_cdocmd(chain=chain,ofile1=ofile1,ofile2=ofile2)
            if os.system(cdocmd)==0:
                print ('\n'+'-'*10,'File has been saved to','\nofile1:',ofile1,'\nofile2:',ofile2)
        else:
            ofile1 = get_ifile(ofile1)[0]
            if ofile2 is not None:
                ofile2 = get_ifile(ofile2)[0]
            cdocmd = get_cdocmd(chain=chain,ofile1=ofile1,ofile2=ofile2)
            if run_cdo_remote(cdocmd=cdocmd)==0:
                print ('\n'+'-'*10,'File has been saved on server to','\nofile1:',ofile1,'\nofile2:',ofile2)
    else:
        print ('Please choose output file names.')
# ---- read result data file into memory as ndarray or dictionary of ndarray
def get_months(season='Annual'):
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',
              'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    if season.lower()=='annual': # 12 months array
        months = months[:12]
    elif season in months: # season contains only one month
        months = [season]
    else: # season defined by consecutive month initials
        months_short = 'JFMAMJJASONDJFMAMJ'
        i = months_short.find(season)
        N = len(season)
        months = months[i:i+N]
    return months
def num2time(num,units):
    '''Convert expression of time from days/months since ... into pandas PeriodIndex.'''
    if units.lower().startswith('months since'):
        period = pd.Period(units.split()[2][:7])
    elif units.lower().startswith('days since'):
        period = pd.Period(units.split()[2])
    else:
        period = None
    return pd.PeriodIndex(period + np.floor(num).astype('int'))
def read(chain,varname=None):
    '''Read the output netcdf file into memory as a dictionary. \n\n chain can be either a string (netcdf file name) or a list representing chains of operators. \n\n return a numpy array value if vname is not None.'''
    with get_data_file_obj(chain=chain) as tmp:
        with Dataset(tmp.name) as ncobj:
            vnames = ncobj.variables.keys()
            zzDict = dict()
            if varname is None:
                vnames = ncobj.variables.keys()
            else:
                vnames = [varname]
            for vname in vnames:
                zzDict[vname] = ncobj.variables[vname][:]
                if vname in ['time','T','T2']: # change the time units
                    tN = ncobj.variables[vname][:]
                    units = ncobj.variables[vname].units
                    zzDict[vname] = num2time(tN,units)
    if varname is None:
        return zzDict
    else:
        return zzDict[varname]
# 

