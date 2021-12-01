'''
Reference: https://stackoverflow.com/questions/20915502/speedup-scipy-griddata-for-multiple-interpolations-between-two-irregular-grids

Wenchang Yang (yang.wenchang@uci.edu)
'''
from scipy.spatial import qhull
import numpy as np
from numba import jit

def interp_weights(x, X):
    nx, nX = x.size, X.size
    bounds = np.zeros((nX, 2), dtype=np.int32)
    weights = np.zeros((nX, 2))
    for i in range(nX):
        if X[i] < x[0]:
            bounds[i, :] = 0, 1
            weights[i, :] = (x[1]-X[i])/(x[1]-x[0]), (X[i]-x[0])/(x[1]-x[0])
        elif X[i] > x[nx-1]:
            bounds[i, :] = nx-2, nx-1
            weights[i, :] = (x[nx-1]-X[i])/(x[nx-1]-x[nx-2]),\
                (X[i]-x[0])/(x[nx-1]-x[nx-2])
        else:
            for j in range(nx-1):
                if X[i] > x[j] and X[i] < x[j+1]:
                    bounds[i, :] = j, j+1
                    weights[i, :] = (x[j+1]-X[i])/(x[j+1]-x[j]), \
                        (X[i]-x[j])/(x[j+1]-x[j])

    return bounds, weights
# jitize
interp_weights_jit = jit(interp_weights, nopython=True)

def ftkji2tpji(Ftkji, Ptkji, Pp, fill_value=None):
    '''Interpolate Ftkji(shape: nt, nlev, nlat, nlon) on pressure levels of
    Pp(shape: nplev,) given the pressure field Ptjji(shape: nt, nlev, nlat, nlon).
    The return is Ftpji(shape: nt, nplev, nlat, nlon). It is useful to convert
    outputs from CESM-LE atmospheric fields onto pressure levels.

    ** Input **
        Ftkji: array-like, shape(nt, nlev, nlat, nlon)
        Ptkji: array-like, shape(nt, nlev, nlat, nlon)
        Pp: vector, shape(nplev,)
        fill_value: scalar, default is nan

    ** Returns **
        Ftpji: array-like, shape(nt, nplev, nlat, nlon)'''
    if fill_value is None:
        fill_value = np.nan
    n_time, n_lev, n_lat, n_lon = Ftkji.shape
    n_plev = Pp.size
    Ftpji = np.zeros((n_time, n_plev, n_lat, n_lon))

    for t in range(n_time):
        for j in range(n_lat):
            for i in range(n_lon):
                for p in range(n_plev):
                    if Pp[p] < Ptkji[t, 0, j, i] \
                        or Pp[p] > Ptkji[t, n_lev-1, j, i]:
                        # specified pressure is out of range of model levels
                        Ftpji[t, p, j, i] = fill_value
                    else:
                        for k in range(n_lev-1):
                            #
                            if Pp[p] >= Ptkji[t, k, j, i] \
                                and Pp[p] <= Ptkji[t, k+1, j, i]:
                                d0, d1, d = Pp[p] - Ptkji[t, k, j, i],\
                                    Ptkji[t, k+1, j, i] - Pp[p], \
                                    Ptkji[t, k+1, j, i] - Ptkji[t, k, j, i]
                                w0, w1 = d1/d, d0/d
                                Ftpji[t, p, j, i] = w0 * Ftkji[t, k, j, i] \
                                    + w1 * Ftkji[t, k+1, j, i]
    return Ftpji
# jitize
ftkji2tpji_jit = jit(ftkji2tpji, nopython=True)
