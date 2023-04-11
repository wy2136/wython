#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Thu Mar  2 09:40:49 EST 2023
if __name__ == '__main__':
    import sys,os
    from misc.timer import Timer
    tt = Timer(f'[{os.getcwd()}] start ' + ' '.join(sys.argv))
import sys, os.path, os, glob, datetime
#import xarray as xr, numpy as np, pandas as pd, matplotlib.pyplot as plt
#more imports
#from misc import get_kws_from_argv
from .modelout import get_modelout_data, update_modelout_data
#
if __name__ == '__main__':
    tt.check('end import')
#
#start from here
 
 
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
    if 'notshowfig' in sys.argv or 'n' in sys.argv:
        pass
    else:
        if 'plt' in globals(): plt.show()
    
