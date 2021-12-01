#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Mon Feb  1 16:20:20 EST 2021
if __name__ == '__main__':
    from misc.timer import Timer
    tt = Timer(f'start {__file__}')
import sys, os.path, os, glob
import xarray as xr, numpy as np, pandas as pd
#import matplotlib.pyplot as plt
#more imports
import xfilter
#
if __name__ == '__main__':
    tt.check('end import')
#
#start from here
 
 
if __name__ == '__main__':
    from wyconfig import * #my plot settings
    np.random.seed(0)
    da = xr.DataArray(np.random.randn(100), dims='day', name='Ta', attrs={'units': 'degC'})

    fig, ax = plt.subplots(1, 1)
    da.plot(label='raw', color='k', ax=ax)
    da.filter.lowpass(1/10, padtype='constant').plot(ax=ax, label='constant pad')
    da.filter.lowpass(1/10, padtype='odd').plot(ax=ax, label='odd pad')
    da.filter.lowpass(1/10, padtype='even').plot(ax=ax,label='even pad')
    da.filter.lowpass(1/10, method='gust').plot(ax=ax,label='Gustafsson method')
    ax.legend(loc='lower right')    


    plt.show()
    tt.check(f'**Done**')
