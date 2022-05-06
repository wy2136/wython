#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Wed Aug  7 12:41:13 EDT 2019

# matplotlib setting
print()
print(f'**wython plot settings ({__file__})**')
import os, os.path, datetime
import xarray as xr
import matplotlib.pyplot as plt
from cycler import cycler

#rcParams
"""
plt.rcParams['figure.dpi'] = 128
plt.rcParams['figure.figsize'] = [6.4, 6.4*9/16]
plt.rcParams['figure.constrained_layout.use'] = True
print(f"[config]: plt.rcParams['figure.dpi'] = {plt.rcParams['figure.dpi']}")
print("[config]: plt.rcParams['figure.figsize'] = [6.4, 6.4*9/16]")
print(f"[config]: plt.rcParams['figure.constrained_layout.use'] = {plt.rcParams['figure.constrained_layout.use']}")
if plt.rcParams['figure.constrained_layout.use']:
    print(f"    plt.tight_layout() is NOT needed if plt.rcParams['figure.constrained_layout.use'] = True")
"""
#figure
plt.rc('figure', dpi=128, figsize=[6.4, 6.4*9/16])
plt.rc('figure.constrained_layout', use=True)
#axes
plt.rc('axes', titlelocation='left')
plt.rc('axes.spines', right=False, top=False)
#pro_cycle
plt.rc('axes', prop_cycle=cycler(linestyle=['-', '--', ':', '-.'])*(plt.rcParams['axes.prop_cycle']))
#grid
plt.rc('axes', grid=True)
plt.rc('grid', linestyle='--', alpha=0.5)
#legend
plt.rc('legend', frameon=False)
#hatches
plt.rc('hatch', color='gray', linewidth=0.5)
print('plt.rcParams:')
paramlist = ['figure.dpi', 'figure.figsize', 'figure.constrained_layout.use',
    'axes.titlelocation', 'axes.spines.right', 'axes.spines.top', 'axes.prop_cycle',
    'axes.grid', 'grid.linestyle', 'grid.alpha',
    'legend.frameon', 
    'hatch.color', 'hatch.linewidth'
    ]
for p in paramlist:
    value = plt.rcParams[p]
    print(f'    {p}: {value}')

#colormaps
import misc.colormaps
print('[imported]: import misc.colormaps')
xr.set_options(cmap_sequential='parula')
print('[config]: xr.set_options(cmap_sequential="parula")')
#xr.set_options(cmap_divergent='turbo')
#print('[config]: xr.set_options(cmap_divergent="turbo")')
# define shortcut functions of constrained_layout_on and constrained_layout_off to set plt.rcParams['figure.constrained_layout.use']

#useful functions
def constrained_layout_on(): plt.rcParams['figure.constrained_layout.use'] = True
def constrained_layout_off(): plt.rcParams['figure.constrained_layout.use'] = False
print('[shortcut functions]:')
print("    constrained_layout_on():  plt.rcParams['figure.constrained_layout.use'] = True")
print("    constrained_layout_off(): plt.rcParams['figure.constrained_layout.use'] = False")
# define wysavefig function: archive fig if exists
def wysavefig(figname, **kws):
    """updated version of plt.savefig"""
    bbox_inches = kws.pop('bbox_inches', 'tight')
    overwritefig = kws.pop('overwritefig', False)
    if os.path.exists(figname) and not overwritefig: #archive by appending date info to figname if figname exists
        mtime = datetime.datetime.fromtimestamp( os.path.getmtime(figname) ).strftime('%Y-%m-%d')
        figname_archive = figname + '.' + mtime
        if os.path.isdir('_history'):#move the archived file to the _history dir if it exists
            figname_archive = os.path.join(os.path.dirname(figname_archive), '_history', os.path.basename(figname_archive))
        os.rename(figname, figname_archive)
        print('[archived]:', figname, '->', figname_archive)
    #savefig
    plt.savefig(figname, bbox_inches=bbox_inches, **kws)
    print('[saved]:', figname)
print('[created]: def wysavefig(figname, **kws):')
# ipython setting
try:
    get_ipython().run_line_magic('config', "InlineBackend.figure_format ='retina'")
    print("[iPython config]: InlineBackend.figure_format ='retina'")
except:
    pass

print()
"""
#not needed after a recent upgrade to Python 3.9.1 (2021-06-03)
if 'PROJ_LIB' not in os.environ:
    os.environ['PROJ_LIB'] = '/'.join ( os.__file__.split('/')[:-3] + ['share', 'proj'])
    print('[added]: PROJ_LIB =', os.environ['PROJ_LIB'])
"""

