'''
Author: Wenchang Yang (wenchang@princeton.edu)
'''
from .butter import lowpass, highpass, bandpass

# from .xarray.butter import lowpass, highpass, bandpass
from .xarray.accessor import FilterAccessor # e.g. array.filter.lowpass

from .xarray.response import (lowpass_response,
    highpass_response, bandpass_response)
