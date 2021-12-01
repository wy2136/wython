from .shell import run_shell

def img2mov(ifile, ofile, framerate=1):
    '''Convert images into a movie.

    ifile can be in a glob pattern, e.g. *.png.

    See: http://trac.ffmpeg.org/wiki/Create%20a%20video%20slideshow%20from%20images'''

    cmd = ' '.join(['ffmpeg',
        '-framerate {}'.format(framerate),
        '-pattern_type glob',
        '-i "{}"'.format(ifile),
        '-pix_fmt yuv420p',
        '{}'.format(ofile)])
    run_shell(cmd)
