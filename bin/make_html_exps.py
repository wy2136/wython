#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Tue Oct 15 16:29:10 EDT 2019
from datetime import datetime
import os.path, sys, os
import glob
#import xarray as xr, numpy as np, pandas as pd
#import matplotlib.pyplot as plt

#html_file = 'index.html'
#model = 'FLOR'

def main(html_file=None, model='FLOR', darkmode=True):    
    if html_file is None: html_file = f'{model}.html'
    tformat = '%Y-%m-%d %H:%M:%S'
    time_stamp = datetime.now()
    try:
        with open(html_file, 'w') as f:
            pass
    except PermissionError:
        print('[PermissionError]')
        return
    with open(html_file, 'w') as f: 
        #get expnames given $model
        rootdir = '/tigress/wenchang/MODEL_OUT'
        if model != 'FLOR': rootdir = os.path.join(rootdir, model)
        expnames = [d for d in os.listdir(rootdir) if os.path.isdir(os.path.join(rootdir, d))] #directories under $rootdir
        expnames = [d for d in expnames if d.endswith('PE') 
            or d.startswith('Agung') or d.startswith('Chichon') or d.startswith('Pinatubo') or d.startswith('StMaria')
            or ('extend' in d and 'rerun' not in d)
            ]
        expnames.sort()
        f.write('<!DOCTYPE html>\n')
        if darkmode:
            f.write('<html data-bs-theme="dark">\n')
        else:
            f.write('<html>\n')
        #head
        f.write('<head>\n')
        s = ''.join([chr(n) for n in [87, 101, 110, 99, 104, 97, 110, 103, 32, 89, 97, 110, 103]]) + ', \u6768\u6587\u660C'
        f.write(f'<title>{model} experiments, {s}</title>\n')
        f.write('<meta charset="utf-8">\n')
        f.write('<meta name="viewport" content="width=device-width, initial-scale=1.0">\n')
        #f.write('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">\n')
        #f.write('<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.0/jquery.min.js"></script>\n')
        #f.write('<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>\n')
        #f.write('<style>body {font-family: Helvetica, Arial, sans-serif} a {text-decoration: none}</style>\n')
        #f.write('<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>\n')
        #f.write('<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@3.4.1/dist/css/bootstrap.min.css" integrity="sha384-HSMxcRTRxnN+Bdg0JdbxYKrThecOKuH5zCYotlSAcp1+c8xmyTe9GYg1l9a69psu" crossorigin="anonymous">\n')
        #f.write('<script src="https://cdn.jsdelivr.net/npm/bootstrap@3.4.1/dist/js/bootstrap.min.js" integrity="sha384-aJ21OjlMXNL5UyIl/XNwTMqvzeRMZH2w8c5cRVpzpU8Y5bApTppSuUkhZXN0VxHd" crossorigin="anonymous"></script>\n')
        #f.write('<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css" integrity="sha384-xOolHFLEh07PJGoPkLv1IbcEPTNtaed2xpHsD9ESMhqIYd0nLMwNLD69Npy4HI+N" crossorigin="anonymous">\n')
        f.write('<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">\n')
        f.write('<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin="anonymous"></script>\n')
        f.write('<style>body {word-break: break-all}</style>\n')
        f.write('</head>\n')
        f.write('\n')

        #body
        f.write('<body>\n')
        f.write('<div class="container">\n')
        # title section
        #f.write('<br>\n')
        f.write('<div class="page-header">\n')
        f.write('<div class="card card-body my-4 border-0">\n')
        f.write(f'<h2>{model} experiments</h2>\n')
        f.write(f'<li>{rootdir}</li>\n')
        f.write('<li>Wenchang Yang</li>\n')
        f.write('<li>Department of Geosciences, Princeton University</li>\n')
        f.write(f'<li>{time_stamp.strftime(tformat)}</li>\n')
        f.write('</div> <!-- card -->\n')
        f.write('</div> <!-- page-header -->\n')
        #f.write('<br>\n')
        f.write('\n')
        
        #main content
        f.write('<div class="list-group">\n')
        for expname in expnames:
            f.write(f'<a class="list-group-item list-group-item-text" data-bs-toggle="collapse" href="#{expname}Content" role="button" aria-expanded="false" aria-controls="{expname}Content">{expname}</a>\n')
            f.write(f'<div class="collapse" id="{expname}Content">\n')
            f.write(f'  <div class="card card-body border-0 text-muted font-monospace">\n') #WY
            #output dir
            odir = os.path.join(rootdir, expname)
            f.write(f'    <li>output dir: {odir}</li>\n')
            #ensemble members
            ens = [d for d in os.listdir(odir) if d.startswith('en')]
            if ens:
                ens.sort()
                n_ens = len(ens)
                members = ', '.join([en[2:] for en in ens])
                f.write(f'    <li>{n_ens} ensemble members: {members}</li>\n')
                #years for each ensemble member
                for en in ens:
                    odir_en = os.path.join(odir, en) #output dir for each ensemble member
                    if 'POSTP' in os.listdir(odir_en):
                        postpdir = os.path.join(odir_en, 'POSTP')
                        years = [int(ncfile[:4]) for ncfile in os.listdir(postpdir) if ncfile.endswith('atmos_month.nc')]
                        years.sort()
                        year_start, year_end = years[0], years[-1]
                        n_years = len(years)
                        if n_years == year_end-year_start+1:
                            f.write(f'    <li>{en}: {n_years} years, {year_start:04d}-{year_end:04d}</li>\n')
                        else:
                            f.write(f'    <li>{en}: {n_years} years, {year_start:04d}-{year_end:04d} (some years are missing!)</li>\n')
            #years for non-ensemble simulations
            if 'POSTP' in os.listdir(odir):
                postpdir = os.path.join(odir, 'POSTP')
                years = [int(ncfile[:4]) for ncfile in os.listdir(postpdir) if ncfile.endswith('atmos_month.nc')]
                years.sort()
                year_start, year_end = years[0], years[-1]
                n_years = len(years)
                if n_years == year_end-year_start+1:
                    f.write(f'    <li>{n_years} years: {year_start:04d}-{year_end:04d}</li>\n')
                else:
                    f.write(f'    <li>{n_years} years: {year_start:04d}-{year_end:04d} (some years are missing!)</li>\n')
            #TC analysis dir
            rootdir_tc = rootdir.replace('MODEL_OUT', 'analysis/TC')
            tcdir = os.path.join(rootdir_tc, expname)
            if os.path.exists(tcdir):
                    f.write(f'    <li>TC analysis dir: {tcdir}</li>\n')
            #experiment dir
            if 'exp' in os.listdir(odir):
                expdir = os.path.realpath(os.path.join(odir, 'exp'))
                f.write(f'    <li>experiment dir: {expdir}</li>\n')
                #check if readme file exists
                readme_file = 'README' if 'README' in os.listdir(expdir) else None
                readme_file = 'README.md' if 'README.md' in os.listdir(expdir) else readme_file #override readme if readme.md exists
                if readme_file is not None:
                    readme_path = os.path.join(expdir, readme_file)
                    with open(readme_path, 'r') as f_readme:
                        f.write(f'    <li>{readme_file} ({readme_path})</li>\n')
                        for line in f_readme:
                            f.write(f'{line}<br>\n')
            f.write(f'  </div> <!-- card -->\n')
            f.write(f'</div> <!-- collapse -->\n')
            f.write('\n')
        f.write('</div> <!-- list-group -->\n')
        f.write('\n')
            

        #s = '\u00a9' + ''.join([chr(n) for n in [87, 101, 110, 99, 104, 97, 110, 103, 89, 97, 110, 103]])
        s = ''.join([chr(n) for n in [87, 101, 110, 99, 104, 97, 110, 103, 89, 97, 110, 103]])
        f.write(f'<p class="text-center text-muted my-4">{s}</p>\n')
        f.write('</div> <!-- container -->\n')
        f.write('</body>\n')
        f.write('</html>\n')
if __name__ == '__main__':
    from misc import get_kws_from_argv
    tformat = '%Y-%m-%d %H:%M:%S'
    t0 = datetime.now()
    print('[start]:', t0.strftime(tformat))

    darkmode = False if 'light' in sys.argv else True
    #model = os.path.basename(os.getcwd())
    models_all = ['FLOR', 'AM2.5', 'AM2.5C360', 'HIRAM',
        'AM4', 'AM4_urban',
        'CM2.1p1', 'AM2.1',
        'FLORktc', 'AM2.5ktc', 
        'FLORktc2', 'AM2.5ktc2', 'AM2.5C360ktc2', 'HIRAMktc2',
        ]
    model = get_kws_from_argv('model', default='FLOR')
    if model == 'all':
        models = models_all
    else:
        models = [model,]
    n_models = len(models)
    for ii,model in enumerate(models, start=1):
        print(f'{ii:02d} of {n_models:02d}:', model)
        main(model=model, darkmode=darkmode)            
        print()
    
    t1 = datetime.now()
    print('[end]:', t1.strftime(tformat))
    print('[total time]:', f'{(t1-t0).seconds:,} seconds')
