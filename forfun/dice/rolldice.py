#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Fri Jul 23 16:27:08 EDT 2021
#import xarray as xr, numpy as np, pandas as pd
import os.path
import matplotlib.pyplot as plt
#more imports
#from PIL import Image 
import random
from matplotlib import image
#
#
#start from here

dice = range(1,6+1)
idir = os.path.dirname(__file__)
while True:
    n = random.choice(dice)
    ifile = os.path.join(idir, f'dice-{n}.jpg')
    #img = Image.open(ifile)
    #img.show()
    #with Image.open(ifile) as img:
    #    img.show()
    plt.ion()
    plt.imshow(image.imread(ifile))
    plt.axis('off')
    #plt.show()
    print(f'Your number is {n}')
    s = input(f'Press Return to continue (or type q and press Return to quit):')
    plt.close()
    if s == 'q':
        break

 
    
