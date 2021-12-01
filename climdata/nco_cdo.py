# requirements: nco, cdo
# python wrapper for the shell tools of nco and cdo
from __future__ import print_function
import os, sys
from netCDF4 import Dataset
from functools import partial
import glob

from .util import (_run_shell, run_shell, cdo)

def cdo_sellevel(levels, ifile, ofile):
    '''CDO command: cdo sellevel,levels ifile ofile. Levels can be both a number or a list of numbers.'''
    if isinstance(levels, (int, float)):
        levels_str = str(levels)
    else:
        levels_str = ','.join([
            str(level) for level in levels
        ])
    cmd = ' '.join([
        'cdo',
        'sellevel,'+levels_str,
        ifile,
        ofile
    ])
    _run_shell(cmd)
def cdo_detrend(ifile, ofile):
    '''CDO detrend operator.'''
    cmd = ' '.join([
        'cdo',
        'detrend',
        ifile,
        ofile
    ])
    _run_shell(cmd)
nc_detrend = cdo_detrend
def nc_mean(ifile, ofile, option='tim'):
    '''Statistical mean of the ifile. timeshift is a string, e.g. '-6hours'.'''
    cmd = ' '.join([
        'cdo',
        option + 'mean',
        ifile,
        ofile
    ])
    _run_shell(cmd)
nc_daymean = partial(nc_mean, option='day')
def nc_monmean(ifile, ofile):
    '''Convert sub-monthly (usually daily) data into monthly data.'''
    cmd = ' '.join([
        'cdo',
        'monmean',
        ifile,
        ofile
    ])
    _run_shell(cmd)
def nc_mergetime(ifiles, ofile):
    '''CDO operator mergetime. ifiles can be either a string(wildcards can be used) or sequence.'''
    if isinstance(ifiles, str):
        ifiles = glob.glob(ifiles)
    cmd = ' '.join([
        'cdo --history',
        'mergetime',
        ' '.join(ifiles),
        ofile
    ])
    _run_shell(cmd)
def _query_vname(ifile):
    return os.popen('cdo showname ' + ifile).read().strip()
def nc_pack(ifile, ofile=None, option='-O -h'):
    if ofile is None:
        ofile = 'packed.' + ifile
    vname = _query_vname(ifile=ifile)
    # cmd = ' '.join([
    #     "ncap2 -O -s",
    #     " '%s=pack(%s)' "%(vname, vname),
    #     ifile,
    #     ofile
    # ])
    # _run_shell(cmd)
    run_shell('ncpdq', option, ifile, ofile)
def nc_unpack(ifile, ofile=None):
    if ofile is None:
        ofile = 'unpacked.' + ifile
    vname = _query_vname(ifile=ifile)
    # # old version
    # cmd = ' '.join([
    #     "ncap2 -O -s",
    #     " '%s=float(unpack(%s))' "%(vname, vname),
    #     ifile,
    #     ofile
    # ])
    # _run_shell(cmd)
    cdo('-b f32 copy', ifile, ofile)
def nc_rename(ifile, vname_old=None, vname_new=None, dimname_old=None, dimname_new=None, options='-O -h'):
    '''
    python wrapper of the nco command *ncrename*

    input:
    --------
    \t ifile: \n\t\t input file name
    \t vname_old: \n\t\t old variable name; string, list of strings, or None
    \t vname_new: \n\t\t new variable name; string, list of strings, or None
    \t dimname_old: \n\t\t old dimension names; string, list of strings, or None
    \t dimname_new: \n\t\t new dimension names; string, list of strings, or None
    \t options: \n\t\t ncrename options; string
    return:
    --------
    \t None '''

    cmd = ' '.join(['ncrename', options])

    # variable name change
    if vname_old is None or vname_new is None:
        pass
    else: # vname_old -> vname_new
        if type(vname_old) is str and type(vname_new) is str:
            cmd = ' '.join([cmd, '-v', vname_old + ',' + vname_new])
        elif type(vname_old) is type(vname_new):
            cmd = ' '.join(
                [cmd]
                + [
                    '-v ' + name_old + ',' + name_new
                    for name_old, name_new in zip(vname_old, vname_new)
                ]
            )
        else:
            pass

    # dimension names change
    if dimname_old is None or dimname_new is None:
        pass
    else: # dimname_old -> dimname_new
        if type(dimname_old) is str and type(dimname_new) is str:
            cmd = ' '.join([
                cmd,
                '-v', dimname_old + ',' + dimname_new,
                '-d', dimname_old + ',' + dimname_new,
            ])
        elif type(dimname_old) is type(dimname_new):
            cmd = ' '.join(
                [cmd]
                + [
                    '-v ' + name_old + ',' + name_new
                    for name_old, name_new in zip(dimname_old, dimname_new)
                ]
                + [
                    '-d ' + name_old + ',' + name_new
                    for name_old, name_new in zip(dimname_old, dimname_new)
                ]
            )
        else:
            pass

    # input file
    cmd = ' '.join([cmd, ifile])

    # execute in shell
    _run_shell(cmd)
def nc_rcat(ifiles, ofile, options='-h'):
    '''nco command ncrcat wrapper.

    Parameters:
    -----------
    ifiles: input files as a string or list of strings
    ofile: output file as a string
    options: ncrcat options as a string, default is '-h' '''
    cmd = ' '.join(['ncrcat', options])

    # input files
    if type(ifiles) is str: # input file in form of a string
        cmd = ' '.join([cmd, ifiles])
    else: # input file in form of a list of strings
        cmd = ' '.join([cmd] + ifiles)

    # output file is a string
    cmd = ' '.join([cmd, ofile])

    _run_shell(cmd)

def _query_time(ifile):
    # tname
    with Dataset(ifile) as f:
        vnames = list( f.variables )
    tname_candidates = ['time', 'T']
    tname = [t for t in tname_candidates if t in vnames][0]

    # year_start
    year_start = os.popen('cdo showyear ' + ifile).read()[:10].split()[0]

    # mon_start
    mon_start = os.popen('cdo showmon ' + ifile).read()[:10].split()[0]

    return tname, year_start, mon_start
def nco_remove_attr(ifile, attr, vname):
    '''Delete the attribute associated with variable vname in file.'''
    cmd = ' '.join([
        "ncatted -O -a",
        attr + "," + vname + ",d,,",
        ifile
    ])
    _run_shell(cmd)
nc_remove_attr = nco_remove_attr
def nc_reunit_time(ifile, units_new='months since 1960-01-01', ofile=None):
    '''Change the units of monthly time into the format like 'months since 1960-01-01'. Only apply for monthly data at this point.'''
    tname, year_start, mon_start = _query_time(ifile)
    year_in_units = units_new.split()[-1].split('-')[0]

    # update the time variable values
    tmpfile = ifile + '.tmp'
    cmd = ' '.join([
        "ncap2 -O -s",
        " '%s=array(0.5+(%s-%s)*12+%s-1,1,$%s)' "%(tname, year_start, year_in_units, mon_start, tname),
        ifile,
        tmpfile
    ])
    _run_shell(cmd)

    # update the time units
    cmd = ' '.join([
        "ncatted -O -a",
        "units," + tname + ",m,c,'" + units_new + "'",
        tmpfile
    ])
    _run_shell(cmd)

    # delete the calendar attribute of time
    cmd = ' '.join([
        "ncatted -O -a",
        "calendar," + tname + ",d,,",
        tmpfile
    ])
    _run_shell(cmd)

    # replace ifile by tmpfile
    if ofile is None:
        ofile = ifile
    cmd = ' '.join(['mv', tmpfile, ofile])
    _run_shell(cmd)
def nc_shifttime(ifile, ofile, timeshift):
    '''CDO command shift time, e.g. cdo shifttime,-6hours ifile ofile.'''
    cmd = ' '.join([
        'cdo',
        'shifttime,'+timeshift,
        ifile,
        ofile
    ])
    _run_shell(cmd)
def _nc_split(ifile, obase, option):
    '''CDO operator split<option>'''
    cmd = ' '.join([
        'cdo',
        'split' + option,
        ifile,
        obase
    ])
    _run_shell(cmd)
nc_splitmon = partial(_nc_split, option='mon')
nc_splitday = partial(_nc_split, option='day')
def nc_ydrunmean(ifile, ofile, N=30):
    '''CDO command cdo ydrunmean.'''
    cmd = ' '.join([
        'cdo',
        'ydrunmean,'+str(N),
        ifile,
        ofile
    ])
    _run_shell(cmd)
def nc_ydaysub(ifile1, ifile2, ofile):
    '''CDO command ydaysub.'''
    cmd = ' '.join([
        'cdo',
        'ydaysub',
        ifile1,
        ifile2,
        ofile
    ])
    _run_shell(cmd)
def nc_ydrunanom(ifile, ofile=None, N=30):
    '''Remove smoothed annual cycle of daily data.'''
    if ofile is None:
        ofile = 'ydrunanom.' + ifile
    cmd = ' '.join([
        'cdo',
        'ydaysub',
        ifile,
        '-ydrunmean,' + str(N),
        ifile,
        ofile
    ])
    _run_shell(cmd)
def nc_cal_daily_flux(ifile, ofile, Nmulc=1):
    '''Calculate daily flux based on time integrated data from ERA-Interim.
    Input:
        ifile: the name of the input file
        ofile: the name of the output file
        Nmulc: a number that will be multiplied by the input file (default=1). '''
    if Nmulc == 1:
        cmd = ' '.join([
            'cdo',
            'divc,86400',
            '-daysum',
            ifile,
            ofile
        ])
    else:
        cmd = ' '.join([
            'cdo',
            'mulc,%g'%Nmulc,
            '-divc,86400',
            '-daysum',
            ifile,
            ofile
        ])
    _run_shell(cmd)
def nc_update_units(ifile, units_new):
    '''Change the units of a dataset.'''
    vname = _query_vname(ifile)
    cmd = ' '.join([
        "ncatted -O -a",
        "units," + vname + ",m,c,'" + units_new + "'",
        ifile
    ])
    _run_shell(cmd)
def nc_change_attr(ifile, vname, attr, value):
    '''Change the attribute associated with variable vname in ifile'''
    run_shell('ncatted -O -a', attr+','+vname+',m,c,"'+value+'"',
        ifile)
def nc_set_record_dimension(ifile, ofile=None, dim='time'):
    ''' use nco command to set the record dimension (unlimited), i.e.
    f'ncks -O -h --mk_rec_dmn {dim} {ifile} {ofile}' '''
    if ofile is None:
        ofile = ifile
    cmd = f'ncks -O -h --mk_rec_dmn {dim} {ifile} {ofile}'
    _run_shell(cmd)
