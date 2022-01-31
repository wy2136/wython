#!/usr/bin/env bash
# Wenchang Yang (wenchang@princeton.edu)
# Wed Dec 18 16:25:15 EST 2019

watch -n 30 -d 'squeue -p cpu -o "%.10i %6P %.40j %.10g %8u %.2t %19S %.10M %10l %.5D %R" --sort=S --states=PENDING | egrep -v "N/A" |head -20'
