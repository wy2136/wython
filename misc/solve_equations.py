#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Tue Feb 21 19:36:41 EST 2023
#e.g. run -it solve_equations.py x+y=10 x-y=5 x y
import sys, os.path, os, glob, datetime
#import xarray as xr, numpy as np, pandas as pd, matplotlib.pyplot as plt
#more imports
#from misc import get_kws_from_argv
import sympy as sym
#
#
#start from here
#e.g. run -it solve_equations.py x+y=10 x-y=5 x y
equations = [s.split('=')[0]+'-'+s.split('=')[1] for s in sys.argv[1:] if '=' in s] # e.g. ['x+y-10', 'x-y-5']
equations = [s.replace('--', '+') if '--' in s else s for s in equations] # in case negative numbers on the right hand size
variables = [s for s in sys.argv[1:] if '=' not in s] #e.g. ['x', 'y']
solutions = sym.solve(equations, variables)
#print(solutions)
try:
    for key,value in solutions.items():
        print(f'{key} = {value}')
except AttributeError:
    print(' '*12, tuple(variables))
    for ii,item in enumerate(solutions, start=1):
        print(f'solution {ii:2d}:', item)
 
