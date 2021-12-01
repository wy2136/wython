# -*- coding: utf-8 -*-
"""
Created on Mon Jul 28  2014

@author: yang
"""

from .stats import p2r, corr_mon_lags
import myplot as mt

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import detrend
from scipy.stats import linregress

# show the linear regression of y by x.
def show_regress(x,y,Ndigits=None,**kwargs):
    '''Old name: add_regress.'''
    b,a,r,p,e = linregress(x, y)
    plt.plot(x, x*b+a, **kwargs)
    if Ndigits is None:
        theText = 'b = ' + '%.2g'%b + '\n' \
                + 'a = ' + '%.2g'%a + '\n' \
                + 'r = ' + '%.2g'%r + '\n' \
                + 'p = ' + '%.2g'%p + '\n' \
                + 'e = ' + '%.2g'%e + '\n'
    else:
        N = Ndigits
        theText = 'b = ' + str(round(b,N)) + '\n' \
                + 'a = ' + str(round(a,N)) + '\n' \
                + 'r = ' + str(round(r,N)) + '\n' \
                + 'p = ' + str(round(p,N)) + '\n' \
                + 'e = ' + str(round(e,N)) + '\n'
    plt.text(.02,.98,theText,
            transform=plt.gca().transAxes,
            verticalalignment='top')
#
# Shows the cross correlation between x1 and x2.
def show_xcorr(x1,x2=None,showMax=False,detrending=False, marker='o', **kwargs):
    '''Shows the cross correlation between x1 and x2, with the x-axis showing the time that x1 lags x2.'''
    if x2 is None:
        x2 = x1
    if detrending:
        x1 = detrend(x1)
        x2 = detrend(x2)
    x1 = (x1 - x1.mean())/x1.std()
    x2 = (x2 - x2.mean())/x2.std()
    lags,cc,line,b = plt.xcorr(x1,x2,usevlines=False,
        marker=marker, linestyle='-', **kwargs)
    plt.grid(True)
    plt.axhline(0,color='gray',ls='--')
    plt.xlabel('Lags')
    plt.ylabel('Correlation')

    # show significant r
    N = x1.size
    df = N - np.abs(lags) - 2
    r = p2r(p=0.05, df=df, twoside=True)
    plt.plot(lags,r,color='gray', ls='--')
    plt.plot(lags,-r,color='gray', ls='--')

    if showMax:
        i = np.abs(cc).argmax()
        tag = ('$' + 'Lags \,=\, ' + '%.2g'%lags[i] + '$\n'
            + '$' + 'r \,=\, ' + '%.2g'%cc[i] + '$\n')
        # mt.tag(tag,'upper right')
        mt.text(1, 1, ha='right', va='top')
    return lags,cc
def show_corr_mon_lags(*args, **kw):
    # show_zero = kw.pop('show_zero', False)
    plot_kw = kw.pop('plot_kw', {})
    r, lags, mon, r_p = corr_mon_lags(*args, **kw)

    # contourf
    # plt.contourf(lags, mon, r, levels=np.arange(-1, 1.01, 0.1), cmap='bwr')
    # contour
    # cs = mt.contour(lags, mon, r, show_zero=show_zero, levels=np.arange(-1.0,1.01,0.1), **kw_contour)
    mt.xyplot(r, lags, mon, levels=np.arange(-1, 1.01, 0.1),
        plot_type='contourf+', **plot_kw)

    plt.yticks(
        np.arange(1,13),
        ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    )
    plt.xticks(lags[::2])
    plt.grid(True)
    plt.axvline(0, color='gray')
    plt.xlabel('Lags (months)')
    plt.gca().invert_yaxis(); plt.draw()
    # return cs
