#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Tue Oct 15 16:29:10 EDT 2019
if __name__ == '__main__':
    from misc.timer import Timer
    _t = Timer(f'start {__file__}')
import datetime
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

def write_list_of_files_to_html(fobj_html): 
    proj_name = os.path.basename(os.getcwd()) # name of the cwd
    #extension = '.nc'
    label = 'sort by mtime'
    ifiles = [f for f in os.listdir() if f != 'index.html']
    if ifiles:
        nfiles = len(ifiles)
        print(nfiles, 'files/dirs found')
        f = fobj_html
        f.write(f'<h3>{label}</h3>\n')
        f.write('<div class="list-group">\n')
        #https://stackoverflow.com/questions/19490015/how-to-get-modification-date-of-a-symlink-in-python
        getmtime = lambda x: max(os.stat(x).st_mtime, os.lstat(x).st_mtime ) # get the mtime of symlink or the realpath, whichever is later
        ifiles.sort(key=getmtime, reverse=True) # descending by file mtime
        for i,ifile in enumerate(ifiles, start=1):
            mtime = datetime.datetime.fromtimestamp( os.stat(ifile).st_mtime ).strftime('%Y-%m-%d_%H:%M:%S')#mtime of the realpath
            if ifile.endswith('.nc'): # get the file size information if ifile is netcdf file
                ifile_size = get_file_size(ifile)
                #s = f'<li class="list-group-item">[{nfiles-i+1:02d}] {ifile}: <a href="{ifile}">{ifile_size}</a></li>\n'
                s = f'<li class="list-group-item">[{mtime}] {ifile}: <a href="{ifile}">{ifile_size}</a></li>\n'
            elif ifile.endswith('.png'):
                #s = f'<p>{ifile}<br><a href="{ifile}"><img src="{ifile}" width="{img_width}"></a></p>\n'
                #s = f'<p><div class="caption"><strong>[{nfiles-i+1:02d}] {ifile}</strong></div><a href="{ifile}"><img src="{ifile}" class="img-responsive"></a></p>\n'
                s = f'<p><div class="caption">[{mtime}] {ifile}</strong></div><a href="{ifile}"><img src="{ifile}" class="img-responsive"></a></p>\n'
            elif ifile.endswith('.ipynb'):
                #s = f'<a class="list-group-item" href="https://nbviewer.jupyter.org/url/tigress-web.princeton.edu/%7Ewenchang/pub/{proj_name}/{ifile}">[{nfiles-i+1:02d}] {ifile}</a></li>\n'
                s = f'<a class="list-group-item" href="https://nbviewer.jupyter.org/url/tigress-web.princeton.edu/%7Ewenchang/{proj_name}/{ifile}">[{mtime}] {ifile}</a></li>\n'
            elif os.path.isdir(ifile):
                s = f'<a class="list-group-item" href="{ifile}">[{mtime}] {ifile} ></a>\n'
            else:
                #s = f'<a class="list-group-item" href="{ifile}">[{nfiles-i+1:02d}] {ifile}</a>\n'
                s = f'<a class="list-group-item" href="{ifile}">[{mtime}] {ifile}</a>\n'
            f.write(s)
        f.write('</div> <!-- list-group -->\n')
        f.write('\n')

def main(html_file='index.html', img_width=800):    
    tformat = '%Y-%m-%d %H:%M:%S'
    time_stamp = datetime.datetime.now()
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
        f.write(f'<title>{proj_name}, Wenchang Yang</title>\n')
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
        f.write('<li>Wenchang Yang</li>\n')
        f.write('<li>Department of Geosciences, Princeton University</li>\n')
        f.write(f'<li>{time_stamp.strftime(tformat)}</li>\n')
        f.write('</div> <!-- well -->\n')
        f.write('</div> <!-- page-header -->\n')
        f.write('\n')

        # recent files/dirs: sort by mtime (most recent first)
        write_list_of_files_to_html(f)

        # List of all files by name
        label = 'sort by name'
        ifiles = [ifile for ifile in os.listdir() if ifile != 'index.html']
        if ifiles:
            f.write(f'<h3>{label}</h3>\n')
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

        f.write('</div> <!-- container -->\n')
        f.write('</body>\n')
        f.write('</html>\n')
if __name__ == '__main__':
    cwd = os.getcwd()
    odir = '/tigress/wenchang/public_html/share'
    # create symlinks to odir for shared filesj
    sharedfiles = sys.argv[1:]
    for ifile in sharedfiles:
        ifile_full = os.path.abspath(ifile)
        ofile = os.path.join( odir, os.path.basename(ifile) )
        if os.path.exists(ofile):
            print('[exists]:', ofile)
        else:
            os.symlink(ifile_full, ofile)
            print('[link created]:', ofile, '->', ifile_full)

    # generate index.html file under odir
    os.chdir(odir)
    main()            
    print('files shared at:\nhttp://tigress-web.princeton.edu/~wenchang/share/')
    os.chdir(cwd)
    
    _t.check(f'end {__file__}')
