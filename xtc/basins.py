#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Sat May 25 23:22:27 EDT 2019
import regionmask
import xarray as xr, numpy as np
from matplotlib import path

def tc_basins(latN=90, latS=-90):
    '''use regionmask to create 8 TC basins'''
    #latN = 90 # north boundary lat
    #latS = -90 # south bounday lat
    name = 'TCBasins'
    names = ['North Atlantic', 'East Pacific', 'West Pacific', 'North Indian',
            'South Indian', 'Australia', 'South Pacific', 'South Atlantic']
    abbrevs = ['NA', 'EP', 'WP', 'NI',
              'SI', 'AU', 'SP', 'SA']
    outlines = [( (295, 0), (260, 20), (260, latN), (360, latN), (360, 0) ),
                ( (200, 0), (200, latN), (260, latN), (260, 20), (295, 0) ),
                ( (105, 0), (105, latN), (200, latN), (200, 0) ),
                ( (30, 0), (30, latN), (105, latN), (105, 0) ),
                ( (30, 0), (30, latS), (105, latS), (105, 0) ),
                ( (105,0), (105, latS), (165, latS), (165, 0) ),
                ( (165, 0), (165, latS), (290, latS), (290, 0) ),
                ( (290, 0), (290, latS), (360, latS), (360, 0) ),
               ]
    numbers = np.arange(len(names))
    # Regions_cls was replaced by Regions since version 0.5.0 of regionmask
    if hasattr(regionmask, 'Regions'):
        Regions = regionmask.Regions
    else:
        Regions = regionmask.Regions_cls
        print('**old versions of regionmask is used: regionmask.Regions_cls**')
    #bs = regionmask.Regions_cls(name=name,
    #bs = regionmask.Regions(name=name,
    bs =             Regions(name=name,
                                numbers=numbers,
                                names=names,
                                abbrevs=abbrevs,
                                outlines=outlines)
    return bs

def tracks_in_basin(ds, basin):
    '''Get the basin bool mask for the tracks dataset.
    **input**:
        ds: tracks dataset;
        basin: basin tag, e.g. "NA" for North Atlantic. 
    **return**:
        in_basin: DataArray of basin mask (bool values)'''
#     ds = xtc.tc_tracks('CTL1860_noleap_tigercpu_intelmpi_18_576PE', years=range(1,11))
#     basin = 'NA'
    # create basin_domain given basin tag, e.g. 'NA' (North Atlantic)
    basins = tc_basins()
    basin_index = basins.map_keys(basin)
    basin_domain = path.Path(basins.coords[basin_index])
    
    # create DataArray of lon/lat pairs
    lon = ds.lon.stack(i_stack=ds.lon.dims)
    lat = ds.lat.stack(i_stack=ds.lat.dims)
    lonlat = xr.concat([lon, lat], dim='lonlat').transpose()
    in_basin = lon.copy().astype('bool') # DataArray to hold the result
    
    # get the basin bool mask for all the tracks
    in_basin.data = basin_domain.contains_points(lonlat)
    in_basin = in_basin.unstack() # unstack to recover the original shape
    
    return in_basin

def mask_basin(da, basin):
    '''mask the input DataArray da by a given basin (e.g. 'NA'). da has lon/lat coordinates'''
    bs = tc_basins()
    return da.where( bs.mask(da) == bs.map_keys(basin) )
