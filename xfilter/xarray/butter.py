'''
Butterworth filter: lowpass, highpass and bandpass.

Author: Wenchang Yang (wenchang@princeton.edu)
'''
import xarray as xr

# import the numpy-based functions
from ..butter import lowpass as lp
from ..butter import highpass as hp
from ..butter import bandpass as bp

def lowpass(da, cutoff=0.25, order=2, dim=None, fs=1.0, **kws):
    '''Butterworth lowpass filter for xarray.DataArray input data.

    *Parameters*:
        da: xarray.DataArray.
        cutoff: float, low-frequency cutoff, default=0.25 (unit is sample freqency).
        order: int, default=2.
        dim: str, default=None (the first dimension).
        fs: number, sample freqency, default=1.0
        kws: other arguments used in scipy.signal.filtfilt

    *Return*:
        DataArray, lowpassed da.'''

    if dim is None:
        assert da.ndim == 1, 'only 1-D array is allowed when dim is None; specify dim explicitly otherwise' 
        axis = 0
    else:
        axis = da.dims.index(dim)

    kwargs = dict(axis=axis, cutoff=cutoff, order=order, fs=fs, **kws)

    return xr.apply_ufunc(lp, da,
        kwargs=kwargs, dask='allowed'
        )

def highpass(da, cutoff=0.25, order=2, dim=None, fs=1.0, **kws):
    '''Butterworth highpass filter for xarray.DataArray input data.

    *Parameters*:
        da: xarray.DataArray.
        cutoff: float, high-frequency cutoff, default=0.25 (unit is sample freqency).
        order: int, default=2.
        dim: str, default=None (the first dimension).
        fs: number, sample freqency, default=1.0
        kws: other arguments used in scipy.signal.filtfilt

    *Return*:
        DataArray, highpassed da.'''

    if dim is None:
        assert da.ndim == 1, 'only 1-D array is allowed when dim is None; specify dim explicitly otherwise' 
        axis = 0
    else:
        axis = da.dims.index(dim)

    kwargs = dict(axis=axis, cutoff=cutoff, order=order, fs=fs, **kws)

    return xr.apply_ufunc(hp, da,
        kwargs=kwargs, dask='allowed'
        )

def bandpass(da, cutoff=(0.125, 0.375), order=2, dim=None, fs=1.0, **kws):
    '''Butterworth bandpass filter for xarray.DataArray input data.

    *Parameters*:
        da: xarray.DataArray.
        cutoff: (float, float), low/high-frequency cut, default=(0.125, 0.375) (unit is sample freqency).
        order: int, default=2.
        dim: str, default=None (the first dimension).
        fs: number, sample freqency, default=1.0
        kws: other arguments used in scipy.signal.filtfilt

    *Return*:
        DataArray, bandpassed da.'''

    if dim is None:
        assert da.ndim == 1, 'only 1-D array is allowed when dim is None; specify dim explicitly otherwise' 
        axis = 0
    else:
        axis = da.dims.index(dim)

    kwargs = dict(axis=axis, cutoff=cutoff, order=order, fs=fs, **kws)

    return xr.apply_ufunc(bp, da,
        kwargs=kwargs, dask='allowed'
        )

if __name__ == '__main__':
	from wyconfig import *
	import numpy as np, xarray as xr	
	np.random.seed(0)
	da = xr.DataArray(np.random.randn(100), dims='day', name='Ta', attrs={'units': 'degC'})

	fig, axes = plt.subplots(1, 1)
	ax = axes[0]
	da.plot(label='raw', color='k', ax=ax)
	bandpass(da, [1/10, 1/5]).plot(ax=ax)
	ax.legend(loc='lower right')    

	plt.show()
