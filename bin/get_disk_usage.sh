#!/usr/bin/env bash
# Wenchang Yang (wenchang@princeton.edu)
# Fri Apr 10 00:52:51 EDT 2020
set -v
set -e
ofile=wy_disk_usage.log
echo " " >> $ofile
du -h -d1 $(pwd)/ |sort -k1h >> $ofile
echo $(date) >> $ofile
