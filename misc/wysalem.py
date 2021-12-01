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

    tt.check(f'**Done**')
    plt.show()
    
