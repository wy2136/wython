#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Wed Apr 22 21:45:03 EDT 2020
import datetime, os.path
#import xarray as xr, numpy as np, pandas as pd
#import matplotlib.pyplot as plt
#more imports
#
#start from here
class Timer:
    def __init__(self, label=None):
        _t0 = datetime.datetime.now()
        _tformat = '%Y-%m-%d_%H:%M:%S'
        # _label0: label for the initial time
        if label is None:
            _label = 'start'
        else:
            _label = label
        s = f'[{_t0.strftime(_tformat)}]: {_label}'
        print()
        print(s)    
        self._t0 = _t0
        self._tformat = _tformat
        self._label0 = _label

    def check(self, label=None):
        '''check time point and length from the initial point'''
        _t = datetime.datetime.now()
        if label is None:
            _label = 'checkpoint'
        else:
            _label = label
        _label0 = self._label0
        s = f'[{_t.strftime(self._tformat)}]: {_label}; **{(_t - self._t0).seconds:,}** seconds from "{_label0}"'
        print()
        print(s)
 
    def reset(self, label=None):
        _t0 = datetime.datetime.now()
        _tformat = self._tformat
        if label is None:
            _label = 'start'
        else:
            _label = label
        s = f'[{_t0.strftime(_tformat)}]: {_label}'
        print()
        print(s)    
        self._t0 = _t0
        self._label0 = _label
    def today(self, fmt='%Y-%m-%d'):
        return datetime.date.today().strftime(fmt)

    def now(self, fmt='%Y-%m-%dT%H:%M:%S'):
        return datetime.datetime.now().strftime(fmt)

    def getmdate(self, ifile, fmt='%Y-%m-%d'):
        """get the modified time of the given file in the default format of '%Y-%m-%d'
        """
        mtime = os.path.getmtime(ifile)
        return datetime.datetime.fromtimestamp(mtime).strftime(fmt)


def today(fmt='%Y-%m-%d'):
    return datetime.date.today().strftime(fmt)

def now(fmt='%Y-%m-%d_%H:%M:%S'):
    return datetime.datetime.now().strftime(fmt)

if __name__ == '__main__':
    t = Timer()
    t.check()
    t.check()
    t.reset('restart')
    t.check()

    print('today is', t.today() )
    print('now is', t.now() )

