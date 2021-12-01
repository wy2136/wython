import numpy as np
from scipy.stats import sem as _sem, t as stu
import xarray as xr

def sem(da, **kws):
    '''standard error of the mean (xarray version).'''
    dim = kws.pop('dim', None)
    if dim is None:
        dim = da.dims[0] # default dim is the first dim
    kws['axis'] = -1
    return xr.apply_ufunc(_sem,
                          da, 
                          input_core_dims=[[dim]],
                          kwargs=kws
                         )
def _cim(zz, **kws):
    '''confidence interval of the mean (numpy version).
    **input**:
        zz: input ndarray
        confidence: default = 0.95
        ddof: default = 1'''
    if not isinstance(zz, np.ndarray):
        zz = np.array(zz)
    confidence = kws.pop('confidence', 0.95)
    ddof = kws.pop('ddof', 1) 
    axis = kws.pop('axis', None) # default cim over all the elements of the array
    # sample size
    if axis is None:
        n = zz.size
    else:
        n = zz.shape[axis]
    dof = n - ddof # 
    std_err = _sem(zz, axis=axis, **kws)
    return std_err * stu.ppf((1 + confidence) / 2, dof)
def cim(da, **kws):
    '''confidence interval of the mean (xarray version).
    **input**:
        da: input dataarray
        confidence: default = 0.95
        ddof: default = 1
        dim: default is the first dimension of the input dataarray'''
    dim = kws.pop('dim', None)
    if dim is None:
        dim = da.dims[0] # default dim is the first dim
    kws['axis'] = -1
    return xr.apply_ufunc(_cim,
                          da, 
                          input_core_dims=[[dim]],
                          kwargs=kws
                         )
