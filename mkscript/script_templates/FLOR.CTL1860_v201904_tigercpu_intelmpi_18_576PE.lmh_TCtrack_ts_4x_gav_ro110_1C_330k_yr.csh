#!/bin/csh  -f
#------------------------------------
#PBS -N lmh_TCtrack_ts_4x
#PBS -l size=1
#PBS -l walltime=24:00:00
#PBS -r y
#PBS -j oe
#PBS -o
#PBS -q batch

set echo

#module load gcp
#source /usr/local/Modules/3.1.6/init/csh
#module use -a /home/fms/local/modulefiles
source /usr/share/Modules/init/csh
module purge
module load intel/18.0/64/18.0.3.222
module load intel-mpi/intel/2018.3/64
module load hdf5/intel-16.0/intel-mpi/1.8.16
module load netcdf/intel-16.0/hdf5-1.8.16/intel-mpi/4.4.0

 set anho           = $1
 #set anho           = AANNHHOO

#set ensemble

# set echo                                
 set ye1            = $anho
 set ye2            = $anho
 set model          = FLOR
 set expname        = CTL1860_v201904_tigercpu_intelmpi_18_576PE
 set scriptname     = ${expname}.lmh_TCtrack_ts_4x_gav_ro110_1C_330k_yr.csh
 set thisdir        = $cwd
 set thisscript     = $thisdir/$scriptname
 set ppdir          = /tigress/wenchang/MODEL_OUT/${model}/${expname}/POSTP
 #set ppdir          = $HOME/scratch/${model}/work/${expname}/POSTP # use this ppdir in case model output still in the scratch disk
 set rootTCanalysis = /tigress/wenchang/analysis/TC

#
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Script: lmh_TCtrack_ts_4x.csh
# Author: Lucas Harris
# Source data: pp/atmos/ts/6hr/X_yr
# Output: Creates figures in $out_dir/atmos_${yr1}_${yr2}
#
# Sample frepp usage (http://www.gfdl.noaa.gov/fms/fre/#analysis):
# <component type="atmos">
# <timeSeries freq="6hr" source="atmos_4xdaily" chunkLength="$(PP_AMIP_CHUNK)">
#       <analysis switch="$(ANALYSIS_SWITCH)" startYear="$(ANA_AMIP_START)" endYear="$(ANA_AMIP_END)" cumulative="yes" script="[script name]" />
# </timeSeries>
#    <timeAverage ... >
#       <analysis script="script_name [options]"/>
#    </timeAverage>

#CAVEAT: Currently only have IBTrACS observations from 1990 onward,
    #so the last step (track_compare) may give weird answers for earlier dates.

# ============== VARIABLES SET BY FREPP =============
set in_data_dir  =  $ppdir
set descriptor   =  ${expname}
set out_dir      =  /tigress/wenchang/MODEL_OUT/${model}/${expname}/analysis_lmh/cyclones_gav_ro110_1C_330k
set WORKDIR      =  $HOME/scratch/TMP
 
 set year = $ye1
#
#
  set yo   = 10000
  @ yy   = $yo + $year
  set yoo  = `echo $yy | cut -c2-5`
  set lasttwo = `echo $yy | cut -c4-5`
  set cyear = $yoo
#
  echo $year
  echo $ye1
  echo $ye2
#
  @ yr1     = $year
  @ yr2     = $year
  @ iyear_beg = $ye1
  @ iyear_end = $ye2
#
# ============== END OF VARIABLES SET BY FREPP =============
 
 
#Currently just process all times in $in_data_dir
#format is pp/atmos/ts/6hr/10yr/atmos.2000010100-2009123123.h500.nc

set tmpdir=$WORKDIR/Harris.TC
mkdir -p $WORKDIR/Harris.TC
set tmpdir=`mktemp -d $WORKDIR/Harris.TC/$descriptor.XXXXXXXXXX`
cd /$tmpdir


set dnm = atmos_4xdaily
set f00 = ${cyear}0101.${dnm}
set f01 = ${ppdir}/${f00}

#gunzip ${ppdir}/${f00}.nc.gz

set cfile_list = `ls -1 ${f01}.nc`
if ( $#cfile_list == 0 ) then
    echo " BUMMER: no more files to process"
    exit
endif

#module load ifort netcdf/4.2 gcp
#module load netcdf hdf5
ncks -v slp ${f01}.nc  ${f00}.slp.nc
ncks -v vort850 ${f01}.nc  ${f00}.vort850.nc
ncks -v tm ${f01}.nc  ${f00}.tm.nc
ncks -v u_ref ${f01}.nc  ${f00}.u_ref.nc
ncks -v v_ref ${f01}.nc  ${f00}.v_ref.nc
# 
# WY: convert noleap or julian calendar to proleptic gregorian, obsolate since 2020-10-28, use wy_modify_time_encoding.py instead
#python $rootTCanalysis/convert_to_pg_calendar.py ${f00}.slp.nc
#python $rootTCanalysis/convert_to_pg_calendar.py ${f00}.vort850.nc
#python $rootTCanalysis/convert_to_pg_calendar.py ${f00}.tm.nc
#python $rootTCanalysis/convert_to_pg_calendar.py ${f00}.u_ref.nc
#python $rootTCanalysis/convert_to_pg_calendar.py ${f00}.v_ref.nc
#WY: modify time axis encoding of units
python $rootTCanalysis/wy_modify_time_encoding.py ${f00}.slp.nc
python $rootTCanalysis/wy_modify_time_encoding.py ${f00}.vort850.nc
python $rootTCanalysis/wy_modify_time_encoding.py ${f00}.tm.nc
python $rootTCanalysis/wy_modify_time_encoding.py ${f00}.u_ref.nc
python $rootTCanalysis/wy_modify_time_encoding.py ${f00}.v_ref.nc
#
set in_files=$tmpdir/${f00}.slp.nc
set proc_files=""
foreach file ( $in_files )
    set proc_file=`echo $file | sed 's/.slp.nc$/.#.nc/'`
    set proc_files="$proc_files $proc_file"
end
set files=`echo $proc_files | tr ' ' '\n'  |  sed 's/^\(.*\)$/"\1"/' | tr '\n' ',' | tr ' ' ','`

set inputname=input_lmh_TCtrack_ts_4x.nml
set outputname=lmh_TCtrack_ts_4x.dat
cat >! $inputname <<EOF
&nlist
    infile = $files
    outfile = 'lmh_TCtrack_ts_4x.dat',
    ncontours = 1,
    warm_core_check = .true.
    cint_slp = 2.
    one_variable_per_file = .true.
    r_offset_warm = 110.
    dt_crit_warm = 1.
    r_crit_warm = 330.
/
EOF

/tigress/gvecchi/ANALYSIS/LUCAS_TRACKER/CODE/bin/track_gav.exe  $inputname || exit

#Copy tracker output in case something goes wrong below
mkdir -p $out_dir/atmos_${yr1}_${yr2}/Harris.TC
cp *.nml *.dat  $out_dir/atmos_${yr1}_${yr2}/Harris.TC

# track sorter
#module load python
module load anaconda/2.1.0
#python /tigress/gvecchi/ANALYSIS/LUCAS_TRACKER/HIRO_py_scripts/convert_time_1583-.py $outputname
#cp ${outputname}* $out_dir/atmos_${yr1}_${yr2}/Harris.TC

#if ($lasttwo == "00") then
#  python /tigress/gvecchi/ANALYSIS/LUCAS_TRACKER/py_scripts/track_sorter_FLOR3.py  $outputname
#else
#  python /tigress/gvecchi/ANALYSIS/LUCAS_TRACKER/py_scripts/track_sorter_FLOR.py $outputname
#endif
#python /tigress/gvecchi/ANALYSIS/LUCAS_TRACKER/py_scripts/track_sorter_FLOR.py $outputname #WY
python $rootTCanalysis/track_sorter_FLOR_fix99.py $outputname #WY
#python /home/lmh/research/seasonal/quick_tracks/trunk/python/track_sorter.py $outputname
#set links=""
#foreach i ( $outputname.*.txt )
#    ln -s $i ${i:r:r}.txt
#end
#python /home/lmh/research/seasonal/quick_tracks/trunk/python/track_compare_an.py -s $yr1 -e $yr2 \
    #${outputname}.warm,${descriptor} |& tee compare_an.text
#\rm `find -type l`

#Move (input and) output to output directory

cp *.txt $out_dir/atmos_${yr1}_${yr2}/Harris.TC
#cp *.txt *.text *.png *.npz $out_dir/atmos_${yr1}_${yr2}/Harris.TC

#rm *.exe

tixe:
rm ${tmpdir}/*
rmdir ${tmpdir}
exit 0
