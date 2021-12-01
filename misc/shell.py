import os

def run_shell(*args):
    '''Run shell command by calling os.system.
    *Parameters*:
        args: str, or list of str.'''
    cmd = ' '.join(list(args))
    s = os.system(cmd)
    if s == 0:# success
        print('[OK]: {}'.format(cmd))
    else:
        raise Exception('\t[Error of Shell]: {}'.format(cmd))
