#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Sun Dec 12 21:48:28 EST 2021
if __name__ == '__main__':
    import sys
    from misc.timer import Timer
    s = ' '
    tt = Timer(s.join(sys.argv))
import sys, os.path, os, glob, datetime, re
#import xarray as xr, numpy as np, pandas as pd, matplotlib.pyplot as plt
#more imports
#
if __name__ == '__main__':
    tt.check('end import')
#
#start from here
def cmip6_model_members(daname, expname, yearspan=None):
    idir = f'/tigress/wenchang/data/cmip6/variables/{daname}'
    expname_versions = [s for s in os.listdir(idir) if s.startswith(expname)]
    if expname_versions:
        expname_versions.sort()
        expname_version = expname_versions[-1]
        idir = os.path.join(idir, expname_version, 'wy_regrid_all_members')
    #idir = f'/tigress/wenchang/data/cmip6/variables/{daname}/{expname}/wy_regrid_all_members'
    if not os.path.exists(idir): idir = idir.replace('wy_regrid_all_members', 'wy_regrid') #some exp/var have only one ens member for each model
    ifiles = [ncfile for ncfile in os.listdir(idir) if ncfile.endswith('.nc')]
    if not ifiles:
        #try to look at a sub directory under the original idir, e.g. 850hPa/
        idir = [os.path.join(idir, subdir) for subdir in os.listdir(idir) 
            if os.path.isdir(os.path.join(idir, subdir)) 
            and os.listdir(os.path.join(idir, subdir))][0]
        ifiles = [ncfile for ncfile in os.listdir(idir) if ncfile.endswith('.nc')]
    #condition that the input data file must cover the specified year span in the format of (year_start, year_end)
    if yearspan is not None:
        ifiles = [ifile for ifile in ifiles 
            if int( ifile.split('.')[-2].split('-')[0] ) <= yearspan[0]
            and int( ifile.split('.')[-2].split('-')[-1] ) >= yearspan[-1]
            ]
    #ifiles.sort()
    model_members = ['_'.join( ifile.split('.')[2:4] ) for ifile in ifiles]
    #sort by model then by member
    #model_members.sort(key = lambda x: x.split('_')[0] + ''.join([f'{int(s):03d}' for s in re.split(r'[ipf]', x.split('_')[1][1:])]))
    #print(model_members)
    #print(idir)
    #print(model_members)
    return model_members
def cmip6_model_members_in_common(*daexp_pairs, yearspan=None):
    """example input: ('ts', 'hist-nat'), ('ts', 'hist-GHG')"""
    model_members_sets_list = [] #list of sets
    for daname,expname in daexp_pairs:
        model_members = cmip6_model_members(daname, expname, yearspan=yearspan)
        model_members_sets_list.append(set(model_members))
    model_members_in_common = model_members_sets_list[0].intersection(*model_members_sets_list)
    model_members_in_common = list(model_members_in_common)
    #model_members_in_common.sort()
    #sort by model then by member
    model_members_in_common.sort(key = lambda x: x.split('_')[0] + ''.join([f'{int(s):03d}' for s in re.split(r'[ipf]', x.split('_')[1][1:])]))
    return model_members_in_common
def cmip6_model_members_count(model_members):
    n_model_members = len(model_members)
    models = list( set([model_member.split('_')[0] for model_member in model_members]) )
    models.sort()
    n_models = len(models)
    max_len = max([len(m) for m in models])
    n_members = {model: len([m_m for m_m in model_members if m_m.split('_')[0]==model]) for model in models}
    #print(n_members)
    print()
    print('members:')
    for ii,model_member in enumerate(model_members, start=1):
        print(f'{ii:3d} of {n_model_members:3d}:', model_member)
    print()
    print('models:')
    for ii,model in enumerate(models, start=1):
        print(f'{ii:2d} of {n_models:2d}: {model.ljust(max_len)} {n_members[model]:2d} members')
    print(f'**{len(model_members)}** members in total')
def cmip6_models_in_common(*daexp_pairs):
    """example input: ('ts', 'hist-nat'), ('ts', 'hist-GHG')"""
    models_sets_list = [] #list of sets
    for daname,expname in daexp_pairs:
        model_members = cmip6_model_members(daname, expname)
        models = [model_member.split('_')[0] for model_member in model_members]
        models_sets_list.append(set(models))
    models_in_common = models_sets_list[0].intersection(*models_sets_list)
    models_in_common = list(models_in_common)
    models_in_common.sort()
    return models_in_common
def cmip6_models_count(models):
    models.sort()
    n_models = len(models)
    print()
    for ii,model in enumerate(models, start=1):
        print(f'{ii:2d} of {n_models:2d}: {model}')
    print(f'**{len(models)}** model in total')
 
 
if __name__ == '__main__':
    #from wyconfig import * #my plot settings
    #daexp_pairs = zip(sys.argv[1::2], sys.argv[2::2]) #e.g. python cmip6_model_members_in_common.py ts hist-nat ts hist-GHG
    #models = cmip6_models_in_common(*daexp_pairs)
    #cmip6_models_count(models)
    try:
        yearspan = (int(sys.argv[-2]), int(sys.argv[-1]))
        daexp_pairs = zip(sys.argv[1:-2:2], sys.argv[2:-2:2]) #e.g. python cmip6_model_members_in_common.py ts hist-nat ts hist-GHG
    except:
        yearspan = None
        daexp_pairs = zip(sys.argv[1::2], sys.argv[2::2]) #e.g. python cmip6_model_members_in_common.py ts hist-nat ts hist-GHG
    model_members = cmip6_model_members_in_common(*daexp_pairs, yearspan=yearspan)
    cmip6_model_members_count(model_members)
    
    #savefig
    if len(sys.argv)>1 and 'savefig' in sys.argv[1:]:
        figname = __file__.replace('.py', f'.png')
        wysavefig(figname)
    tt.check(f'**Done**')
    #plt.show()
    
