#!/usr/bin/env bash
# Wenchang Yang (wenchang@princeton.edu)
# Wed Apr  8 17:31:05 EDT 2020
set -v
set -e

this_dir=$(pwd)
input_files=/home/wenchang/tgScratch/GEOCLIM/wenchang/CM2.5/input/input_for_FLOR/*
grid_files=/home/wenchang/tgScratch/GEOCLIM/wenchang/CM2.5/mosaics/*.nc

# input files
for f in $input_files; do
    ln -sf $f $this_dir/
done

# grid files
for f in $grid_files; do
    ln -sf $f $this_dir/
done
