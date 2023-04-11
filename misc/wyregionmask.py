#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Fri Sep  9 10:52:45 EDT 2022
if __name__ == '__main__':
    import sys
    from misc.timer import Timer
    tt = Timer('start ' + ' '.join(sys.argv))
import sys, os.path, os, glob, datetime
import xarray as xr, numpy as np, pandas as pd, matplotlib.pyplot as plt
#more imports
import regionmask
#
if __name__ == '__main__':
    tt.check('end import')
#
#start from here
def make_regions(lon, lat):
    '''make regions based on input lon/lat vecs'''
    name = 'myRegions'
    names = ['myRegion',]
    abbrevs = ['myReg',]
    outlines = [[(x, y) for x,y in zip(np.array(lon), np.array(lat))],]
    numbers = np.arange(len(names))
    # Regions_cls was replaced by Regions since version 0.5.0 of regionmask
    #bs = regionmask.Regions_cls(name=name,
    regions = regionmask.Regions(name=name,
                                numbers=numbers,
                                names=names,
                                abbrevs=abbrevs,
                                outlines=outlines)
    return regions

def flag_region(da, lon, lat):
    """given polygon defined by lon/lat vecs, generate flags (0s) of lon/lat grids defined within da"""
    regions = make_regions(lon, lat)
    return regions.mask(da)

def where_region(da, lon, lat):
    """mask da so that only grids within plogon (defined by lon/lat vecs) are kept"""
    return da.where(flag_region(da, lon, lat)==0)
 
 
if __name__ == '__main__':
    #from wyconfig import * #my plot settings
    
    #savefig
    if 'savefig' in sys.argv or 's' in sys.argv:
        figname = __file__.replace('.py', f'.png')
        if 'overwritefig' in sys.argv or 'o' in sys.argv:
            wysavefig(figname, overwritefig=True)
        else:
            wysavefig(figname)
    tt.check(f'**Done**')
    print()
    if 'notshowfig' in sys.argv:
        pass
    else:
        plt.show()
    
