# -*- coding: utf-8 -*-
"""
Created on Thu Jan 15, 2015

@author: Wenchang Yang
"""
from __future__ import print_function

import myplot as mt

from scipy.signal import detrend
import numpy as np
import matplotlib.pyplot as plt

# show power spectrum of x
def show_power_spectrum(x, dt=1, showMax=True, detrending=False, bootstraping=True, Nsample=1000, alpha=0.05, return_data=False, **kwargs):
    '''show power spectrum of x.'''
    if detrending:
        x = detrend(x)
    P = np.abs(np.fft.fft(x))**2
    f = np.fft.fftfreq(x.size,dt)
    L = f>0
    f = f[L]
    P = P[L]
    plt.plot(f,P,**kwargs)
    plt.grid(True)
    plt.xlabel('Frequency')
    plt.ylabel('Power')

    if showMax:
        i = P.argmax()
        tag = '$' + 'f \,=\, ' + '%.2g'%f[i] + '$\n' \
            + '$' + 'T \,=\, ' + '%.2g'%(1.0/f[i]) + '$\n'
        mt.text(1, 1, tag, ha='right', va='top')
    if bootstraping:
        N = x.size
        I = np.random.randint(0,N,size=(Nsample,N))
        X_bs = x[I]
        # if detrending:
        #     X_bs = detrend(X_bs,axis=-1)
        P_bs = np.abs(np.fft.fft(X_bs,axis=-1))**2
        P_bs = P_bs[:,L]
        plt.plot(f,np.percentile(P_bs,100-alpha*50,axis=0),color='gray')
        tag = '$' + r'\alpha \,=\, ' + '%.2g'%alpha + '$\n' \
            + '$' + r'N_{sample} \,=\, ' + '%.2g'%Nsample + '$\n'
        mt.text(0, 1, tag, va='top')
    if return_data:
        return f, P
