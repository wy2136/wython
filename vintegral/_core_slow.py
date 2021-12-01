#!/usr/bin/env python
# Written by Wenchang Yang (yang.wenchang@uci.edu)
import numpy as np
# from numba import jit

# @jit
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

# @jit
def vi3d(q, plevels, ps):
    '''Vertically integrate ndarray q with shape (nlevel, nlat, lon).

    *Input*:
        q: (nlevel, nlat, nlon) shape ndarray.
        plevels: (nlevel,) shape ndarray.
        ps: (nlat, nlon) shape ndarray.

    *Return*:
        viq: (nlat, nlon) shape ndarray.'''
    nlevel, nlat, nlon = q.shape
    viq = np.zeros((nlat, nlon))
    for ilat in range(nlat):
        for ilon in range(nlon):
            viq[ilat, ilon] = vi1d(q[:, ilat, ilon], plevels, ps[ilat, ilon])
    return viq

# @jit
def vi4d(q, plevels, ps):
    '''vertically integrate ndarray q with shape(ntime, nlvel, nlat, nlon).

    *Input*:
        q: (ntime, nlevel, nlat, nlon) shape ndarray.
        plevels: (nlevel,) shape ndarray.
        ps: (ntime, nlat, nlon) shape ndarray.

    *Return*:
        viq: (ntime, nlat, nlon) shape ndarray.'''
    ntime, nlevel, nlat, nlon = q.shape
    viq = np.zeros((ntime, nlat, nlon))
    for i in range(ntime):
        viq[i, :, :] = vi3d(q[i, :, :, :], plevels, ps[i, :, :])
    return viq
