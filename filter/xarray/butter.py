'''
Butterworth filter: lowpass, highpass and bandpass.

Author: Wenchang Yang (wenchang@princeton.edu)
'''

import numpy as np
# import matplotlib.pyplot as plt
import xarray as xr

from ..butter import lowpass as lp
from ..butter import highpass as hp
from ..butter import bandpass as bp

def lowpass(da, cutoff=0.25, order=2, dim=None, fs=1.0):
    '''Butterworth lowpass filter for xarray.DataArray input data.

    *Parameters*:
        da: xarray.DataArray.
        cutoff: float, low-frequency cutoff, default=0.25 (unit is sample freqency).
        order: int, default=2.
        dim: str, default=None (the first dimension).
        fs: number, sample freqency, default=1.0

    *Return*:
        DataArray, lowpassed da.'''

    if dim is None:
        dim = da.dims[0]
        axis = 0
    else:
        axis = da.dims.index(dim)

    # numpy version lowpass
    Y = lp(da.data, cutoff=cutoff, order=order, axis=axis, fs=fs)

    # wrap the result into a DataArray
    dims = da.dims
    coords = da.coords
    attrs = da.attrs.copy()
    s = 'cutoff={}, order={}, dim={}, fs={}'.format(cutoff, order, dim, fs)
    attrs['Forward-backward Butterworth lowpass'] = s
    return xr.DataArray(Y, dims=dims, coords=coords, attrs=attrs)

def highpass(da, cutoff=0.25, order=2, dim=None, fs=1.0):
    '''Butterworth highpass filter for xarray.DataArray input data.

    *Parameters*:
        da: xarray.DataArray.
        cutoff: float, high-frequency cutoff, default=0.25 (unit is sample freqency).
        order: int, default=2.
        dim: str, default=None (the first dimension).
        fs: number, sample freqency, default=1.0

    *Return*:
        DataArray, highpassed da.'''

    if dim is None:
        dim = da.dims[0]
        axis = 0
    else:
        axis = da.dims.index(dim)

    # numpy version lowpass
    Y = hp(da.data, cutoff=cutoff, order=order, axis=axis, fs=fs)

    # wrap the result into a DataArray
    dims = da.dims
    coords = da.coords
    attrs = da.attrs.copy()
    s = 'cutoff={}, order={}, dim="{}", fs={}'.format(cutoff, order, dim, fs)
    attrs['Forward-backward Butterworth highpass'] = s
    return xr.DataArray(Y, dims=dims, coords=coords, attrs=attrs)

def bandpass(da, cutoff=(0.125, 0.375), order=2, dim=None, fs=1.0):
    '''Butterworth bandpass filter for xarray.DataArray input data.

    *Parameters*:
        da: xarray.DataArray.
        cutoff: (float, float), low/high-frequency cut, default=(0.125, 0.375) (unit is sample freqency).
        order: int, default=2.
        dim: str, default=None (the first dimension).
        fs: number, sample freqency, default=1.0

    *Return*:
        DataArray, bandpassed da.'''

    if dim is None:
        dim = da.dims[0]
        axis = 0
    else:
        axis = da.dims.index(dim)

    # numpy version lowpass
    Y = bp(da.data, cutoff=cutoff, order=order,
        axis=axis, fs=fs)

    # wrap the result into a DataArray
    dims = da.dims
    coords = da.coords
    attrs = da.attrs.copy()
    s = 'lowcut={}, highcut={}, order={}, dim="{}", fs={}'.format(
        cutoff[0], cutoff[1], order, dim, fs)
    attrs['Forward-backward Butterworth bandpass'] = s
    return xr.DataArray(Y, dims=dims, coords=coords, attrs=attrs)
