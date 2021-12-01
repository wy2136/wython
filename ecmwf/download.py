# Follow the instructions from https://software.ecmwf.int/wiki/display/WEBAPI/Access+ECMWF+Public+Datasets#AccessECMWFPublicDatasets-key
# before using this package.
#
# Written by Wenchang Yang (yang.wenchang@uci.edu)
#
from __future__ import print_function
import os, sys
from calendar import monthrange
from ecmwfapi import ECMWFDataServer
server = ECMWFDataServer()

# def _get_script_path():
#     return os.path.dirname(os.path.realpath(sys.argv[0]))
def download_data(data_dict, year, month, ofile, redownload=False):
    ''' An example of data_dict is:
        data_dict = {
        "class": "ei",
        "dataset": "interim",
        "date": "1979-01-01/to/1979-01-31",
        "expver": "1",
        "grid": "2/2",
        "levelist": "1/2/3/5/7/10/20/30/50/70/100/125/150/175/200/225/250/300/350/400/450/500/550/600/650/700/750/775/800/825/850/875/900/925/950/975/1000",
        "levtype": "pl",
        "param": "130.128",
        "step": "0",
        "stream": "oper",
        "target": "CHANGEME",
        "time": "00/06/12/18",
        "type": "an",
    }'''

    # set the date range
    if month is None: # download the data of the whole year
        date0 = '-'.join([str(year), '01', '01'])
        date1 = '-'.join([str(year), '12', '31'])
    else: # download the data of a month
        _, dd = monthrange(year, month)
        date0 = '-'.join([str(year), str(month).zfill(2), '01'])
        date1 = '-'.join([str(year), str(month).zfill(2), str(dd)])
    data_dict['date'] = date0 + '/to/' + date1

    # set the format as netcdf
    data_dict['format'] = "netcdf"

    # set the target
    if month is None: # download data of a year
        data_dict['target'] = '.'.join([ofile, str(year), 'nc'])
    else: # download data of a month
        data_dict['target'] = '.'.join([ofile, str(year), str(month).zfill(2), 'nc'])

    # download the data
    if os.path.exists(data_dict['target']):
        print('!!!!', data_dict['target'], 'already exists.\n')
        if redownload:
            print('#### Redownloading data ...\n')
            server.retrieve(data_dict)
    else:
        server.retrieve(data_dict)

def download_monthly_data(data_dict, year, ofile, redownload=False):
    ''' An example of data_dict is:
        data_dict = {
        "class": "e2",
        "dataset": "era20c",
        "date": "19000101/19000201/19000301/19000401/19000501/19000601/19000701/19000801/19000901/19001001/19001101/19001201",
        "expver": "1",
        "grid": "1/1",
        "format": "netcdf",
        "levtype": "sfc",
        "param": "31.128",
        "stream": "moda",
        "type": "an",
        "target": "CHANGEME",
    }'''

    # set the date range
    data_dict['date'] = '/'.join(['{year}{month:02d}01'.format(year=year,
        month=i) for i in range(1,13)])

    # set the format as netcdf
    data_dict['format'] = "netcdf"

    # set the target
    data_dict['target'] = '{ofile}.{year}.nc'.format(ofile=ofile, year=year)

    # download the data
    if os.path.exists(data_dict['target']):
        print('[!Alread Exists]', data_dict['target'])
        if redownload:
            print('[Redownloading data] ...\n')
            server.retrieve(data_dict)
    else:
        server.retrieve(data_dict)
