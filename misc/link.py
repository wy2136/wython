#!/usr/bin/env python
import os, sys

def link_file(ifile, opath, options='-f'):
    cmd = ' '.join([
        'ln',
        options,
        ifile,
        opath
    ])
    status = os.system(cmd)
    if status == 0:
        print('[OK]: {}'.format(cmd))
    else:
        print('\t[**Error**]: {}'.format(cmd))

if __name__ == '__main__':
    ifile = sys.argv[1]
    opath = sys.argv[2]
    link_file(ifile, opath)
