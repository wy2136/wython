# -*- coding: utf-8 -*-
"""
Created on Tue Apr 15 15:57:01 2014

@author: yang
"""
from __future__ import print_function

import h5py
import numpy as np

def open(fileName='data.h5'):
    return h5py.File(fileName)
# 
def dump(fileName='data.h5', group=None):
    '''Show what hdf5 file contains given fileName and group.'''
    with h5py.File(fileName,'r') as f:
        if group is None: # only show the first-level data names
            print ('fileName: ' + fileName + ': ')
            print('-'*10)
            print('Datasets/groups:')
            for name in f:
                if isinstance(f[name],h5py._hl.group.Group):
                    print (' '*4 + name + '/')
                else:
                    print (' '*4 + name)
            print('-'*10)
            print ('fileName: ' + fileName + ': ')
        else: # show the data names with the group
            print(fileName)
            print('-'*10)
            print(group+'/')
            for name in f[group]:
                if isinstance(f[group + '/' + name],h5py._hl.group.Group):
                    print (' '*4 + name + '/')
                else:
                    print (' '*4 + name)
            print(group+'/')
            print('-'*10)
            print(fileName)
#
def list(fileName='data.h5', group=None):
    with h5py.File(fileName,'r') as f:
        if group is None:
            theList = [item for item in f]
        else:
            theList = [item for item in f[group]]
    return theList
# 
def look(dataName, fileName='data.h5'):
    with h5py.File(fileName) as f:
        print('shape:', f[dataName].shape)
        for key, value in f[dataName].attrs.items():
            if type(value) is str:
                value = value.split()
            print(key, '(len: %g)' % len(value))
        print('\n')
# 
def save(data, dataName='data', fileName='data.h5'):
    with h5py.File(fileName) as f:
        if dataName in f:
            f[dataName][:] = data
        else:
            f.create_dataset(dataName,data=data)
#
def load(dataName,fileName='data.h5'):
    with h5py.File(fileName,'r') as f:
        data = f[dataName][:]
    return data
def load_ensemble(ensemble, fileName='data.h5'):
    members = list(fileName=fileName, group=ensemble)
    data = []
    for member in members:
        data.append(
            load(dataName=ensemble+'/'+member, fileName=fileName)
        )
    data = np.array(data)
    return data, members
#
def set_attrs(dataName,key,value,fileName='data.h5'):
    with h5py.File(fileName) as f:
        f[dataName].attrs[key] = value
# 
def get_attrs(dataName,key,fileName='data.h5'):
    with h5py.File(fileName) as f:
        value = f[dataName].attrs[key]
    return value
# 
def delete(dataName,fileName='data.h5'):
    with h5py.File(fileName) as f:
        dataFullName = dataName
        f[dataFullName][:] = 0
    
    


