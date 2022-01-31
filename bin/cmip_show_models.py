#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Fri Dec 10 22:13:27 EST 2021
if __name__ == '__main__':
    from misc.timer import Timer
    tt = Timer(f'start {__file__}')
import sys, os.path, os, glob, datetime
#import xarray as xr, numpy as np, pandas as pd, matplotlib.pyplot as plt
#more imports
#
if __name__ == '__main__':
    tt.check('end import')
#
#start from here
 
 
if __name__ == '__main__':
    #from wyconfig import * #my plot settings
    show_members = True if len(sys.argv)>1 and 'members' in sys.argv[1:] else False # if members appears in args, also show members
    models = [d for d in os.listdir(os.getcwd())
        if os.path.isdir(d)
        and not d.startswith('wy_')
        and not d.endswith('_error')
        and not d.endswith('_drop')
        and d not in ('old',)
        ]
    models.sort()
    n_models = len(models)
    n_all_members = 0
    n_max = max([len(s) for s in models])
    print()
    print('##', n_models, 'models')
    for ii,model in enumerate(models, start=1):
        if show_members:
            members = [d for d in os.listdir(os.path.join(os.getcwd(), model)) 
                if os.path.isdir(os.path.join(os.getcwd(),model, d))
                and d.startswith('r')
                and not d.endswith('empty')
                ]
            n_members = len(members)
            n_all_members += n_members
            print(f'{ii:2d} of {n_models:2d}:', model.ljust(n_max), f'{n_members:3d}', 'members')
        else:
            print(f'{ii:2d} of {n_models:2d}: {model}')
    if show_members:
        print('##', n_all_members, 'members in total')
    
    #savefig
    if len(sys.argv)>1 and 'savefig' in sys.argv[1:]:
        figname = __file__.replace('.py', f'.png')
        wysavefig(figname)
    tt.check(f'**Done**')
    #plt.show()
    
