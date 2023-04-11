#!/usr/bin/env bash
# Wenchang Yang (wenchang@princeton.edu)
# Fri Aug  2 15:45:46 EDT 2019
# used for FLOR/AM2.5/HIRAM; for CM2.1/AM2.1, use wyplev2p1.sh
# example usage:
# ./wyplev.sh 01100101.atmos_month.nc vcomp vcomp.plev.nc
# ./wyplev.sh 01100101.atmos_month.nc vcomp vcomp.plev850.nc 85000
# ./wyplev.sh 01100101.atmos_month.nc vcomp vcomp.plev850200.nc "85000 20000"
# note: need to run 'python -m misc.get_pkbk model=xxx expname=xxx' to get the pkbk.nc file first before running this script
source /projects/GEOCLIM/wenchang/fre-nctools/site-configs/princeton/env.sh
export PATH=/projects/GEOCLIM/wenchang/fre-nctools/build/tigercpu_intelmpi_18/princeton/bin:$PATH
run_interp=/projects/GEOCLIM/wenchang/fre-nctools/postprocessing/plevel/plevel.sh

#input args
ifile=$1 #e.g., 01100101.atmos_month.nc
daname=$2 #e.g., temp #ucomp #$2 # e.g. temp 
ofile=$3 #e.g., ${daname}.plev.nc
if [ $# -eq 4 ]; then
    pp=$4 #plevels (units Pa), e.g. 20000 85000; if not specified, will use the default ncep defined plevels 
fi
tmpfile=wytmp.${daname}.input.nc

if [ -e $ofile ]; then
    echo "[exists]: ${ofile}"
    exit 0
fi

#cp /tigress/wenchang/MODEL_OUT/FLOR_pkak.nc ${data_name}.input.nc
#ncks -A -v $data_name,ps,time_bounds,average_T1,average_T2,average_DT $ifile ${data_name}.input.nc
#ncks -O -v $daname,pk,bk,ps,time_bounds,average_T1,average_T2,average_DT,lonb,latb $ifile $tmpfile
ncks -O -v $daname,ps,time_bounds,average_T1,average_T2,average_DT $ifile $tmpfile
#ncks -A /tigress/wenchang/MODEL_OUT/FLOR_pkak.nc $tmpfile
#ncks -A /tigress/wenchang/test/pkbk/FLOR.CTL1990_v201905_tigercpu_intelmpi_18_576PE.nc $tmpfile
#ncks -A /tigress/wenchang/MODEL_OUT/FLOR_pkbk.nc $tmpfile
if [ ! -e pkbk.nc ]; then
    echo "need to run 'python -m misc.get_pkbk model=xxx expname=xxx' to get the pkbk.nc file first before running this script"
    exit 0
fi
ncks -A pkbk.nc $tmpfile


#$run_interp -a -p "20000" -i ${data_name}.input.nc -o $ofile

if [ $# -eq 4 ]; then
    $run_interp -a -p "${pp}" -i ${tmpfile} -o $ofile
else
    $run_interp -a -i ${tmpfile} -o $ofile
fi

#rm tmpfile after success
if [ $? -eq 0 ]; then
    rm ${tmpfile}
fi
