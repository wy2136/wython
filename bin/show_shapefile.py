#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Fri Mar  4 11:26:55 EST 2022
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
if len(sys.argv)>1:
    ifiles = sys.argv[1:]
    for ifile in ifiles:
        shdf = salem.read_shapefile(ifile)
        print(f'**{ifile}**')
        print(shdf)
        print()
        print('**first record**')
        print(shdf.iloc[0,:])
        print()
        print('**columns**')
        print(shdf.columns)
        print()
else:
    print(f'please provide input shape files:')
    print(f'    {os.path.basename(__file__)} shapfile1,[shapefile2,...]')
 
 
if __name__ == '__main__':
    #from wyconfig import * #my plot settings
    
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
    
