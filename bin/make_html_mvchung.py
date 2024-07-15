#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Tue Oct 15 16:29:10 EDT 2019
from datetime import datetime
import os.path, sys, os
import glob
#import xarray as xr, numpy as np, pandas as pd
#import matplotlib.pyplot as plt

#html_file = 'index.html'
#img_width = 800
#proj_name = os.path.basename(os.getcwd()) # name of the cwd

def get_file_size(ifile):
    s = os.path.getsize(ifile) # an integer
    if s<1e3:
        return f'{s}B'
    elif s<1e6:
        return f'{s/1e3:.1f}K'
    elif s<1e9:
        return f'{s/1e6:.1f}M'
    else:
        return f'{s/1e9:.1f}G'

def containing_files(extension):
    return len(glob.glob(f'*{extension}')) > 0

def write_list_of_files_to_html(fobj_html, extension, label): 
    proj_name = os.path.basename(os.getcwd()) # name of the cwd
    #extension = '.nc'
    #label = 'NC Files'
    ifiles = glob.glob(f'*{extension}')
    if ifiles:
        nfiles = len(ifiles)
        print(nfiles, label, 'found')
        f = fobj_html
        label_id = '_'.join(label.split(' '))
        f.write(f'<h3 id="{label_id}">{label}</h3>\n')
        f.write('<div class="list-group">\n')
        ifiles.sort(key=lambda x: x[:x.index(extension)].lower())# take extension out before sorting
        for i,ifile in enumerate(ifiles, start=1):
            if ifile.endswith('.nc'): # get the file size information if ifile is netcdf file
                ifile_size = get_file_size(ifile)
                #s = f'<li class="list-group-item">[{nfiles-i+1:02d}] {ifile}: <a href="{ifile}">{ifile_size}</a></li>\n'
                s = f'<li class="list-group-item">[{i:02d}/{nfiles:02d}] {ifile}: <a href="{ifile}">{ifile_size}</a></li>\n'
            elif ifile.endswith('.png'):
                #s = f'<p>{ifile}<br><a href="{ifile}"><img src="{ifile}" width="{img_width}"></a></p>\n'
                #s = f'<p><div class="caption"><strong>[{nfiles-i+1:02d}] {ifile}</strong></div><a href="{ifile}"><img src="{ifile}" class="img-responsive"></a></p>\n'
                s = f'<p><div class="caption"><strong>[{i:02d}/{nfiles:02d}] {ifile}</strong></div><a href="{ifile}"><img src="{ifile}" class="img-responsive"></a></p>\n'
            elif ifile.endswith('.ipynb'):
                #s = f'<a class="list-group-item" href="https://nbviewer.jupyter.org/url/tigress-web.princeton.edu/%7Ewenchang/pub/{proj_name}/{ifile}">[{nfiles-i+1:02d}] {ifile}</a></li>\n'
                s = f'<a class="list-group-item" href="https://nbviewer.jupyter.org/url/tigress-web.princeton.edu/%7Emvchang/{proj_name}/{ifile}">[{i:02d}/{nfiles:02d}] {ifile}</a></li>\n'
            else:
                #s = f'<a class="list-group-item" href="{ifile}">[{nfiles-i+1:02d}] {ifile}</a>\n'
                s = f'<a class="list-group-item" href="{ifile}">[{i:02d}/{nfiles:02d}] {ifile}</a>\n'
            f.write(s)
        f.write('</div> <!-- list-group -->\n')
        f.write('\n')

def main(html_file='index.html', img_width=800):    
    tformat = '%Y-%m-%d %H:%M:%S'
    time_stamp = datetime.now()
    print('[cwd]:', os.getcwd())
    proj_name = os.path.basename(os.getcwd()) # name of the cwd
    # navigation construction
    cwd_levels = os.getcwd().split('/')
    nav = []
    if 'analysis' in cwd_levels:
        home_name = 'analysis'
    elif 'pub' in cwd_levels:
        home_name = 'pub'
    else:
        home_name = None
    if home_name in cwd_levels:
        path_levels = cwd_levels[cwd_levels.index(home_name):]
    else:
        path_levels = []
    if path_levels:
        for i,name in enumerate(path_levels[-1::-1], start=1):
            href = '../'*(i-1)
            nav.append(f'<a href="{href}">{name}</a>') 
        nav[-1] = nav[-1].replace(home_name, 'Home')
        nav = '/'.join(nav[-1::-1])
            
    try:
        with open(html_file, 'w') as f:
            pass
    except PermissionError:
        print('[PermissionError]')
        return
    with open(html_file, 'w') as f: 
        f.write('<!DOCTYPE html>\n')
        f.write('<html>\n')
        f.write('<head>\n')
        s = ''.join([chr(n) for n in [87, 101, 110, 99, 104, 97, 110, 103, 32, 89, 97, 110, 103]]) + ', \u6768\u6587\u660C'
        f.write(f'<title>{proj_name}, {s}</title>\n')
        f.write('<meta charset="utf-8">\n')
        f.write('<meta name="viewport" content="width=device-width, initial-scale=1.0">\n')
        f.write('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">\n')
        #f.write('<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.0/jquery.min.js"></script>\n')
        #f.write('<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>\n')
        #f.write('<style>body {font-family: Helvetica, Arial, sans-serif} a {text-decoration: none}</style>\n')
        f.write('<style>body {word-break: break-all}</style>\n')
        f.write('</head>\n')
        f.write('\n')

        f.write('<body>\n')
        f.write('<div class="container">\n')
        # title section
        f.write('<div class="page-header">\n')
        f.write('<div class="well">\n')
        if nav:
            f.write(f'{nav}\n')
        f.write(f'<h2>{proj_name}</h2>\n')
        #f.write('<li>Wenchang Yang</li>\n')
        f.write('<li>Maya V. Chung</li>\n')
        f.write('<li>Department of Geosciences, Princeton University</li>\n')
        f.write(f'<li>{time_stamp.strftime(tformat)}</li>\n')
        f.write('</div> <!-- well -->\n')
        
        f.write('<div class="list-group">\n')
        if [ifile for ifile in glob.glob('*') if os.path.isdir(ifile)]:#sub dirs exist under pwd
            f.write(f'<a class=" list-group-item list-group-item-text" href="#Directories">Directories</a>\n')
        for extension,label in zip(['.png', '.py', '.pdf', '.ipynb', '.nc', '.csv'],
            ['Figures', 'Python Files', 'PDFs', 'Notebooks', 'NC Files', 'CSV Files']):
            if containing_files(extension):
                label_id = '_'.join(label.split(' '))
                f.write(f'<a class=" list-group-item list-group-item-text" href="#{label_id}">{label}</a>\n')
        f.write(f'<a class=" list-group-item list-group-item-text" href="#All_Files">All Files</a>\n')
        f.write(f'<a class=" list-group-item list-group-item-text" href="#All_Files_by_Time">All Files by Time</a>\n')
        f.write('</div> <!-- list-group -->\n')
        f.write('\n')
            
        f.write('</div> <!-- page-header -->\n')
        f.write('\n')

        # List of directories
        label = 'Directories'
        ifiles = [ifile for ifile in glob.glob('*') if os.path.isdir(ifile)]
        if ifiles:
            f.write(f'<h3 id="{label}">{label}</h3>\n')
            f.write('<div class="list-group">\n')
            ifiles.sort(key=lambda x: x.lower())
            if os.path.basename(os.getcwd()) in ('WWA',):
                ifiles = ifiles[-1::-1] #reverse ifiles in some cases
            for ifile in ifiles:
                f.write(f'<a class=" list-group-item list-group-item-text" href="{ifile}">{ifile}/</a>\n')
            f.write('</div> <!-- list-group -->\n')
            f.write('\n')

        # figures
        write_list_of_files_to_html(f, extension='.png', label='Figures')

        # python scripts 
        write_list_of_files_to_html(f, extension='.py', label='Python Files')

        # pdf files
        write_list_of_files_to_html(fobj_html=f, extension='.pdf', label='PDFs')

        # jupyter notebooks
        write_list_of_files_to_html(f, extension='.ipynb', label='Notebooks')
    
        # python scripts
        # write_list_of_files_to_html(fobj_html=f, extension='.py', label='Python Scripts')
    
        # shell scripts
        # write_list_of_files_to_html(fobj_html=f, extension='.sh', label='Shell Scripts')

        # netcdf file
        write_list_of_files_to_html(fobj_html=f, extension='.nc', label='NC Files')

        # csv file
        write_list_of_files_to_html(fobj_html=f, extension='.csv', label='CSV Files')

        # List of all files
        label = 'All Files'
        ifiles = [ifile for ifile in glob.glob('*') if not os.path.isdir(ifile)]
        if ifiles:
            f.write(f'<h3 id="All_Files">{label}</h3>\n')
            f.write('<div class="list-group">\n')
            ifiles.sort(key=lambda x: '.'.join(x.split('.')[:-1]).lower() if '.' in x else x.lower())# sort by file names without the extension
            for ifile in ifiles:
                if ifile.endswith('.nc'):
                    ifile_size = get_file_size(ifile)
                    s = f'<li class="list-group-item">{ifile}: <a href="{ifile}">{ifile_size}</a></li>\n'
                else:
                    s = f'<a class="list-group-item" href="{ifile}">{ifile}</a>\n'
                f.write(s)
            f.write('</div> <!-- list-group -->\n')
            f.write('\n')

        # List of all files by modified time
        label = 'All Files by Time'
        ifiles = [ifile for ifile in glob.glob('*') if not os.path.isdir(ifile)]
        if ifiles:
            f.write(f'<h3 id="All_Files_by_Time">{label}</h3>\n')
            f.write('<div class="list-group">\n')
            #ifiles.sort(key=lambda x: '.'.join(x.split('.')[:-1]).lower() if '.' in x else x.lower())# sort by file names without the extension
            ifiles.sort(key=lambda x: os.path.getmtime(x), reverse=True)# sort by file modified time 
            for ifile in ifiles:
                if ifile.endswith('.nc'):
                    ifile_size = get_file_size(ifile)
                    s = f'<li class="list-group-item">{ifile}: <a href="{ifile}">{ifile_size}</a></li>\n'
                else:
                    s = f'<a class="list-group-item" href="{ifile}">{ifile}</a>\n'
                f.write(s)
            f.write('</div> <!-- list-group -->\n')
            f.write('\n')


        #s = '\u00a9' + ''.join([chr(n) for n in [87, 101, 110, 99, 104, 97, 110, 103, 89, 97, 110, 103]])
        #s = ''.join([chr(n) for n in [87, 101, 110, 99, 104, 97, 110, 103, 89, 97, 110, 103]])
        s = 'Maya V. Chung' 
        f.write(f'<p class="text-center text-muted">{s}</p>')
        f.write('</div> <!-- container -->\n')
        f.write('</body>\n')
        f.write('</html>\n')
if __name__ == '__main__':
    tformat = '%Y-%m-%d %H:%M:%S'
    t0 = datetime.now()
    print('[start]:', t0.strftime(tformat))

    main()            
    
    t1 = datetime.now()
    print('[end]:', t1.strftime(tformat))
    print('[total time]:', f'{(t1-t0).seconds:,} seconds')
