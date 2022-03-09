#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Sun May 17 15:10:48 EDT 2020
if __name__ == '__main__':
    from misc.timer import Timer
    tt = Timer(f'start {__file__}')
import sys, os.path, os, glob
#import xarray as xr, numpy as np, pandas as pd
#import matplotlib.pyplot as plt
#more imports
#
if __name__ == '__main__':
    tt.check('end import')
    
#start from here
def tracks_in_region(ds, region):
    '''Get the basin bool mask for the tracks dataset.
    **input**:
        ds: tracks dataset;
        region: Nx2 array as input for matplotlib.path.Path. 
            One example is boundary coords from shapefile: 
                shdf = salem.read_shapefile(ishapefile)
                region = np.array( shdf.geometry[0].boundary.coords )
    **return**:
        in_region: DataArray of in in_region mask (bool values)'''
#     ds = xtc.tc_tracks('CTL1860_noleap_tigercpu_intelmpi_18_576PE', years=range(1,11))
#     basin = 'NA'
    # create regionPath given Nx2 region array
    regionPath = path.Path(region)
    
    # create DataArray of lon/lat pairs
    lon = ds.lon.stack(i_stack=ds.lon.dims)
    lat = ds.lat.stack(i_stack=ds.lat.dims)
    lonlat = xr.concat([lon, lat], dim='lonlat').transpose()
    in_region = lon.copy().astype('bool') # DataArray to hold the result
    
    # get the region bool mask for all the tracks
    in_region.data = regionPath.contains_points(lonlat)
    in_region = in_region.unstack() # unstack to recover the original shape
    
    return in_region
 
if __name__ == '__main__':
    tt.check(f'**Done**')

