#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Wed Aug  7 12:41:13 EDT 2019
if __name__ == '__main__':
    from misc.timer import Timer
    tt = Timer(f'start {__file__}')
import os.path, sys, os, datetime, glob
print('[imported]: os.path, sys, os, datetime, glob')

import xarray as xr, numpy as np, pandas as pd, matplotlib as mpl
print(f'[imported]: xarray({xr.__version__}) as xr, numpy({np.__version__}) as np, pandas({pd.__version__}) as pd, matplotlib({mpl.__version__}) as mpl')

# matplotlib setting
import matplotlib.pyplot as plt
print('[imported]: import matplotlib.pyplot as plt')
#from wyconfig import *
import wyconfig
from wyconfig import constrained_layout_on, constrained_layout_off
from matplotlib.pyplot import plot, figure, close, show
print('[imported]: from matplotlib.pyplot import plot, figure, close, show')
plt.ion()
print('[executed]:', 'plt.ion()')

if __name__ == '__main__':
    tt.check('**done**')
