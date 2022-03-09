#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Mon Mar  7 17:12:07 EST 2022
if __name__ == '__main__':
    import sys
    from misc.timer import Timer
    tt = Timer('start ' + ' '.join(sys.argv))
import sys, os.path, os, glob, datetime
#import xarray as xr, numpy as np, pandas as pd, matplotlib.pyplot as plt
import numpy as np
from numpy import pi, sin, cos, arctan2
#more imports
#
if __name__ == '__main__':
    tt.check('end import')
#
#start from here
def gcdistance(lat1, lon1, lat2, lon2, units='m'):
    """
    From: https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude

    This uses the ‘haversine’ formula to calculate the great-circle distance between two points – that is, 
    the shortest distance over the earth’s surface – giving an ‘as-the-crow-flies’ distance between the points 
    (ignoring any hills they fly over, of course!).
    Haversine
    formula:    a = sin²(Δφ/2) + cos φ1 ⋅ cos φ2 ⋅ sin²(Δλ/2)
    c = 2 ⋅ atan2( √a, √(1−a) )
    d = R ⋅ c
    where   φ is latitude, λ is longitude, R is earth’s radius (mean radius = 6,371km);
    note that angles need to be in radians to pass to trig functions!
    """
    R = 6371.0088 * 1000
    #lat1,lon1,lat2,lon2 = map(np.radians, [lat1,lon1,lat2,lon2])
    lat1 = lat1*pi/180
    lon1 = lon1*pi/180
    lat2 = lat2*pi/180
    lon2 = lon2*pi/180

    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2) **2
    c = 2 * arctan2(a**0.5, (1-a)**0.5)
    d = R * c
    
    if units == 'km':
        d = d/1000
    elif units == 'mile':
        d = d/1000*0.621371
    return d
 
def tc_distance(ds, lat0, lon0, units='m'):
    """use gcdistance to calculate great-circle distance from TC track points in ds to (lat0, lon0)"""
    return gcdistance(ds.lat, ds.lon, lat0, lon0, units=units)
 
if __name__ == '__main__':
    #from wyconfig import * #my plot settings
    # https://andrew.hedges.name/experiments/haversine/
    lat1, lon1, lat2, lon2 = 38.898556, -77.037852, 38.897147, -77.043934
    d = gcdistance(lat1, lon1, lat2, lon2)
    d_km = gcdistance(lat1, lon1, lat2, lon2, units='km')
    d_mile = gcdistance(lat1, lon1, lat2, lon2, units='mile')
    
    print(f'{d = } m: {lat1 = }, {lon1 = }, {lat2 = }, {lon2 = }')
    print(f'{d_km = } km: {lat1 = }, {lon1 = }, {lat2 = }, {lon2 = }')
    print(f'{d_mile = } mile: {lat1 = }, {lon1 = }, {lat2 = }, {lon2 = }')

    print()
    lat1, lon1, lat2, lon2 = 0, 0, np.array([0, 0, 0, 0, 90, 90, -90, -90]), np.array([90, 180, 270, 360, 0, 180, 0, 180])
    d = gcdistance(lat1, lon1, lat2, lon2, units='km')
    print(f'{d = } km: {lat1 = }, {lon1 = }, {lat2 = }, {lon2 = }')
    for ii,(lat_, lon_) in enumerate(zip(lat2, lon2)):
        print(f'{d[ii] = :,} km: {lat1 = }, {lon1 = }, {lat_ = }, {lon_ = }')
    
    #savefig
    if len(sys.argv)>1 and 'savefig' in sys.argv[1:]:
        figname = __file__.replace('.py', f'.png')
        if 'overwritefig' in sys.argv[1:]:
            wysavefig(figname, overwritefig=True)
        else:
            wysavefig(figname)
    tt.check(f'**Done**')
    print()
    #plt.show()
    
