#!/usr/bin/env bash
# Wenchang Yang (wenchang@princeton.edu)
# Fri Nov 10 14:55:55 EST 2023
##SBATCH --nodes=1                # node count
##SBATCH --ntasks-per-node=1      # number of tasks per node
# 
#SBATCH --ntasks=1               # total number of tasks across all nodes = nodes x ntasks-per-node
#SBATCH --cpus-per-task=1        # cpu-cores per task (>1 if multi-threaded tasks)
#SBATCH --mem-per-cpu=16G         # memory per cpu-core (4G is default)
#SBATCH --time=24:00:00          # total run time limit (HH:MM:SS)
#SBATCH --mail-type=all          # send email when job begins/ends/fails
#SBATCH --mail-user=wenchang@princeton.edu
# 
##SBATCH --array=1-100#%32        # job array with index values 1, 2, ...,; max job # is 32 if specified
##SBATCH --output=slurm-%A.%a.out # stdout file
##SBATCH --error=slurm-%A.%a.err  # stderr file
set -e #v
##env settings
#export PATH=/tigress/wenchang/miniconda3/bin:$PATH
#export PYTHONPATH=/tigress/wenchang/wython
#export PYTHONUNBUFFERED=TRUE # see https://stackoverflow.com/questions/230751/how-to-flush-output-of-print-function
#export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK #for multi-threaded job
#ii_job=$SLURM_ARRAY_TASK_ID #for job array

#GEOCLIM
rootdir=/projects/GEOCLIM/wenchang/MODEL_OUT
echo "# Disk usage under $rootdir"
echo "* Wenchang Yang"
echo "* Department of Geosciences, Princeton University"
echo
echo $(date)
echo $rootdir
du -h -d1 $rootdir |sort -k1hr
echo
for dir in AM4_urban AM2.5C360 CM2.1p1 AM2.5 AM4; do
    echo $(date)
    echo $rootdir/$dir
    du -h -d1 $rootdir/$dir |sort -k1hr
    echo
done
echo "**done**"
echo $(whoami)
echo $(date)
