# requries convert, montage tools in the OS
import os, glob
from .shell import run_shell


def _get_ifile(ifile_raw):
    '''get the actual ifile and ofile that can be used in the image manipulating functions'''
    if isinstance(ifile_raw, str):
        ifile = glob.glob(ifile_raw)
    else:
        ifile = ifile_raw
    ifile.sort()
    ifile = ' '.join(ifile)
    return ifile

def make_gif(ifile, ofile=None, delay=100, loop=0):
    '''make gif images from input files.'''
    # deal with input parameters
    ifile = _get_ifile(ifile)
    if ofile is None:
        ofile = 'mygif.gif'

    cmd = ' '.join(['convert',
        '-delay', str(delay),
        '-loop', str(loop),
        ifile,
        ofile])
    run_shell(cmd)

def montage(ifile, ofile=None, n_col=1):
    '''Merge multiple images into a single one.'''
    ifile = _get_ifile(ifile)
    if ofile is None:
        ofile = 'montage.pdf'
    # system montage command
    cmd = ' '.join(['montage',
        '-mode concatenate',
        '-tile', '{}x'.format(n_col),
        ifile,
        ofile])
    run_shell(cmd)
