import time
import matplotlib.pyplot as plt

def end_interactive(fig=None, sleep_time=.5):
    '''End the interactive mode in jupyter notebook 
    when the `notebook` backend is used (i.e. %matplotlib notebook).
    See https://github.com/matplotlib/matplotlib/issues/6071 for the discussion.'''
    if fig is None:
        fig = plt.gcf()
    fig.canvas.draw()
    time.sleep(sleep_time)
    plt.close(fig)
