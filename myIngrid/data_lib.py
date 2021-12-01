# -*- coding: utf-8 -*-
"""
@author: yang
"""
from . import data_lib_iri
from .data_lib_iri import *

# ######## data paths on the Columbia data library.

#  climate index
mjo_phase = 'http://strega.ldeo.columbia.edu:81/OTHER/.wyang/.strega/.home/.climate_index/.MJO_index.nc/.phase'
mjo_amplitude = 'http://strega.ldeo.columbia.edu:81/OTHER/.wyang/.strega/.home/.climate_index/.MJO_index.nc/.amplitude'

# time series
itcz_states_daily = 'http://strega.ldeo.columbia.edu:81/OTHER/.wyang/.strega/.home/.ITCZ_states/.itcz_daily.nc/.n'
itcz_states = itcz_states_daily
itcz_states_3hourly = 'http://strega.ldeo.columbia.edu:81http://strega.ldeo.columbia.edu:81/OTHER/.wyang/.strega/.home/.ITCZ_states/.itcz_3hourly.nc/.n'

# surface
# monthly
qu_int_erai = 'http://strega.ldeo.columbia.edu:81/OTHER/.wyang/.strega/.home/.ERAInterim/.Surface/.qu.int.nc/.int_qu'
qv_int_erai = 'http://strega.ldeo.columbia.edu:81/OTHER/.wyang/.strega/.home/.ERAInterim/.Surface/.qv.int.nc/.int_qv'
sic_erai = 'http://strega.ldeo.columbia.edu:81/OTHER/.wyang/.strega/.home/.ERAInterim/.Surface/.sic.nc/.ci'
# daily
hfls_daily_erai = 'http://strega.ldeo.columbia.edu:81/OTHER/.wyang/.strega/.home/.ERAInterim/.daily/.hfls.nc/.slhf'
hfls_daily_anom_erai = 'http://strega.ldeo.columbia.edu:81/OTHER/.wyang/.strega/.home/.ERAInterim/.daily/.hfls.ydayanom.nc/.slhf'
hfss_daily_erai = 'http://strega.ldeo.columbia.edu:81/OTHER/.wyang/.strega/.home/.ERAInterim/.daily/.hfss.nc/.sshf'
hfss_daily_anom_erai = 'http://strega.ldeo.columbia.edu:81/OTHER/.wyang/.strega/.home/.ERAInterim/.daily/.hfss.ydayanom.nc/.sshf'
pr_daily_erai = 'http://strega.ldeo.columbia.edu:81/OTHER/.wyang/.strega/.home/.ERAInterim/.daily/.prcp.daily.nc/.prcp'
pr_daily_anom_erai = 'http://strega.ldeo.columbia.edu:81/OTHER/.wyang/.strega/.home/.ERAInterim/.daily/.prcp.daily.ydayanom.nc/.prcp'
rlns_daily_erai = 'http://strega.ldeo.columbia.edu:81/OTHER/.wyang/.strega/.home/.ERAInterim/.daily/.rlns.nc/.str'
rlns_daily_anom_erai = 'http://strega.ldeo.columbia.edu:81/OTHER/.wyang/.strega/.home/.ERAInterim/.daily/.rlns.ydayanom.nc/.str'
rsns_daily_erai = 'http://strega.ldeo.columbia.edu:81/OTHER/.wyang/.strega/.home/.ERAInterim/.daily/.rsns.nc/.ssr'
rsns_daily_anom_erai = 'http://strega.ldeo.columbia.edu:81/OTHER/.wyang/.strega/.home/.ERAInterim/.daily/.rsns.ydayanom.nc/.ssr'
u10_daily_erai = 'http://strega.ldeo.columbia.edu:81/OTHER/.wyang/.strega/.home/.ERAInterim/.daily/.u10.daily.nc/.U10'
u10_daily_anom_erai = 'http://strega.ldeo.columbia.edu:81/OTHER/.wyang/.strega/.home/.ERAInterim/.daily/.u10.daily.ydayanom.nc/.U10'
v10_daily_erai = 'http://strega.ldeo.columbia.edu:81/OTHER/.wyang/.strega/.home/.ERAInterim/.daily/.v10.daily.nc/.V10'
v10_daily_anom_erai = 'http://strega.ldeo.columbia.edu:81/OTHER/.wyang/.strega/.home/.ERAInterim/.daily/.v10.daily.ydayanom.nc/.V10'
wind10_daily_erai = 'http://strega.ldeo.columbia.edu:81/OTHER/.wyang/.strega/.home/.ERAInterim/.daily/.wind10.daily.nc/.WIND10'
wind10_daily_anom_erai = 'http://strega.ldeo.columbia.edu:81/OTHER/.wyang/.strega/.home/.ERAInterim/.daily/.wind10.daily.ydayanom.nc/.WIND10'

# OLR
olr_daily = 'http://strega.ldeo.columbia.edu:81/OTHER/.wyang/.strega/.home/.olr/.olr.day.mean.nc/.olr'
olr_daily_anom = 'http://strega.ldeo.columbia.edu:81/OTHER/.wyang/.strega/.home/.olr/.olr.day.anom.nc/.olr'

# SST
oisst2 = 'http://strega.ldeo.columbia.edu:81/OTHER/.wyang/.strega/.home/.sst/.oisst.nc/.sst'
oisst2_anom = 'http://strega.ldeo.columbia.edu:81/OTHER/.wyang/.strega/.home/.sst/.oisst.ydayanom.nc/.sst'
oisst2_monanom = 'http://strega.ldeo.columbia.edu:81/OTHER/.wyang/.strega/.home/.sst/.oisst.monanom.nc/.sst'


# pressure levels
div_daily_200mb_erai = 'http://strega.ldeo.columbia.edu:81/OTHER/.wyang/.strega/.home/.ERAInterim/.daily/.div.daily.200mb.nc/.D'
div_daily_anom_200mb_erai = 'http://strega.ldeo.columbia.edu:81/OTHER/.wyang/.strega/.home/.ERAInterim/.daily/.div.daily.ydayanom.200mb.nc/.D'
phi_daily_200mb_erai = 'http://strega.ldeo.columbia.edu:81/OTHER/.wyang/.strega/.home/.ERAInterim/.daily/.phi.daily.200mb.nc/.VP'
phi_daily_anom_200mb_erai = 'http://strega.ldeo.columbia.edu:81/OTHER/.wyang/.strega/.home/.ERAInterim/.daily/.phi.daily.ydayanom.200mb.nc/.VP'
phi_daily_850mb_erai = 'http://strega.ldeo.columbia.edu:81/OTHER/.wyang/.strega/.home/.ERAInterim/.daily/.phi.daily.850mb.nc/.VP'
phi_daily_anom_850mb_erai = 'http://strega.ldeo.columbia.edu:81/OTHER/.wyang/.strega/.home/.ERAInterim/.daily/.phi.daily.ydayanom.850mb.nc/.VP'
psi_daily_200mb_erai = 'http://strega.ldeo.columbia.edu:81/OTHER/.wyang/.strega/.home/.ERAInterim/.daily/.psi.daily.200mb.nc/.SF'
psi_daily_anom_200mb_erai = 'http://strega.ldeo.columbia.edu:81/OTHER/.wyang/.strega/.home/.ERAInterim/.daily/.psi.daily.ydayanom.200mb.nc/.SF'
psi_daily_850mb_erai = 'http://strega.ldeo.columbia.edu:81/OTHER/.wyang/.strega/.home/.ERAInterim/.daily/.psi.daily.850mb.nc/.SF'
psi_daily_anom_850mb_erai = 'http://strega.ldeo.columbia.edu:81/OTHER/.wyang/.strega/.home/.ERAInterim/.daily/.psi.daily.ydayanom.850mb.nc/.SF'
q_daily_850mb_erai = 'http://strega.ldeo.columbia.edu:81/OTHER/.wyang/.strega/.home/.ERAInterim/.daily/.q.daily.850mb.nc/.q'
q_daily_anom_850mb_erai = 'http://strega.ldeo.columbia.edu:81/OTHER/.wyang/.strega/.home/.ERAInterim/.daily/.q.daily.ydayanom.850mb.nc/.q'
qu_daily_850mb_erai = 'http://strega.ldeo.columbia.edu:81/OTHER/.wyang/.strega/.home/.ERAInterim/.daily/.qu.daily.850mb.nc/.qu'
qu_daily_anom_850mb_erai = 'http://strega.ldeo.columbia.edu:81/OTHER/.wyang/.strega/.home/.ERAInterim/.daily/.qu.daily.ydayanom.850mb.nc/.qu'
qv_daily_850mb_erai = 'http://strega.ldeo.columbia.edu:81/OTHER/.wyang/.strega/.home/.ERAInterim/.daily/.qv.daily.850mb.nc/.qv'
qv_daily_anom_850mb_erai = 'http://strega.ldeo.columbia.edu:81/OTHER/.wyang/.strega/.home/.ERAInterim/.daily/.qv.daily.ydayanom.850mb.nc/.qv'
u_daily_200mb_erai = 'http://strega.ldeo.columbia.edu:81/OTHER/.wyang/.strega/.home/.ERAInterim/.daily/.u.daily.200mb.nc/.U'
u_daily_anom_200mb_erai = 'http://strega.ldeo.columbia.edu:81/OTHER/.wyang/.strega/.home/.ERAInterim/.daily/.u.daily.ydayanom.200mb.nc/.U'
u_daily_850mb_erai = 'http://strega.ldeo.columbia.edu:81/OTHER/.wyang/.strega/.home/.ERAInterim/.daily/.u.daily.850mb.nc/.U'
u_daily_anom_850mb_erai = 'http://strega.ldeo.columbia.edu:81/OTHER/.wyang/.strega/.home/.ERAInterim/.daily/.u.daily.ydayanom.850mb.nc/.U'
v_daily_200mb_erai = 'http://strega.ldeo.columbia.edu:81/OTHER/.wyang/.strega/.home/.ERAInterim/.daily/.v.daily.200mb.nc/.V'
v_daily_anom_200mb_erai = 'http://strega.ldeo.columbia.edu:81/OTHER/.wyang/.strega/.home/.ERAInterim/.daily/.v.daily.ydayanom.200mb.nc/.V'
v_daily_850mb_erai = 'http://strega.ldeo.columbia.edu:81/OTHER/.wyang/.strega/.home/.ERAInterim/.daily/.v.daily.850mb.nc/.V'
v_daily_anom_850mb_erai = 'http://strega.ldeo.columbia.edu:81/OTHER/.wyang/.strega/.home/.ERAInterim/.daily/.v.daily.ydayanom.850mb.nc/.V'
zeta_daily_850mb_erai = 'http://strega.ldeo.columbia.edu:81/OTHER/.wyang/.strega/.home/.ERAInterim/.daily/.zeta.850mb.nc/.zeta'
zeta_daily_anom_850mb_erai = 'http://strega.ldeo.columbia.edu:81/OTHER/.wyang/.strega/.home/.ERAInterim/.daily/.zeta.ydayanom.850mb.nc/.zeta'
