#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Tue Oct 15 16:29:10 EDT 2019
from datetime import datetime
import os.path, sys, os
import glob
#import xarray as xr, numpy as np, pandas as pd
#import matplotlib.pyplot as plt
from misc import intToRoman

def main(html_file='index.html', darkmode=True, rootdir=None):
    """main function to generate the html file"""
    tformat = '%Y-%m-%d %H:%M:%S'
    time_stamp = datetime.now()
    date = time_stamp.strftime(tformat).split()[0]
    year = time_stamp.strftime(tformat).split('-')[0]
    #get rootdir
    if rootdir is None:
        rootdir = os.getcwd()
    #get files and dirs under the rootdir
    ifiles = [ifile for ifile in os.listdir(rootdir) if not os.path.isdir(os.path.join(rootdir, ifile))]
    if ifiles: ifiles.sort()
    idirs = [idir for idir in os.listdir(rootdir) if os.path.isdir(os.path.join(rootdir, idir))]
    if idirs: idirs.sort()
    #test the permission
    try:
        with open(html_file, 'w') as f:
            pass
    except PermissionError:
        print('[PermissionError]')
        return
    #start to write to file
    with open(html_file, 'w') as f: 
        #html head
        name  = ''.join([chr(n) for n in [87, 101, 110, 99, 104, 97, 110, 103, 32, 89, 97, 110, 103]]) + ', \u6768\u6587\u660C'
        html_theme = 'data-bs-theme="dark"' if darkmode else ''
        s = f'''<!doctype html>
<html {html_theme}>
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <title>{rootdir}, {name}</title>
    <style>body {{word-break: break-all}}</style>
  </head>
''' 
        f.write(s) #html head

        #body, title section
        s = f'''
<body>
<div class="container my-4">
<div>
<a href="http://tigress-web.princeton.edu/~wenchang/pub/" class="btn btn-outline-secondary">home</a>
<button type="button" class="btn btn-outline-secondary" id="btnSwitch">dark/light switch</button>
</div>
<div class="card card-body border-0">
<h2>{rootdir}</h2>
<div class="text-muted">
  <li>Wenchang Yang</li>
  <li>Princeton University</li>
  <li>{date}</li>
</div> <!-- text-muted -->
</div> <!-- card -->
'''
        f.write(s) #body starts, title section

        #main content
        f.write('\n')
        f.write('<div class="list-group">\n')
        for idir in idirs:
            f.write(f'<a class=" list-group-item list-group-item-text" href="{idir}">{idir}/</a>\n')
        for ifile in ifiles:
            f.write(f'<a class=" list-group-item list-group-item-text" href="{ifile}">{ifile}</a>\n')
        f.write('</div> <!-- list-group -->\n')
            
            
        #bottom
        name  = ''.join([chr(n) for n in [87, 101, 110, 99, 104, 97, 110, 103, 89, 97, 110, 103]])
        s = f'''
<!-- <p class="text-center text-muted my-4">{name}</p> -->
<p class="text-center mt-4 mb-0 opacity-50"><img width="100px" src="https://avatars.githubusercontent.com/u/8202276"></p>
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
</script>
</body>
</html>
'''
        f.write(s) #bottom
    print('[saved]:', html_file)

if __name__ == '__main__':
    #from misc import get_kws_from_argv
    tformat = '%Y-%m-%d %H:%M:%S'
    t0 = datetime.now()
    print('[start]:', t0.strftime(tformat))

    darkmode = False if 'light' in sys.argv else True
    main(darkmode=darkmode)            
    
    t1 = datetime.now()
    print('[end]:', t1.strftime(tformat))
    print('[total time]:', f'{(t1-t0).seconds:,} seconds')
