#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Tue Oct 15 16:29:10 EDT 2019
#wy2024-03-20: use font awesome for dark/light switch
from datetime import datetime
import os.path, sys, os
import glob
#import xarray as xr, numpy as np, pandas as pd
#import matplotlib.pyplot as plt
from misc import intToRoman
#import filecmp #use filecmp_exclude_date instead
def filecmp_exclude_date(file1, file2):
    """compare two files to see if the content of them are the same, but exclude the date line (e.g  <li>2023-12-01</li>)"""
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        for line1,line2 in zip(f1,f2):
            if not line1.startswith('  <li>20') and line1 != line2: #compare all lines except that starting with '  <li>20'
                return False
    return True

def archive_file(ifile):
    """archive an old file"""
    mtime = os.path.getmtime(ifile)
    mtime_s = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')
    ifile_new = ifile + '.' + mtime_s
    os.rename(ifile, ifile_new)
    print('[archived]:', ifile, '->', ifile_new)


def main(html_file=None, model='FLOR', darkmode=True, modeler='wenchang'):
    """main function to generate the html file"""
    tformat = '%Y-%m-%d %H:%M:%S'
    time_stamp = datetime.now()
    date = time_stamp.strftime(tformat).split()[0]
    year = time_stamp.strftime(tformat).split('-')[0]
    if html_file is None: 
        html_file = f'{model}.by.{modeler}.html'
    html_file_tmp = html_file + '.tmp'
    #get expnames given $model
    rootdir = '/tigress/wenchang/MODEL_OUT'
    if modeler != 'wenchang': rootdir = os.path.join(rootdir, modeler) #e.g., modeler=gvecchi; rootdir = '/tigress/wenchang/MODEL_OUT/gvecchi'
    if model != 'FLOR': rootdir = os.path.join(rootdir, model)
    dirs = [d for d in os.listdir(rootdir) if os.path.isdir(os.path.join(rootdir, d))] #directories under $rootdir
    expnames = [d for d in dirs
        if len(glob.glob(f'{rootdir}/{d}/POSTP/*.atmos_month.nc')) > 0
        or len(glob.glob(f'{rootdir}/{d}/en*/POSTP/*.atmos_month.nc')) > 0
        ]
    if expnames:
        expnames.sort(key=lambda x: x.lower())
    else:
        if os.path.exists(html_file):
            archive_file(html_file)
        else:
            print(f'  **no experiments found for model {model} by {modeler}**')
        return
    #test the permission
    try:
        with open(html_file_tmp, 'w') as f:
            pass
    except PermissionError:
        print('[PermissionError]')
        return
    #start to write to file
    with open(html_file_tmp, 'w') as f: 
        #html head
        name  = ''.join([chr(n) for n in [87, 101, 110, 99, 104, 97, 110, 103, 32, 89, 97, 110, 103]]) + ', \u6768\u6587\u660C'
        html_theme = 'data-bs-theme="dark"' if darkmode else ''
        s = f'''<!doctype html>
<html {html_theme}>
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://wy2136.github.io/external/font-awesome-4.7.0/css/font-awesome.min.css">
    <title>{model} experiments, {name}</title>
    <style>body {{word-break: break-all}}</style>
  </head>
''' 
        #<link href="https://getbootstrap.com/docs/5.3/assets/css/docs.css" rel="stylesheet">
        f.write(s) #html head

        #body, title section
        model_type = 'AOGCM (atmosphere-ocean coupled)' if model.startswith('FLOR') or model.startswith('CM') \
            else 'AGCM (atmosphere-only)'
        #resolution
        if model.startswith('AM2.5C360'):
            resolution = '~25km atmos/land'
        elif model.startswith('AM2.5') or model.startswith('HIRAM'):
            resolution = '~50km atmos/land'
        elif model.startswith('AM4'):
            resolution = '~100km atmos/land'
        elif model.startswith('AM2.1'):
            resolution = '~200km atmos/land'
        elif model.startswith('FLOR'):
            resolution = '~50km atmos/land, 1 deg ocean/ice'
        elif model.startswith('CM2.1'):
            resolution = '~200km atmos/land, 1 deg ocean/ice'
        else:
            resolution = 'resoution NA'
        #model description link
        if '2.1' in model:
            model_link = 'https://github.com/mom-ocean/MOM4p1'
        elif model.startswith('FLOR') or model.startswith('AM2.5'):
            model_link = 'https://www.gfdl.noaa.gov/cm2-5-and-flor/'
        elif model.startswith('HIRAM'):
            model_link = 'https://www.gfdl.noaa.gov/hiram-quickstart/'
        elif model.startswith('AM4'):
            model_link = 'https://www.gfdl.noaa.gov/atmospheric-model/' 
        else:
            model_link = '#'
        s = f'''
<body>
<div class="container my-4">
<div>
<a href="index.html" class="btn btn-outline-secondary">models</a>
<i class="fa fa-adjust fa-lg" id="btnSwitch"></i>
</div>
<div class="card card-body border-0">
<h2>{model} experiments by {modeler}</h2>
<div class="text-muted">
  <li>Wenchang Yang</li>

  <li>Princeton University</li>
  <li>{date}</li>
<h5><span class="mt-3 mb-0 badge bg-info text-dark"><span><a href="{model_link}" class="text-dark">{model}</a></span></h5>
  <li>{model_type}</li>
  <li>{resolution}</li>
  <li>{rootdir}</li>
</div> <!-- text-muted -->
</div> <!-- card -->
'''
        f.write(s) #body starts, title section

        #main content
        f.write('\n')
        f.write('<div class="accordion" id="accordionExperiments">\n')
        n_exps = len(expnames)
        for ii,expname in enumerate(expnames, start=1):
            #output dir
            odir = os.path.join(rootdir, expname)
            workdirIndicator = ' * ' if 'scratch' in os.path.realpath(odir) else ''
            f.write('<div class="accordion-item">\n')
            #accordion-header
            if ii == 1: #can be set to be opposite when ii != 0
                #button_status = ''
                #collapse_content_status = 'show'
                button_status = 'collapsed'
                collapse_content_status = ''
            else:
                button_status = 'collapsed'
                collapse_content_status = ''

            s = f'''<h2 class="accordion-header">
 <button class="accordion-button {button_status}" type="button" data-bs-toggle="collapse" data-bs-target="#{expname.replace(".", "p")}Content">
[{ii:02d}; {model}] {expname} {workdirIndicator}
</button>
</h2>
'''
            f.write(s) #accordion-header
            #collapse
            f.write(f'<div id="{expname.replace(".", "p")}Content" class="accordion-collapse collapse {collapse_content_status}">\n')
            #f.write(f'<div class="card card-body font-monospace">\n')
            f.write(f'<div class="card card-body border-0 text-muted font-monospace">\n')
            #collapse content starts here
            #short description of the output data from readme file under the output dir
            #check if readme file exists
            _file = f'/tigress/wenchang/MODEL_OUT/wyreadme/README.{modeler}.{model}.{expname}'
            readme_file = _file if os.path.exists(_file) else None #usually prepared for experiments from other modelers
            readme_file = os.path.join(odir, 'README') if 'README' in os.listdir(odir) else readme_file #override the one from wy if exists
            readme_file = os.path.join(odir, 'README.md') if 'README.md' in os.listdir(odir) else readme_file #override readme if readme.md exists
            if readme_file is not None:
                f.write('<div>\n')
                with open(readme_file, 'r') as f_readme:
                    for line in f_readme:
                        f.write(f'{line}<br>\n')
                f.write('</div>\n')
                f.write('<br>\n')
            f.write(f'  <li>output dir: {odir}</li>\n')
            real_odir = os.path.realpath(odir)
            if real_odir != odir:
                f.write(f'  <li>real output dir: {os.path.realpath(odir)}</li>\n')
            #ensemble members
            ens = [d for d in os.listdir(odir) if d.startswith('en')]
            if ens:
                ens.sort()
                n_ens = len(ens)
                members = ', '.join([en[2:] for en in ens])
                f.write(f'  <li>{n_ens} ensemble members: {members}</li>\n')
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
                            f.write(f'  <li>{en}: {n_years} years, {year_start:04d}-{year_end:04d}</li>\n')
                        else:
                            f.write(f'  <li>{en}: {n_years} years, {year_start:04d}-{year_end:04d} (some years are missing!)</li>\n')
            #years for non-ensemble simulations
            if 'POSTP' in os.listdir(odir):
                postpdir = os.path.join(odir, 'POSTP')
                years = [int(ncfile[:4]) for ncfile in os.listdir(postpdir) if ncfile.endswith('atmos_month.nc')]
                years.sort()
                year_start, year_end = years[0], years[-1]
                n_years = len(years)
                if n_years == year_end-year_start+1:
                    f.write(f'  <li>{n_years} years: {year_start:04d}-{year_end:04d}</li>\n')
                else:
                    f.write(f'  <li>{n_years} years: {year_start:04d}-{year_end:04d} (some years are missing!)</li>\n')
            #TC analysis dir
            rootdir_tc = rootdir.replace('MODEL_OUT', 'analysis/TC')
            tcdir = os.path.join(rootdir_tc, expname)
            if os.path.exists(tcdir):
                    f.write(f'  <li>TC analysis dir: {tcdir}</li>\n')
            #experiment dir
            if 'exp' in os.listdir(odir):
                expdir = os.path.realpath(os.path.join(odir, 'exp'))
                f.write(f'  <li>experiment dir: {expdir}</li>\n')
                #check if readme file exists
                readme_file = 'README' if 'README' in os.listdir(expdir) else None
                readme_file = 'README.md' if 'README.md' in os.listdir(expdir) else readme_file #override readme if readme.md exists
                if readme_file is not None:
                    readme_path = os.path.join(expdir, readme_file)
                    f.write(f'  <li>{readme_file} of experiment ({readme_path})</li>\n')
                    #with open(readme_path, 'r') as f_readme:
                    #    for line in f_readme:
                    #        f.write(f'{line}<br>\n')
            #item ends
            s = f'''<!-- item ends -->
</div> <!-- card -->
</div> <!--accordion-collapse -->
</div> <!-- accordion-item -->
'''
            f.write(s) #item ends
            f.write('\n')
        f.write('</div> <!-- accordion -->\n')
            
        #bottom
        name  = ''.join([chr(n) for n in [87, 101, 110, 99, 104, 97, 110, 103, 89, 97, 110, 103]])
        s = f'''
<!-- <p class="text-center text-muted my-4">{name}</p> -->
<p class="text-center opacity-50 mt-4 mb-0"><img width="100px" src="https://avatars.githubusercontent.com/u/8202276"></p>
<div class="text-center text-muted">{intToRoman(int(year))}</div> <!-- text-center -->

</div> <!-- container -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
<script>
document.getElementById("btnSwitch").addEventListener("click",()=>{{
    if (document.documentElement.getAttribute("data-bs-theme") == "dark") {{
        document.documentElement.setAttribute("data-bs-theme","light")
    }}
    else {{
        document.documentElement.setAttribute("data-bs-theme","dark")
    }}
}})
</script>
</body>
</html>
'''
        f.write(s) #bottom
    if os.path.exists(html_file):
        #if filecmp.cmp(html_file_tmp, html_file, shallow=False):
        if filecmp_exclude_date(html_file_tmp, html_file):
            os.remove(html_file_tmp)
            print(f'  **NO update to {html_file}**')
        else:
            archive_file(html_file) 
            os.rename(html_file_tmp, html_file)
            print('[updated]:', html_file)
    else:
        os.rename(html_file_tmp, html_file)
        print('[saved]:', html_file)
    

if __name__ == '__main__':
    from misc import get_kws_from_argv
    tformat = '%Y-%m-%d %H:%M:%S'
    t0 = datetime.now()
    print('[start]:', t0.strftime(tformat))

    darkmode = False if 'light' in sys.argv else True
    #model = os.path.basename(os.getcwd())
    models_all_wenchang = ['FLOR', 'AM2.5', 'AM2.5C360', 'HIRAM',
        'AM4', 'AM4_urban',
        'CM2.1p1', 'AM2.1',
        'FLORktc', 'AM2.5ktc', 
        'FLORktc2', 'AM2.5ktc2', 'AM2.5C360ktc2', 'HIRAMktc2',
        ]
    models_in_work = [m+'_work' for m in models_all_wenchang] #model exps in workdir
    models_all_wenchang += models_in_work
    models_all_wenchang += [m+'_work' for m in ['AM4c192', 'AM4c192ub', 'AM4_github_20190805',]]
    #models used by other modelers
    #gvecchi
    models_all_gvecchi = ['FLOR', 'AM2.5', 'AM2.5C360', 'HIRAM']#, 'AM4_urban'] #no experiments for AM4_urban
    #gabe rios
    models_all_gr7610 = ['FLOR_work', 'AM2.5_work', 'AM2.5C360_work', 'HIRAM_work'] # see /tigress/MODEL_OUT/gr7610/
    #chenggong
    models_all_cw55 = ['AM2.5','HIRAM'] #
    models_in_work = [m+'_work' for m in models_all_cw55]
    models_all_cw55 += models_in_work
    #maya
    models_all_mvchung = ['FLOR',] #
    #bosong
    models_all_bosongz = ['AM2.5','HIRAM'] #
    #maofeng
    models_all_maofeng = ['FLOR','AM4', 'FLOR_work', 'AM4_work'] #
    #haozhe
    models_all_hh6765 = ['AM2.5_work','AM4_work', 'AM4mg2_work'] #

    model = get_kws_from_argv('model', default='AM2.1')
    modeler = get_kws_from_argv('modeler', default='wenchang')
    if model == 'all':
        if modeler == 'wenchang':
            models = models_all_wenchang
        elif modeler == 'gvecchi':
            models = models_all_gvecchi
        elif modeler == 'gr7610':
            models = models_all_gr7610
        elif modeler == 'cw55':
            models = models_all_cw55
        elif modeler == 'mvchung':
            models = models_all_mvchung
        elif modeler == 'bosongz':
            models = models_all_bosongz
        elif modeler == 'maofeng':
            models = models_all_maofeng
        elif modeler == 'hh6765':
            models = models_all_hh6765
        else:
            print('please provide a valid modeler')
            sys.exit()
    else:
        models = [model,]
    n_models = len(models)
    for ii,model in enumerate(models, start=1):
        print(f'{ii:02d} of {n_models:02d}:', model)
        main(model=model, darkmode=darkmode, modeler=modeler)            
        print()
    
    t1 = datetime.now()
    print('[end]:', t1.strftime(tformat))
    print('[total time]:', f'{(t1-t0).seconds:,} seconds')
