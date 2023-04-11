#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Fri Mar  4 10:35:28 EST 2022
if __name__ == '__main__':
    import sys
    from misc.timer import Timer
    tt = Timer('start ' + ' '.join(sys.argv))
import sys, os.path, os, glob, datetime
import xarray as xr, numpy as np, pandas as pd, matplotlib.pyplot as plt
#more imports
import salem
#
if __name__ == '__main__':
    tt.check('end import')
#
#start from here
#ifile = 'gadm40_BRA_1.shp'
ifile = [ifile for ifile in os.listdir('.') if ifile.endswith('.shp')][0]
shdf = salem.read_shapefile(ifile)

if __name__ == '__main__':
    from wyconfig import * #my plot settings
    from geoplots import mapplot
    fig, ax = plt.subplots(figsize=(6,5))
    shdf.plot(ax=ax)
    for ii in range(shdf.index.size): 
        p = shdf.loc[ii, 'geometry'].centroid
        x, y = p.x, p.y
        #plt.text(x, y, str(ii), ha='center', va='center', color='lightgray', fontsize='x-small')
        try:
            name = shdf.loc[ii, 'NAME_1']
            ax.text(x, y, f'{ii:02d}_{name}', ha='center', va='center', color='lightgray', fontsize='xx-small')
        except:
            pass
    try: 
        ax.set_title( shdf.loc[0, 'COUNTRY'] )
    except:
        pass
    #ax.set_xlabel('lon')
    #ax.set_ylabel('lat')
    mapplot()
    ax.set_aspect('equal')
    
    #savefig
    if len(sys.argv)>1 and 'savefig' in sys.argv[1:]:
        figname = __file__.replace('.py', f'.png')
        if 'overwritefig' in sys.argv[1:]:
            wysavefig(figname, overwritefig=True)
        else:
            wysavefig(figname)
    tt.check(f'**Done**')
    print()
    plt.show()
