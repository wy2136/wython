#!/usr/bin/env bash
# Wenchang Yang (wenchang@princeton.edu)
# Wed Apr  8 17:31:05 EDT 2020
set -v
set -e

this_dir=$(pwd)
input_dir=/home/wenchang/tgScratch/GEOCLIM/CM2.5_data/input/VOLCANIC/CMIP6

ln -sf ${input_dir}/extsw_V3_DATATROP_RCP.nc ${this_dir}/extsw_data.nc
ln -sf ${input_dir}/extlw_V3_DATATROP_RCP.nc ${this_dir}/extlw_data.nc
ln -sf ${input_dir}/omgsw_V4_DATATROP_RCP.nc ${this_dir}/omgsw_data.nc
ln -sf ${input_dir}/asmsw_V4_DATATROP_RCP.nc ${this_dir}/asmsw_data.nc

