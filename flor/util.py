#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Fri Nov  2 15:52:35 EDT 2018
import os, os.path, sys
import xarray as xr

this_dir, this_file = os.path.split(__file__)

def get_land():
    ifile = os.path.join(this_dir, 'data', 'CTL1860.00010101.atmos_month.land_mask.nc')
    return xr.open_dataarray(ifile)
