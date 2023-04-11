#!/usr/bin/env bash
# Wenchang Yang (wenchang@princeton.edu)
# Fri Aug  2 15:45:46 EDT 2019
# example usage:
#ifile=/projects/GEOCLIM/wenchang/MODEL_OUT/AM2.1p1/CTL2010GF_tigercpu_intelmpi_18_30PE/POSTP/01300101.atmos_daily.nc
#daname=ucomp
#ofile=01300101.atmos_daily.$daname.plev.nc
#pp='25000 85000'
#./wyplev2p1.sh $ifile $daname $ofile "$pp"
#
#ifile=/projects/GEOCLIM/wenchang/MODEL_OUT/AM2.1p1/CTL2010GF_tigercpu_intelmpi_18_30PE/POSTP/01300101.atmos_month.nc
#daname=temp
#ofile=01300101.atmos_month.$daname.plev.nc
#./wyplev2p1.sh $ifile $daname $ofile
#
#ifile=/projects/GEOCLIM/wenchang/MODEL_OUT/AM2.1p1/CTL2010GF_tigercpu_intelmpi_18_30PE/POSTP/01300101.atmos_month.nc
#daname=sphum
#ofile=01300101.atmos_month.$daname.plev.nc
#./wyplev2p1.sh $ifile $daname $ofile

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
ncks -O -v $daname,pk,bk,ps,time_bounds,average_T1,average_T2,average_DT,lonb,latb $ifile $tmpfile
#ncks -A /tigress/wenchang/MODEL_OUT/FLOR_pkak.nc $tmpfile

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
