#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Wed Feb  5 11:37:37 EST 2020
import os, os.path, sys, datetime
#import xarray as xr, numpy as np, pandas as pd
#import matplotlib.pyplot as plt
import argparse
print()

# args setting
parser = argparse.ArgumentParser()
parser.add_argument('--model', help='model name')
parser.add_argument('--expname', help='experiment name')
parser.add_argument('--ens', help='ensemble members, e.g. 1:5')
parser.add_argument('--years', help='model years, e.g. 1:10 or 1981:2000')
args = parser.parse_args()
model = args.model if args.model else 'FLOR'
expname = args.expname
ens = args.ens
if ens:
    en_start, en_end = [int(s) for s in ens.split(':')]
else:
    en_start, en_end = 1, 5
years = args.years
if years:
    year_start, year_end = [int(s) for s in years.split(':')]
else:
    year_start, year_end = 1, 10 

cwd = os.getcwd()

# template script
model_template = 'FLOR'
expname_template = 'CTL1860_v201904_tigercpu_intelmpi_18_576PE'
ifile = os.path.join(os.path.dirname(os.path.abspath(__file__)),
    'script_templates', 
    f'{model_template}.{expname_template}.lmh_TCtrack_ts_4x_gav_ro110_1C_330k_yr.csh')

def do_replace(content, istr, ostr):
    '''replace istr with ostr in content'''
    print('[replacing]:', istr, '->', ostr)
    return content.replace(istr, ostr)

# target script path
obasename = os.path.basename(ifile)
# modify the script name accordingly
if model != model_template:
    obasename = obasename.replace(model_template, model)
if model in ('AM2.5C360',):
    obasename = obasename.replace('_1C_', '_') # use the default value of dt_crit_warm = 2.
elif model in ('HIRAM',):
    obasename = obasename.replace('_1C_', '_2p5C_') # dt_crit_warm = 2.5degC
elif model in ('AM4', 'AM4_urban'):
    obasename = obasename.replace('_ro110_', '_ro250_') # r_offset_warm = 250.
    obasename = obasename.replace('_1C_', '_p75C_') # dt_crit_warm = 0.75degC
    obasename = obasename.replace('_330k_', '_550k_') # r_crit_warm = 550.
else:
    pass

if expname:
    obasename = obasename.replace(expname_template, expname)
ofile = os.path.join(cwd, obasename)
if os.path.exists(ofile):
    print('[exists]:', obasename)
    sys.exit()

# tracker script
with open(ifile) as fi:
    icontent = fi.read()
    print('[ifile]:', ifile)
    with open(ofile, 'w') as fo:
        ocontent = icontent
        # modify the script content accordingly
        if model != model_template:
            istr, ostr = '= FLOR', f'= {model}'
            ocontent = do_replace(ocontent, istr, ostr)
        if model in ('FLOR',):
            istr, ostr = '${model}/', ''
            ocontent = do_replace(ocontent, istr, ostr) # FLOR outputs are directly under MODEL_OUT
        elif model in ('AM2.5C360',):
            istr, ostr = 'dt_crit_warm = 1.', 'dt_crit_warm = 2.! default is 2.'
            ocontent = do_replace(ocontent, istr, ostr)
            istr, ostr = '_1C_', '_'
            ocontent = do_replace(ocontent, istr, ostr)
        elif model in ('HIRAM',):
            istr, ostr = 'dt_crit_warm = 1.', 'dt_crit_warm = 2.5! default is 2.'
            ocontent = do_replace(ocontent, istr, ostr)
            istr, ostr = '_1C_', '_2p5C_'
            ocontent = do_replace(ocontent, istr, ostr)
        elif model in ('AM4', 'AM4_urban'):
            istr, ostr = 'r_offset_warm = 110.', 'r_offset_warm = 250.! default is 110.'
            ocontent = do_replace(ocontent, istr, ostr)
            istr, ostr = '_ro110_', '_ro250_'
            ocontent = do_replace(ocontent, istr, ostr)
            
            istr, ostr = 'dt_crit_warm = 1.', 'dt_crit_warm = 0.75! default is 2.'
            ocontent = do_replace(ocontent, istr, ostr)
            istr, ostr = '_1C_', '_p75C_'
            ocontent = do_replace(ocontent, istr, ostr)
            
            istr, ostr = 'r_crit_warm = 330.', 'r_crit_warm = 550.! default is 330.'
            ocontent = do_replace(ocontent, istr, ostr)
            istr, ostr = '_330k', '_550k'
            ocontent = do_replace(ocontent, istr, ostr)
            
            #sorter script
            #istr, ostr = 'python $rootTCanalysis/track_sorter_FLOR_fix99.py $outputname #WY', 'python $rootTCanalysis/track_sorter_AM4C96.py $outputname #WY/GV'
            istr, ostr = 'python $rootTCanalysis/track_sorter_FLOR_fix99.py $outputname #WY', 'python $rootTCanalysis/track_sorter_fix99_AM4C96.py $outputname #WY/GV/WY'
            ocontent = do_replace(ocontent, istr, ostr)
        if expname:
            istr, ostr = f'= {expname_template}', f'= {expname}'
            ocontent = do_replace(ocontent, istr, ostr)
        if ens:
            istr = '#set ensemble'
            ostr = '''#set ensemble
set en           = $2
set eno   = 100
@ enoo   = $eno + $en
set en  = `echo $enoo | cut -c2-3`'''
            ocontent = do_replace(ocontent, istr, ostr)
            istr, ostr = '${expname}/', '${expname}/en${en}/'
            ocontent = do_replace(ocontent, istr, ostr)
        fo.write(ocontent)
        print('[created]:', obasename)

# loop script
loop_basename = f'loop.{obasename}'.replace('.csh', '.sh')
loop_file = os.path.join(cwd, loop_basename)
t = datetime.datetime.now()
with open(loop_file, 'w') as fo:
    if ens:
        s = f'''#!/usr/bin/env bash
# Wenchang Yang (wenchang@princeton.edu)
# {t.year:04d}-{t.month:02d}-{t.day:02d}T{t.hour:02d}:{t.minute:02d}:{t.second:02d}@Princeton
set -ev

script=./{obasename}
for en in {{{en_start}..{en_end}}}; do
for year in {{{year_start}..{year_end}}}; do
$script  $year $en
done
done'''
    else:
        s = f'''#!/usr/bin/env bash
# Wenchang Yang (wenchang@princeton.edu)
# {t.year:04d}-{t.month:02d}-{t.day:02d}T{t.hour:02d}:{t.minute:02d}:{t.second:02d}@Princeton
set -ev

script=./{obasename}
for year in {{{year_start}..{year_end}}}; do
$script  $year
done'''
    fo.write(s)
    print('[created]:', loop_basename)

# slurm script
if model in ('AM2.5C360',):#AM2.5C360 needs more memory (about 11.26 GB) than the default 4G
    mem_per_cpu = 16#G
else:
    mem_per_cpu = 4#G
slurm_basename = f'slurm.{obasename}'.replace('.csh', '.sh')
slurm_file = os.path.join(cwd, slurm_basename)
t = datetime.datetime.now()
with open(slurm_file, 'w') as fo:
    if ens:
        nyears = year_end - year_start + 1
        nens = en_end - en_start + 1
        s = f'''#!/usr/bin/env bash
# Wenchang Yang (wenchang@princeton.edu)
# {t.year:04d}-{t.month:02d}-{t.day:02d}T{t.hour:02d}:{t.minute:02d}:{t.second:02d}@Princeton
##SBATCH --job-name=array-job     # create a short name for your job
#SBATCH --output=slurm-%A_%a.out # STDOUT file
##SBATCH --error=slurm-%A_%a.err  # STDERR file
#SBATCH --nodes=1                # node count
#SBATCH --ntasks=1               # total number of tasks across all nodes
#SBATCH --cpus-per-task=1        # cpu-cores per task (>1 if multi-threaded tasks)
#SBATCH --mem-per-cpu={mem_per_cpu}G         # memory per cpu-core (4G is default)
#SBATCH --time=01:01:00          # total run time limit (HH:MM:SS)
#SBATCH --array=1-{nyears*nens}#%32              # job array with index values 1, 2, ..., {nyears*nens}; max job # is 32
#SBATCH --mail-type=all          # send email on job start, end and fault
#SBATCH --mail-user=wenchang@princeton.edu
set -ev
ii=$SLURM_ARRAY_TASK_ID
en_start={en_start}
year_start={year_start}
year=$(( year_start + (ii-1)%{nyears} ))
en=$(( en_start + (ii-1)/{nyears} ))
script={obasename}

$(pwd)/$script  $year $en
'''
    else:
        s = f'''#!/usr/bin/env bash
# Wenchang Yang (wenchang@princeton.edu)
# {t.year:04d}-{t.month:02d}-{t.day:02d}T{t.hour:02d}:{t.minute:02d}:{t.second:02d}@Princeton
##SBATCH --job-name=array-job     # create a short name for your job
#SBATCH --output=slurm-%A_%a.out # STDOUT file
##SBATCH --error=slurm-%A_%a.err  # STDERR file
#SBATCH --nodes=1                # node count
#SBATCH --ntasks=1               # total number of tasks across all nodes
#SBATCH --cpus-per-task=1        # cpu-cores per task (>1 if multi-threaded tasks)
#SBATCH --mem-per-cpu={mem_per_cpu}G         # memory per cpu-core (4G is default)
#SBATCH --time=01:01:00          # total run time limit (HH:MM:SS)
#SBATCH --array={year_start}-{year_end}#%32              # job array with index values {year_start}, {year_start+1}, ..., {year_end}, max # of jobs is 32
#SBATCH --mail-type=all          # send email on job start, end and fault
#SBATCH --mail-user=wenchang@princeton.edu
set -ev
year=$SLURM_ARRAY_TASK_ID
script={obasename}

$(pwd)/$script  $year
'''
    fo.write(s)
    print('[created]:', slurm_basename)

# change the file permissions to 755
os.chmod(ofile, 0o755)
os.chmod(loop_file, 0o755)
os.chmod(slurm_file, 0o755)
print()
