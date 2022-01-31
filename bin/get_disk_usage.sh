#!/usr/bin/env bash
# Wenchang Yang (wenchang@princeton.edu)
# Fri Apr 10 00:52:51 EDT 2020
set -v
set -e
echo " " >> disk_usage
du -h -d1 $(pwd)/ |sort -k1h >> disk_usage
echo $(date) >> disk_usage
