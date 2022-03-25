#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Tue Aug 20 15:22:18 EDT 2019
import xarray as xr, numpy as np, matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm, ListedColormap
from matplotlib.collections import LineCollection

def single_track_plot(lonvec, latvec, vmvec, ax=None, lw=0.5, alpha=0.6, cmap=None):
    '''plot TC a TC track with varied colors indicating wind spead.'''
    if ax is None:
        ax = plt.gca()
    
    # create segments for the LineCollection
    L = ~np.isnan(lonvec)
    x = lonvec[L]
    y = latvec[L]
    vm = vmvec[L]
    vm = (vm[:-1] + vm[1:])/2.0
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    
    if cmap is None:
        # colormap from: 
        # https://upload.wikimedia.org/wikipedia/commons/6/6f/Tropical_cyclones_1945_2006_wikicolor.png
        c = ListedColormap(np.array([(114, 185, 249),
                                    (122, 246, 244),
                                    (255, 254, 209),
                                    (252, 231, 134),
                                    (247, 195, 90),
                                    (241, 148, 64),
                                    (238, 107, 103)])/255.0 )
    else:
        c = plt.get_cmap(cmap, 7)
    levels = [0, 17, 33, 43, 50, 58, 70, 100]
    norm = BoundaryNorm(levels, c.N)
    
    # LineCollection objects
    lc = LineCollection(segments, cmap=c, norm=norm)
    lc.set_array(vm)
    lc.set_linewidth(lw)
    lc.set_alpha(alpha)

    lines = ax.add_collection(lc)
    ax.autoscale()
    
    return lines

def trackplot(ds, **kwargs):
    '''plot TC a TC track with varied colors indicating wind spead.
    kwargs include: 
        ax(=plt.gca()), 
        lw(=0.5), 
        alpha(=0.5). 
        
    **usage**
        lines = trackplot(ds.isel(year=slice(0,10)), alpha=1)
        plt.colorbar(lines.isel(year=0, storm=0).item())
    '''    
    add_colorbar = kwargs.pop('add_colorbar', True)
    ax = kwargs.pop('ax', plt.gca())

    #simple version track plot, fast speed
    ezplot = kwargs.pop('ezplot', False)
    if ezplot:
        ax.plot(ds.lon.values.flat, ds.lat.values.flat, **kwargs)    
        return

    #complex version track plot, slow speed
    lines = xr.apply_ufunc(single_track_plot,
                          ds.lon, ds.lat, ds.windmax,
                          input_core_dims=[['stage'], ['stage'], ['stage']],
                          vectorize=True,
                          kwargs=kwargs)
    ax.autoscale()
    if add_colorbar:
        #plt.colorbar(lines.isel(year=0, storm=0).item())
        plt.colorbar(lines.values.flat[0])
    
    return lines
