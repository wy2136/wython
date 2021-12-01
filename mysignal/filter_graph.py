# -*- coding: utf-8 -*-
"""
Created on Thu Jan 15, 2015
 
@author: Wenchang Yang 
"""
from __future__ import print_function

from .filter import \
    _lowpass_ba, _highpass_ba, _bandpass_ba, \
    _lowpass_ba_lanczos, _highpass_ba_lanczos

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import freqz

# ---- general filter
def show_response(b=None,a=1.0,fbfilt=False, label=None, xtick_labels_T=False, return_data=False):
    '''Show the signal response function in frequency space given the coefficients of a and b. '''
    # parameters
    if b is None:
        b = [1./4,]*4
    b = np.array(b)
    a = np.array(a)
    print ('b = ',b)
    print ('a = ',a)
    print ('fbfilt is ',fbfilt)
    
    # data
    w,h = freqz(b,a)
    xx = w/w[-1]/2
    if fbfilt:
        yy = abs(h**2)
    else:
        yy = abs(h)
    
    # plot
    plt.plot(xx, yy, label=label)
    plt.xlim(0,0.5)
    plt.axhline(1,color='gray', ls='--')
    plt.title('b = ' + str(b.round(2)) + '; a = ' + str(a.round(2)), y=1.02)
    # xtick labels as periods
    if xtick_labels_T:
        T = np.array(
            [2, 4, 10, 100]
        )
        f = 1./T
        xtick_labels = [str(i) for i in T]
        plt.xticks(f, xtick_labels)
        plt.xlabel('$T/T_s$')
        plt.ylabel('$|R(T/T_s)|$')
    else:
        plt.xlabel('$f/f_s$')
        plt.ylabel('$|R(f/f_s)|$')
    
    # return data
    if return_data:
        return xx, yy
# 
# ---- Butterworth filter
def show_response_lp(lowcut=0.25,fs=1.0,order=2, fbfilt=True,label=None, xtick_labels_T=False, return_data=False):
    '''Show the lowpass (Butterworth) response function.'''
    # params
    print ('lowcut = ',lowcut)
    print ('fs = ',fs)
    print ('order = ',order)
    
    # data
    b,a = _lowpass_ba(lowcut=lowcut,fs=fs,order=order)
    
    # plot
    xx, yy = show_response(b, a, fbfilt=fbfilt, label=label, xtick_labels_T=xtick_labels_T, return_data=True)
    plt.title('$f_{low}/f_s = $ $%.2g$' % (lowcut/fs), y=1)
    plt.axvline(lowcut,color='gray', ls='--')
    
    # return data
    if return_data:
        return xx, yy

def show_response_hp(highcut=0.25,fs=1.0,order=2, fbfilt=True,label=None, xtick_labels_T=False, return_data=False):
    '''Show the highpass (Butterworth) response function.'''
    # params
    print ('highcut = ',highcut)
    print ('fs = ',fs)
    print ('order = ',order)
    print ('fbfilt is ',fbfilt)
    
    # data
    b,a = _highpass_ba(highcut=highcut,fs=fs,order=order)
    
    # plot
    xx, yy = show_response(b, a, fbfilt=fbfilt, label=label, xtick_labels_T=xtick_labels_T, return_data=True)
    plt.title('$f_{high}/f_s = $ $%.2g$' % (highcut/fs), y=1)
    plt.axvline(highcut,color='gray', ls='--')
    
    # return data
    if return_data:
        return xx, yy
def show_response_bp(lowcut=0.125,highcut=0.375,fs=1.0,order=2, fbfilt=True,label=None, xtick_labels_T=False, return_data=False):
    '''Show the bandpass (Butterworth) response function. '''
    # params
    print ('lowcut = ',lowcut)
    print ('highcut = ',highcut)
    print ('fs = ',fs)
    print ('order = ',order)
    print ('fbfilt is ',fbfilt)
    
    # data
    b,a = _bandpass_ba(lowcut=lowcut,highcut=highcut,fs=fs,order=order)
    
    # plot
    xx, yy = show_response(b, a, fbfilt=fbfilt, label=label, xtick_labels_T=xtick_labels, return_data=True)
    plt.title('$f_{high}/f_s = $ $%.2g$, $f_{high}/f_s = $ $%.2g$' % (lowcut/fs, highcut/fs), y=1)
    plt.axvline(highcut,color='gray', ls='--')
    plt.axvline(lowcut,color='gray', ls='--')
    plt.xlabel('$f/f_s$')
    plt.ylabel('$|R(f/f_s)|$')
    
    # return data
    if return_data:
        return xx, yy
# 
# ---- Lanczos filter
def show_response_lp_lanczos(lowcut=0.25,fs=1.,M=10, fbfilt=True,label=None, xtick_labels_T=False, return_data=False):
    '''Show the lowpass (Lanczos) response function.'''
    # params
    print ('lowcut = ',lowcut)
    print ('fs = ',fs)
    print ('M = ',M)
    print ('fbfilt is ',fbfilt)
    
    # data
    b,a = _lowpass_ba_lanczos(lowcut,fs=fs,M=M)
    
    # plot
    xx, yy = show_response(b, a, fbfilt=fbfilt, label=label, xtick_labels_T=xtick_labels_T, return_data=True)
    plt.title('$f_{low}/f_s = $ $%.2g$' % (lowcut/fs), y=1)
    plt.axvline(lowcut,color='gray', ls='--')
    
    # return data
    if return_data:
        return xx, yy
def show_response_hp_lanczos(highcut=0.25, fs=1., M=10, fbfilt=True, label=None, xtick_labels_T=False, return_data=False):
    '''Show the highpass (Lanczos) response function.'''
    # params
    print ('highcut = ',highcut)
    print ('fs = ',fs)
    print ('M = ',M)
    print ('fbfilt is ',fbfilt)
    
    # data
    b,a = _highpass_ba_lanczos(highcut,fs=fs,M=M)
    
    # plot
    xx, yy = show_response(b, a, fbfilt=fbfilt, label=label, xtick_labels_T=xtick_labels_T, return_data=True)
    plt.title('$f_{high}/f_s = $ $%.2g$' % (highcut/fs), y=1)
    plt.axvline(highcut,color='gray', ls='--')
    
    # return data
    if return_data:
        return xx, yy
def show_response_bp_lanczos(lowcut=0.125,highcut=0.375,fs=1.0,M=10, fbfilt=True,label=None, xtick_labels_T=False, return_data=False):
    '''Show the bandpass (Lanczos) response function.'''
    # params
    print ('lowcut = ',lowcut)
    print ('highcut = ',highcut)
    print ('fs = ',fs)
    print ('M = ',M)
    print ('fbfilt is ',fbfilt)
    
    # data
    b,a = _lowpass_ba_lanczos(highcut,fs=fs,M=M)
    w,hlow = freqz(b,a)
    b,a = _highpass_ba_lanczos(lowcut,fs=fs,M=M)
    w,hhigh = freqz(b,a)
    xx = w/w[-1]/2
    if fbfilt:
        yy = abs(hlow**2*hhigh**2)
    else:
        yy = abs(hlow)*abs(hhigh)
    
    # plot
    plt.plot(xx, yy, label=label)
    plt.title('$f_{high}/f_s = $ $%.2g$, $f_{high}/f_s = $ $%.2g$' % (lowcut/fs, highcut/fs), y=1)
    plt.axvline(highcut,color='gray', ls='--')
    plt.axvline(lowcut,color='gray', ls='--')
    plt.axhline(1,color='gray', ls='--')
    # xtick labels as periods
    if xtick_labels_T:
        T = np.array(
            [2, 4, 10, 100]
        )
        f = 1./T
        xtick_labels = [str(i) for i in T]
        plt.xticks(f, xtick_labels)
        plt.xlabel('$T/T_s$')
        plt.ylabel('$|R(T/T_s)|$')
    else:
        plt.xlabel('$f/f_s$')
        plt.ylabel('$|R(f/f_s)|$')
    
    # return data
    if return_data:
        return xx, yy
# 
