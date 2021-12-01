# -*- coding: utf-8 -*-
"""
Created on Tue Apr 15 15:57:01 2014

@author: yang
"""
from __future__ import print_function

import os
# import tempfile

# pdf
def eps2pdf(epsfile):
    if not epsfile.endswith('.eps'):
        epsfile += '.eps'
    os.system('epstopdf ' + epsfile)
    # os.remove(epsfile)
def pdf2png(pdffile,dpi=100,pngfile=None):
    if not pdffile.endswith('.pdf'):
        pdffile += '.pdf'
    if pngfile is None:
        pngfile = pdffile.replace('.pdf','.png')
    elif not pngfile.endswith('.png'):
        pngfile +=  '.png'
    os.system('convert -density ' + str(dpi) + 'x' + str(dpi)
                + pdffile.rjust(len(pdffile)+1) + pngfile.rjust(len(pngfile)+1))
def pdf2jpg(pdffile,dpi=100,jpgfile=None):
    if not pdffile.endswith('.pdf'):
        pdffile += '.pdf'
    if jpgfile is None:
        jpgfile = pdffile.replace('.pdf','.jpeg')
    elif not jpgfile.endswith('.jpeg'):
        jpgfile +=  '.jpeg'
    os.system('convert -density ' + str(dpi) + 'x' + str(dpi)
                + pdffile.rjust(len(pdffile)+1) + jpgfile.rjust(len(jpgfile)+1))
def get_size(pdffile):
    pdfinfo = os.popen('identify -verbose ' + pdffile).read()
    i = pdfinfo.find('Print size')
    j = pdfinfo.find('Units')
    pdfsizeString = pdfinfo[i+12:j-2]
    # print pdfsizeString
    sizeList = pdfsizeString.split('x')
    width = sizeList[0]
    height = sizeList[-1]
    print (width, height)
    return float(width),float(height)

def crop(pdffile, margin=5):
     os.system('pdfcrop -margin ' + str(margin) + ' ' + pdffile + ' ' + pdffile)
     return pdffile

def tag(pdffile,labelString,new_pdffile=None):
    if not pdffile.endswith('.pdf'):
        pdffile += '.pdf'
    if new_pdffile is None:
        new_pdffile = pdffile
    if not new_pdffile.endswith('.pdf'):
        new_pdffile += '.pdf'
    pdfwidth,pdfheight = get_size(pdffile)
    # tex file
    texList = [\
    r'\documentclass[12pt]{article}',\
    r'\usepackage{graphicx}',\
    r'\usepackage[margin=0in, paperwidth=' + str(pdfwidth) + 'in, paperheight=' + str(pdfheight) + 'in]{geometry}',\
    r'\begin{document}',\
    r'\begin{figure}[ht]',\
    r'\makebox[0pt][l]{\raisebox{-\totalheight}{\includegraphics[width=\textwidth]{' + pdffile + '}}}',\
    r'\raisebox{-\totalheight}{\large \bfseries  ' + labelString + ')}',\
    r'  \end{figure}',\
    r'  \end{document}']
    # tmp = tempfile.NamedTemporaryFile()
    # tmp_file = tmp.name
    # tmp_file = 'temp'
    # tmp_dir = os.path.dirname(tmp_file)
    tmp_dir = '/Users/wenchang/Downloads'
    tmp_file = tmp_dir + '/temp'
    # tex_file = tmp_file + '.tex'
    tex_file = tmp_dir + '/temp.tex'
    with open(tex_file,'w') as f:
        for line in texList:
            f.write(line+'\n')
    # pdflatex
    os.system('pdflatex -interaction=batchmode -output-directory='
             + tmp_dir + ' ' + tex_file)
    # pdfcrop
    # crop(tmp_file + '.pdf')
    # replace the original file by temp.pdf
    os.system('mv  ' + tmp_file + '.pdf ' + new_pdffile)
    # remove temp files
    # print tmp_file
    # tmp.close()
    # os.system('rm ' + tmp_file + '*')
    print ('---->',pdffile, 'has been tagged',labelString,' and saved into')
    print ('---->',new_pdffile)

def montage(pdffiles,montageName='Fig_montage.pdf',columns=1, ifTag=False):
    if ifTag==True:
        new_pdffiles = []
        for i,pdffile in enumerate(pdffiles):
            if not pdffile.endswith('.pdf'):
                pdffile = ''.join([pdffile,'.pdf'])
            theTag = chr(ord('a')+i)
            new_pdffile = pdffile.replace('.pdf','_tagged.pdf')
            tmp_dir = '/Users/wenchang/Downloads/temp'
            new_pdffile = os.path.join(tmp_dir,os.path.basename(new_pdffile))
            tag(pdffile,theLabel,new_pdffile=new_pdffile)
            new_pdffiles.append(new_pdffile)
    else:
        new_pdffiles = pdffiles
    figwidth = 0.99/columns
    f = open('/Users/wenchang/Downloads/temp.tex','w')
    texList = [\
    r'\documentclass[12pt]{article}',\
    r'\usepackage{graphicx}',\
    r'\usepackage[captionskip=0pt]{subfig}',\
    r'\usepackage[margin=0in, paperwidth=6.5in, paperheight=11in]{geometry}',\
    r'\linespread{0.1}',\
    r'\newcommand{\figwidth}{0.99}',\
    r'\newcommand{\figwidthLast}{0.99}',\
    r'\begin{document}',\
    r'\pagestyle{empty}',\
    r'\captionsetup[figure]{labelformat=empty, font=large, margin=.05\textwidth}',\
    r'\begin{figure}[h]',\
    r'\centering']
    for line in texList:
        f.write(line + '\n')
    for i,pdffile in enumerate(new_pdffiles):
        line = r'\captionsetup[subfloat]{position=bottom, labelformat=empty, font=Large, singlelinecheck=true}'
        f.write(line + '\n')
        if not pdffile.endswith('.pdf'):
            pdffile = pdffile + '.pdf'
        line = r'\subfloat[]{\includegraphics[width=' + str(figwidth) +  r'\textwidth]{' + pdffile + '}}'
        f.write(line + '\n')
        if (i+1)%columns==0:
            line = r'\newline'
            f.write(line + '\n')
    texList = [\
    r'\end{figure}',\
    r'\end{document}']
    for line in texList:
        f.write(line + '\n')
    f.close()
    os.system('pdflatex -interaction=batchmode -output-directory=/Users/wenchang/Downloads \
            /Users/wenchang/Downloads/temp.tex')
    crop('/Users/wenchang/Downloads/temp.pdf')
    os.system('mv /Users/wenchang/Downloads/temp.pdf ' + montageName)
    # os.system('rm temp.*')

    # remove the tagged files
    if ifTag==True:
        for taggedFile in new_pdffiles:
            os.remove(taggedFile)
    #
class Pdf(object):
    '''A pdf object that can be nicely displayed in IPython Notebook. '''
    def __init__(self, fname, width=600):
        width_orig, height_orig = get_size(pdffile=fname)
        if width is None:
            width_new, height_new = width_orig, height_orig
        else:
            width_new, height_new = width, width/width_orig*height_orig*1.1
        self.fname = fname
        self.width = width_new
        self.height = height_new

    def _repr_html_(self):
        return '<iframe src={0} width={1} height={2} style="margin:0"></iframe>'.format(
            self.fname, self.width, self.height
        )

    def _repr_latex_(self):
        return r'\includegraphics[width=1.0\textwidth]{{{0}}}'.format(
            self.fname
        )
