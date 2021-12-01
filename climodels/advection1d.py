#!/usr/bin/env python
import numpy as np
from numpy import pi
import matplotlib.pyplot as plt

class Advection1D:
    def __init__(self, Lx=1., nx=51, tmax=2., dt=0.01, c=1., u0=None):
        dx = Lx/(nx-1)
        nt = int(tmax/dt)
        if u0 is None:
            u0 = np.zeros(nx)
            u0[int(nx/8):int(nx/8)*3+1] = 1
        elif isinstance(u0, np.ufunc) or callable(u0):
            x = np.linspace(0, Lx, nx)
            u0 = u0(2*pi*x/Lx)
        self.Lx = Lx
        self.nx = nx
        self.dx = dx
        self.tmax = tmax
        self.nt = nt
        self.dt = dt
        self.c = c
        self.u0 = u0.copy()
        self.u = u0.copy()
        self.t = 0

    def run(self):
        c = self.c
        dt = self.dt
        dx = self.dx
        u = self.u
        plt.figure()
        self.plot_snapshot()
        for i in range(self.nt):
            if c >= 0:
                u[1:] = u[1:] - c*dt/dx * (u[1:] - u[:-1])
                u[0] = u[-1]
            else:
                u[:-1] = u[:-1] - c*dt/dx * (u[1:] - u[:-1])
                u[-1] = u[0]
            self.u = u
            self.t += dt
            self.plot_snapshot()


        return self
    def plot_snapshot(self):
        plt.clf()
        t = self.t
        Lx = self.Lx
        nx = self.nx
        x = np.linspace(0, Lx, nx)
        u = self.u
        plt.plot(x, u)
        plt.xlabel('x (nx = {})'.format(self.nx))
        plt.ylabel('u')
        plt.xlim(0,Lx)
        ylim = abs(self.u0.max()*2)
        plt.ylim(-ylim, ylim)
        plt.grid('on')
        plt.text(0.02*Lx, ylim*0.98, 't = {:.2f}'.format(t), va='top')
        plt.pause(0.1)
