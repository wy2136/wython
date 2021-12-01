#!/usr/bin/env python
# Written by Wenchang Yang (yang.wenchang@uci.edu)

import numpy as np
from numba import jit#, float64

# @jit(float64(float64[:], float64[:], float64),
#     nopython=True, nogil=True)
@jit(nopython=True, nogil=True)
def vi1d(q, plevels, ps):
    '''Vertically integrate q with shape (nlevel,), given pressure
    levels 'plevels' and surface air pressure.

    *Input*:
        q: ndarray with shape (nlevel,).
        plevels: ndarray with shape (nlevel,), in *ascending* order..
        ps: scalar.

    *Return*:
        viq: scalar.'''

    if ps <= plevels[0]: # integral levels are all under the surface
        return 0
    elif ps <= plevels[1]: # only one level is above surface
        return q[0] * (ps - plevels[0])/2.0
    else: # more than two levels are above surface
        nlevel_above_surface = plevels[plevels < ps].size
        viq = 0
        for i in range(nlevel_above_surface):
            if i == 0:
                viq += q[i] * (plevels[i+1] - plevels[i])/2.0
            elif i <  nlevel_above_surface - 1:
                viq += q[i] * (plevels[i+1] - plevels[i-1])/2.0
            else:
                viq += q[i] * (ps - plevels[i-1])/2.0
        return viq

# @jit(float64[:,:](float64[:,:,:], float64[:], float64[:,:]),
#     nopython=True, nogil=True)
@jit(nopython=True, nogil=True)
def vi3d(q, plevels, ps):
    '''Vertically integrate ndarray q with shape (nlevel, nlat, lon)
     or (nlevel, nlon, nlat).

    *Input*:
        q: ndarray, (nlevel, nlat, nlon) or (nlevel, nlon, nlat) shape.
        plevels: ndarray, (nlevel,) shape.
        ps: ndarray, (nlat, nlon) or (nlon, nlat) shape.

    *Return*:
        viq: ndarray, (nlat, nlon) or (nlon, nlat) shape .'''

    nlevel, M, N = q.shape
    viq = np.zeros((M, N))
    for i in range(M):
        for j in range(N):
            viq[i, j] = vi1d(q[:, i, j], plevels, ps[i, j])
    return viq

# @jit(float64[:,:,:](float64[:,:,:,:], float64[:], float64[:,:,:]),
    # nopython=True, nogil=True)
@jit(nopython=True, nogil=True)
def vi4d(q, plevels, ps):
    '''Vertically integrate 4-D ndarray q.

    *Input*:
        q: ndarray, (ntime, nlevel, nlat, nlon)
            or (ntime, nlevel, nlon, nlat) shape.
        plevels: ndarray, (nlevel,) shape.
        ps: ndarray, (ntime, nlat, nlon) or (ntime, nlon, nlat) shape.

    *Return*:
        viq: (ntime, nlat, nlon) shape ndarray.'''

    ntime, nlevel, M, N = q.shape
    viq = np.zeros((ntime, M, N))
    for i in range(ntime):
        for j in range(M):
            for k in range(N):
                viq[i, j, k] = vi1d(q[i, :, j, k], plevels, ps[i, j, k])
    return viq
