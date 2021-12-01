# -*- coding: utf-8 -*-
"""
@author: yang
"""
# import numpy as np
# import webbrowser
# from netCDF4 import Dataset
# import matplotlib.pyplot as plt
# import pandas as pd
# import myplot as mt
# import atmos_ocean as ao

from . import connect_to_data as igc
from .connect_to_data import goto, look, readnames, readunits, read, readall, readlon, readlat, readt, readXYclim, num2time

from . import data_lib_management as igd
from .data_lib_management import get_data, find, get_data_from_erai, get_data_from_cmip5, get_models_from_cmip5, get_runs_from_cmip5

# from . import data_lib

from . import ingrid_operators as igo
from .ingrid_operators import *


#
# def _get_server_from_url(url):
#     print url
#     return 'http://' + url.split('//')[1].split('/')[0]
# def _get_path_from_url(url):
#     return [
#         '/' + '/'.join( url.split('/')[3:] )
#     ]