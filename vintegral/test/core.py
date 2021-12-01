import matplotlib.pyplot as plt
import xarray as xr
from vintegral import vi4d



datadir = '/home/wenchay/mydata/erai/daily'
ncfile_q = datadir + '/q/q.daily.2014.*.nc'
ncfile_ps = datadir + '/ps/ps.daily.2014.nc'
ncfile_qint = datadir + '/q.int/q.int.daily.2014.nc'

q = xr.open_mfdataset(ncfile_q)['q']
plevels = q['level'].values*100
ps = xr.open_dataset(ncfile_ps)['sp']
qint = xr.open_dataset(ncfile_qint)['int_q']
viq = qint.copy()
viq.values = vi4d(q.values, plevels, ps.values)/9.8
#
# plt.close('all')
# plt.figure()
# qint.isel(time=0).geo.plot()
# plt.figure()
# viq.isel(time=0).geo.plot()
# plt.figure()
# (viq-qint).isel(time=0).geo.plot()
#
# plt.figure()
# qint.mean('time').geo.plot()
# plt.figure()
# viq.mean('time').geo.plot()
# plt.figure()
# (viq-qint).mean('time').geo.plot()
