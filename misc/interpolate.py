'''
Reference: https://stackoverflow.com/questions/20915502/speedup-scipy-griddata-for-multiple-interpolations-between-two-irregular-grids

Wenchang Yang (yang.wenchang@uci.edu)
'''
from scipy.spatial import qhull
import numpy as np

def interp_weights(xy, XY, d=2):
    tri = qhull.Delaunay(xy)
    simplex_indices = tri.find_simplex(XY)
    vertices = np.take(tri.simplices, simplex_indices, axis=0)
    temp = np.take(tri.transform, simplex_indices, axis=0)
    delta = XY - temp[:, d, :]
    bary = np.einsum('njk,nk->nj', temp[:, :d, :], delta)
    weights = np.hstack( (bary, 1-bary.sum(axis=1, keepdims=True)))

    return vertices, weights

def interpolate(values, vertices, weights, fill_value=np.nan):
    result = np.einsum('nj,nj->n', np.take(values, vertices), weights)
    result[np.any(weights<0, axis=1)] = fill_value

    return result

def batch_interpolate(values, vertices, weights, fill_value=np.nan):
    result = np.einsum('bnj,nj->bn', np.take(values, vertices, axis=1), weights)
    result[:, np.any(weights<0, axis=1)] = fill_value

    return result

def ftji2tlatlon(f_tji, lon_ji, lat_ji, lon_vec, lat_vec, loop_used=False):
    nt, nj, ni = f_tji.shape
    nlon, nlat = lon_vec.size, lat_vec.size

    # from x, y to xy
    x = lon_ji.ravel()
    y = lat_ji.ravel()
    L = ~np.isnan(x+y)
    x = x[L]
    y = y[L]
    xy = np.array([x, y]).transpose()

    #  from lon_vec, lat_vec to XY
    Lon, Lat = np.meshgrid(lon_vec, lat_vec)
    X = Lon.ravel()
    Y = Lat.ravel()
    XY = np.array([X, Y]).transpose()

    vertices, weights = interp_weights(xy, XY, d=2)
    if loop_used:
        f_tlatlon = np.zeros((nt, nlat, nlon))
        for k in range(nt):
            values = f_tji[k, :, :].ravel()[L]
            r = interpolate(values, vertices, weights, fill_value=np.nan)
            f_tlatlon[k, :, :] = r.reshape((nlat, nlon))
    else:
        f_tlatlon = np.zeros((nt, nlat*nlon))
        values = f_tji.reshape((nt, nj*ni))[:, L]
        f_tlatlon = batch_interpolate(values, vertices, weights,
            fill_value=np.nan)
        f_tlatlon = f_tlatlon.reshape((nt, nlat, nlon))


    return f_tlatlon
