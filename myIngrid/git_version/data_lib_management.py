# -*- coding: utf-8 -*-
"""
@author: yang
"""
from urllib2 import urlopen
from .ingrid_operators import *
from . import data_lib
# 
# ---- get the server,e.g. ['http://iridl.ldeo.columbia.edu/expert/']
def get_server(serverName='iri'):
    '''Get the server url in a list, e.g. if serverName is 'iri', then the returned server is 'http://iridl.ldeo.columbia.edu' '''
    server = 'http://iridl.ldeo.columbia.edu'
    s = serverName.lower()
    if s in ['kage','strega']:
        server = server.replace('iridl',s).replace('.edu','.edu:81')
    return server
# 
# ---- get datasets, e.g. ['http://strega.ldeo.columbia.edu:81','CMIP5']
def get_dataset_lib():
    '''return ['cmip5','erai','era-interim','ncep/ncar','ncep/doe','20c']'''
    return ['cmip5','erai','era-interim','ncep/ncar','ncep/doe','20c']
def get_dataset(datasetName):
    '''Get the dataset, e.g. if the datasetName is 'cmip5', then the returned dataset is  'http://strega.ldeo.columbia.edu:81/CMIP5'. '''
    s = datasetName.lower()
    if s in ['cmip5']:
        dataset = get_server('strega') + '/CMIP5'
    elif s in ['erai','era-interim']:
        dataset = get_server('kage') + '/home/.OTHER/.ERAInterim'
    else:
        print 'No dataset has been found for',datasetName
        dataset = None
    return dataset
# 
# -------- get a data chain from a name
def get_url_char_map():
    return {' ':'%20', 
            '{':'%7B',
            '}':'%7D',
            '[':'%5B',
            ']':'%5D',
            '(':'%28',
            ')':'%29'
            }
def get_data(name,includingServer=True):
    '''Get the data full path expressed in a list, e.g. if name is 'gpcp', then the returned data is 'http://iridl.ldeo.columbia.edu/SOURCES/.NASA/.GPCP/.V2p2/.satellite-gauge/.prcp'. '''
    # get the right server
    if hasattr(data_lib,name):
        s = getattr(data_lib,name)
        if s.startswith('/SOURCES'):
            server = get_server('iri')
        # elif 'kage' in s:
        elif s.startswith('/home'):
            server = get_server('kage')
        # elif 'strega' in s:
        elif s.startswith('/OTHER'):
            server = get_server('strega')
        else:
            print 'No server has been found.'
            server = ''
    else:
        print 'No data has been found for',name
        return
        
    # replace the url characters by regular ones, e.g. replace '%5B' by '['
    char_map = get_url_char_map()
    for key,value in char_map.items():
         s = s.replace(value,key)
    
    if includingServer:
        return server + s
    else:
        return s
        
def get_url(data):
    '''Get the corresponding url for the data. The chain can be either a list or a string. \n
    Example: \n
    get_url('gpcp') returns \n
    'http://iridl.ldeo.columbia.edu/SOURCES/.NASA/.GPCP/.V2p2/.satellite-gauge/.prcp' '''

    s = data.lower()
    if s in ['iri','kage','strega']:
        url = get_server(serverName=s)
    elif s in get_dataset_lib():
        url = get_dataset(datasetName=s)
    elif hasattr(data_lib,s):
        url = get_data(name=s)
    else:
        url = data
        
    char_map = get_url_char_map()
    for key,value in char_map.items():
        url = url.replace(key,value)
    return url
# 
# ---- data navigation
def get_items(url):
    htmls = urlopen(url).read()
    htmls = htmls[htmls.find('Datasets and variables'):htmls.find('Last updated:')]
    myitems = []
    for line in htmls.split('\n'):
        head = '<a href=".'
        tail = '/"'
        if head in line and tail in line:
            myitems.append(line[line.find(head)+10:line.find(tail)])
        else:
            pass
    return sorted(myitems)
# 
# ---- ERA-Interim
def get_data_from_erai(vname,freq=None,level=None,year=None):
    server = 'http://kage.ldeo.columbia.edu:81'
    s = server + '/home/.OTHER/.ERAInterim'
    if vname in ['evap','pme','prcp','pr','ps','ts']:
        # surface variables
        level = 'Surface'
        if freq is None:
            freq = 'monthly'
        if vname=='pr' or vname=='prcp':
            vname = 'prcp'
        s += '/' + '/'.join( ['.'+freq, '.'+level, '.'+vname+'.nc', '.'+vname] )
    else:
        # atmosphere interior variables
        if level is None and year is None:
            # monthly data
            freq = 'monthly'
            s += '/' + '/'.join( ['.'+freq, '.PressureLevel_37', '.'+vname+'.nc', '.'+vname] )
        else:
            # daily data
            freq = 'daily'
            if year is not None:
                # by year
                s += '/' + '/'.join( ['.'+freq, '.PressureLevel', '.byYear', 
                    '.'+vname, '.'+vname+'_'+str(year)+'.nc', '.'+vname] )
            else:
                # level is not None, by level
                s += '/' + '/'.join( ['.'+freq, '.PressureLevel', '.byLevel', '.mb'+str(level),
                    '.'+vname+'.nc', '.'+vname] )
    return s    
# 
# -------- cmip5 url
def get_data_from_cmip5(vname=None,scenario=None,model=None,P=None,run='r1i1p1',realm='atmos',tResolution='mon',lonlat2XY=True):
    if vname is None or model is None or scenario is None:
        if vname is not None and scenario is not None:
            s = get_server('strega') + '/' + '/'.join( ['CMIP5','.byScenario'] + ['.'+scenario] + ['.' + realm] + ['.' + tResolution] + ['.' + vname] )
            return s
        else:
            return get_server('strega') + '/CMIP5/.byScenario'
    else:
        s = ( get_server('strega') + '/CMIP5/.byScenario/.' + scenario
                + '/.' + realm + '/.' + tResolution + '/.' + vname + '/.' + model
                + '/.' + run + '/.' + vname )
        
        if P is not None:
            s = s.replace('/.' + run, '/.' + run + '/.' + P)
        if lonlat2XY:
            s += renameGrid('lon','X') + renameGrid('lat','Y')
        return s
def get_models_from_cmip5(vname,scenario,realm='atmos',tResolution='mon'):
    url = get_server('strega') + '/CMIP5/.byScenario/.' + scenario + '/.' + realm \
                + '/.' + tResolution + '/.' + vname
    models = get_items(url)
    return models
def get_runs_from_cmip5(vname,scenario,model,realm='atmos',tResolution='mon'):
    url = get_server('strega') + '/CMIP5/.byScenario/.' + scenario + '/.' + realm \
                + '/.' + tResolution + '/.' + vname + '/.' + model
    runs = get_items(url)
    return runs