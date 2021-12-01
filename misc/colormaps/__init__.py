#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Sun Apr 26 14:04:41 EDT 2020
#import sys, os.path, os, datetime
#import xarray as xr, numpy as np, pandas as pd
#import matplotlib.pyplot as plt
#more imports
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
#
def RGBToPyCmap(rgbdata):
    nsteps = rgbdata.shape[0]
    stepaxis = np.linspace(0, 1, nsteps)

    rdata=[]; gdata=[]; bdata=[]
    for istep in range(nsteps):
        r = rgbdata[istep,0]
        g = rgbdata[istep,1]
        b = rgbdata[istep,2]
        rdata.append((stepaxis[istep], r, r))
        gdata.append((stepaxis[istep], g, g))
        bdata.append((stepaxis[istep], b, b))

    mpl_data = {'red':   rdata,
                 'green': gdata,
                 'blue':  bdata}

    return mpl_data

def register_cmap(name, cmap_data):
    _cmap_data = np.array(cmap_data)
    # register colormap
    mpl_data = RGBToPyCmap(_cmap_data)
    """
    #old version
    plt.register_cmap(name=cmap_name, data=mpl_data, lut=_cmap_data.shape[0])
    # register colormap of reversed version
    mpl_data_r = RGBToPyCmap(_cmap_data[::-1,:])
    plt.register_cmap(name=cmap_name+'_r', data=mpl_data_r, lut=_cmap_data.shape[0])
    """
    #new version: 2021-06-03 by wy
    cmap = LinearSegmentedColormap(name, mpl_data, _cmap_data.shape[0])
    plt.register_cmap(cmap=cmap)
    plt.register_cmap(cmap=cmap.reversed())

    print(f'[registered colormaps]: {name} and {name}_r')

    

cmap_name = 'tc'
if cmap_name not in plt.colormaps():
    from .tc import _tc_data as _cmap_data
    register_cmap(cmap_name, _cmap_data)

cmap_name = 'turbo'
if cmap_name not in plt.colormaps():
    from .turbo import _turbo_data as _cmap_data
    register_cmap(cmap_name, _cmap_data)

cmap_name = 'parula'
if cmap_name not in plt.colormaps():
    from .parula import _parula_data as _cmap_data
    register_cmap(cmap_name, _cmap_data)

if __name__ == '__main__':
    t = np.linspace(0, np.pi*2, 100)
    z = np.sin(t.reshape(t.size,1)) * np.cos(t.reshape(1, t.size))
    def myplot(mycmap):
        plt.figure()
        plt.pcolormesh(z, cmap=mycmap)
        plt.colorbar()
        plt.title(f'{mycmap} colormap')

    #tc
    myplot('tc')

    # parula
    plt.figure()
    plt.pcolormesh(z, cmap='parula')
    plt.colorbar()
    plt.title('Parula colormap (new version: Matlab 2017a and later)')

    # turbo
    plt.figure()
    plt.pcolormesh(z, cmap='turbo')
    plt.colorbar()
    plt.title('turbo colormap from Google AI')

    plt.show()
