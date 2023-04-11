#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Fri May 15 13:45:34 EDT 2020
if __name__ == '__main__':
    from misc.timer import Timer
    tt = Timer(f'start {__file__}')
import sys, os.path, os, glob
import xarray as xr, numpy as np, pandas as pd
#import matplotlib.pyplot as plt
#more imports
import salem
#
if __name__ == '__main__':
    tt.check('end import')
    
#start from here
def get_world_shape(cntry_names=None):
    '''return GeoDataFrame of countries given country names.'''
    dfgeo = salem.read_shapefile(salem.get_demo_file('world_borders.shp'))
    if cntry_names is None: 
        return dfgeo
    elif isinstance(cntry_names, str):
        if cntry_names.lower() == 'china':
            return dfgeo[ dfgeo['CNTRY_NAME'].isin(['China', 'Taiwan']) ]
        else:
            return dfgeo[ dfgeo['CNTRY_NAME']==cntry_names ]
    else:
        return dfgeo[ dfgeo['CNTRY_NAME'].isin(cntry_names) ]

 
 
if __name__ == '__main__':
    from wyconfig import *
    from geoplots import xticks2lon, yticks2lat
    """
    print('world')
    shdf = get_world_shape()
    print(shdf)
    shdf.plot()

    print('China')
    shdf = get_world_shape('China')
    print(shdf)
    shdf.plot()

    print('United States')
    shdf = get_world_shape('United States')
    print(shdf)
    shdf.plot()
    """
    if len(sys.argv)>1:
        cntry_names = [s for s in sys.argv[1:] if s not in ('savefig',)]
        if len(cntry_names)<1:
            shdf = get_world_shape()
        else:
            shdf = get_world_shape(cntry_names)
    else:
        shdf = get_world_shape()
    shdf.plot()
    ax = plt.gca()
    ax.set_aspect('equal')
    xticks2lon()
    yticks2lat()

    if 'savefig' in sys.argv:
        figname = 'wymap.png'
        wysavefig(figname)
    tt.check(f'**Done**')
    plt.show()
    
