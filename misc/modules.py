# -*- coding: utf-8 -*-
"""
Created on Tue Nov 11, 2014

@author: yang
"""
from __future__ import print_function

import os,os.path
import datetime
# import csv
_dirname, = os.path.dirname(os.path.realpath(__file__)),
# print dirname
cityGeoFile = os.path.join(_dirname,'GeoLiteCity-Location.csv')
# print cityGeoFile


# module creation
def mcreate(moduleName):
    """created a customized module file."""
    # parameters
    if not moduleName.endswith('.py'):
        moduleName = moduleName+'.py'
    moduleNameFull = os.path.join(_dirname,moduleName)
    now = datetime.datetime.now()
    today = now.strftime('%a %b %d, %Y')

    if not os.path.exists(moduleNameFull):
        # add some information at the beginning of the module file
        with open(moduleNameFull,'w') as f:
            # f.write('# -*- coding: utf-8 -*-\n')
            f.write('"""\n')
            f.write('Created on ' + today + '\n')
            # f.write(' \n')
            f.write('@author: Wenchang Yang (yang.wenchang@uci.edu) \n')
            f.write('"""\n')
            print ('A new module file has been created:',moduleNameFull)
    else:
        print ('The module exists at:',moduleNameFull)
    os.system('open '+ moduleNameFull)
# path navigation
def goto(pathShortName=None):
    '''open frequently used directories'''
    if os.uname()[1]=='Wenchang-Yangs-MacBook-Pro.local':
        pathDict = {'proj':'~/Dropbox/Work/myProjects/',
                'python':'~/Dropbox/Work/myPython/',
                'config':'~/Dropbox/Work/myConfigs/'}
    elif os.uname()[1]=='engey':
        pathDict = {'proj': '~/projs',
                    'data': '~/data',
                    'model': '~/models'}
    else:
        pathDict = None
    if pathShortName is None:
        print (pathDict)
    else:
        if os.uname()[1]=='engey':
            openCommand = 'xdg-open '
        else:
            openCommand = 'open '
        os.system(openCommand + pathDict[pathShortName])

# module edit
def medit(module):
    '''edit the source file of a module'''
    filename = module.__file__
    if filename.endswith('.pyc'):
        filename = filename[:-1]
    if os.uname()[1]=='engey':
        os.system('vi ' + filename)
    else:
        os.system('open '+filename)
def mgoto(module):
    '''goto the directory of a module'''
    filename = module.__file__
    dirname = os.path.dirname(filename)
    if os.uname()[1]=='engey':
        os.system('xdg-open '+ dirname)
    else:
        os.system('open '+dirname)
#

# find the longitude and latitude of a city
# def find_lonlat(city):
#     '''Get the longitude and latitude of a city given its name.'''
#     with open(cityGeoFile) as f:
#         reader = csv.reader(f)
#         for row in reader:
#             if city in row:
#                 lon = row[6]
#                 lat = row[5]
#                 break
#     return lon,lat
