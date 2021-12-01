import os

def _run_shell(cmd):
    '''Run shell command by calling os.system.

    Pamrameters:
    ------------
    cmd: the command string, e.g. 'ls -lh'. '''
    s = os.system(cmd)
    if s == 0:# success
        print('[OK]: {}'.format(cmd))
    else:
        raise Exception('\n[Shell Error]: {}'.format(cmd))
def run_shell(*args):
    '''The abstract of nco commands'''
    cmd = ' '.join(list(args))
    _run_shell(cmd)
def cdo(*args):
    '''The abstract of cdo commands'''
    cmd = 'cdo ' + ' '.join(list(args))
    _run_shell(cmd)
