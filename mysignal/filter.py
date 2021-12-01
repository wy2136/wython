# -*- coding: utf-8 -*-
"""
Created on Thu Jan 15, 2015
 
@author: Wenchang Yang 
"""
from __future__ import print_function

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt

# ---- Butterworth filter
def _lowpass_ba(lowcut=0.25,fs=1.0,order=2):
    nyq = 0.5 * fs
    low = lowcut / nyq
    b,a = butter(order,low,btype='lowpass')
    return b,a
def lowpass(X,lowcut=0.25,fs=1.0,order=2,axis=-1):
    b,a = _lowpass_ba(lowcut,fs=fs,order=order)
    Y = filtfilt(b,a,X,axis=axis)
    return Y
def _highpass_ba(highcut=0.25,fs=1.0,order=2):
    nyq = 0.5 * fs
    high = highcut / nyq
    b,a = butter(order,high,btype='highpass')
    return b,a
def highpass(X,highcut=0.25,fs=1.0,order=2,axis=-1):
    b,a = _highpass_ba(highcut,fs,order=order)
    Y = filtfilt(b,a,X,axis=axis)
    return Y

def _bandpass_ba(lowcut=0.125,highcut=0.375,fs=1.0,order=2):
    nyq = 0.5 * fs
    low = lowcut /nyq
    high = highcut / nyq
    b,a = butter(order,[low,high],btype='bandpass')
    return b,a
def bandpass(X,lowcut=0.125,highcut=0.375,fs=1.0,order=2,axis=-1):
    b,a = _bandpass_ba(lowcut,highcut,fs,order=order)
    Y = filtfilt(b,a,X,axis=axis)
    return Y
# 
# ---- Lanczos filter
def _lowpass_ba_lanczos(lowcut=0.25,fs=1.0,M=10):
    '''estimate the Lanczos lowpass filter coefficients.
    b_k = [\frac{\sin(2\pi f_{cut}k)}{\pi k}][\frac{\sin(\pi k/(M+1))}{\pi k/(M+1)}]
    https://books.google.com/books?id=p7YMOPuu8ugC&pg=PA612&lpg=PA612&dq=Lanczos+filter+coefficients&source=bl&ots=Zx1bDJvGh6&sig=WQqdwryB8SU5d-ygDwAwbpx8IsQ&hl=en&sa=X&ei=cGS5VOqKDNivoQSG0IHoAw&ved=0CD0Q6AEwBA#v=onepage&q=Lanczos%20filter%20coefficients&f=false
    
    http://www.unl.edu.ar/ceneha/uploads/LanczosFiltering(1979).pdf'''
    low = lowcut / fs
    M = float(M)
    k = np.arange(-M,M+1)
    # b = ( np.sin(2*np.pi*low*k) / (np.pi*k) )*( np.sin(np.pi*k/(M+1)) / (np.pi*k/(M+1)) )
    # b[M] = 2*low
    b = 2*low*np.sinc(2*low*k) * np.sinc(k/(M+1))
    b = b / b.sum()
    a = 1.0
    return b,a
def lowpass_lanczos(X,lowcut=0.25,fs=1.,M=10,axis=-1):
    b,a = _lowpass_ba_lanczos(lowcut,fs=fs,M=M)
    Y = filtfilt(b,a,X,axis=axis)
    return Y
def _highpass_ba_lanczos(highcut=0.25,fs=1.0,M=10):
    '''estimate the Lanczos highpass filter coefficients'''
    b,a = _lowpass_ba_lanczos(lowcut=highcut,fs=fs,M=M)
    b = -b
    b[M] = 1+b[M]
    return b,a
def highpass_lanczos(X,highcut=0.25,fs=1.,M=10,axis=-1):
    b,a = _highpass_ba_lanczos(highcut,fs=fs,M=M)
    Y = filtfilt(b,a,X,axis=axis)
    return Y
def bandpass_lanczos(X,lowcut=0.125,highcut=0.375,fs=1.,M=10,axis=-1):
    # Ylow = lowpass_lanczos(X,lowcut=lowcut,fs=fs,M=M,axis=axis)
    # Yhigh = highpass_lanczos(X,highcut=highcut,fs=fs,M=M,axis=axis)
    # Y = X - Ylow - Yhigh
    Y = lowpass_lanczos(X,lowcut=highcut,fs=fs,M=M,axis=axis)
    Y = highpass_lanczos(Y,highcut=lowcut,fs=fs,M=M,axis=axis)
    return Y
# 


