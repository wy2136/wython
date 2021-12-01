"""
Author: Wenchang Yang
Email: yang.wenchang@uci.edu
"""
import numpy as np

def cal_grid_area(lon, lat):
    '''Calculate area of each grid specified by lon and lat, with unit Earth radius.'''
    Nx = lon.size
    Ny = lat.size
    
    # re-orgznize the longitude and latitude vectors
    lon_ = lon.reshape((Nx, 1))
    lat_ = lat.reshape((Ny, 1))
    
    # initialize dlon and dlat
    dlon = np.zeros((Nx, 1))
    dlat = np.zeros((Ny, 1))
    
    # interior values
    dlon[1:-1] = (lon_[2:] - lon_[:-2])/2.0
    dlat[1:-1] = (lat_[2:] - lat_[:-2])/2.0
    
    # dlon boundary values
    dlon[0] = lon_[1] - lon_[0]
    dlon[-1] = lon_[-1] - lon_[-2]
    
    # dlat boundary values: depend on the order of the lat vector
    if lat_[1] >= lat_[0]:
        lat_lower = max(-90, lat_[0]*2 - lat_[1])
        dlat[0] = (lat_[1] - lat_lower)/2.0
        lat_upper = min(90, lat_[-1]*2 - lat_[-2])
        dlat[-1] = (lat_upper - lat_[-2])/2.0
    else: # lat_[1] < lat_[0]
        lat_upper = min(90, lat_[0]*2 - lat_[1])
        dlat[0] = (lat_[1] - lat_upper)/2.0
        lat_lower = min(-90, lat_[-1]*2 - lat_[-2])
        dlat[-1] = (lat_lower - lat_[-2])/2.0
        dlat *= -1
    
    # change the units from degree to radian
    dlon = dlon * np.pi/180.0
    dlat = dlat * np.pi/180.0
    lat_ = lat_ * np.pi/180.0
    
    # calculate the area covered each grid
    S = np.cos(lat_)*dlat*dlon.T
    
    return S
    
    
        
    
    