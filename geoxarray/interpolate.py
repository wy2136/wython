'''author: Wenchang Yang (yang.wenchang@uci.edu)'''


import numpy as np
from scipy.interpolate import interp1d
import xarray as xr

def regrid(da, **new_grid):
    ''' Interpolate input DataArray into a new grid.
    
    # Input:
        da: DataArray
        new_grid: dict with keys as one of of da.dims, e.g. lon=np.arange(0,360,2).
    
    # Return:
        regrided DataArray.'''
    
    # dim to regrid along
    if len(new_grid) > 1:
        raise ValueError('Currently only support regriding along a SINGLE dimension.')
    da = da.copy()
    regrid_dim = list(new_grid)[0]
    new_grid_values = new_grid[regrid_dim]
    old_grid_values = da[regrid_dim].values
    i_dim = da.dims.index(regrid_dim)
    
    # interpolation function
    f = interp1d(old_grid_values, da.values, kind='linear', axis=i_dim,
        copy=True, bounds_error=False, fill_value='extrapolate',
        assume_sorted=False)

    # wrap into DataArray
    new_coords = {key:da[key] for key in da.dims}
    new_coords[regrid_dim] = new_grid_values
    da_regrid = xr.DataArray(f(new_grid_values),
        dims=da.dims,
        coords=new_coords)
    return da_regrid
    
