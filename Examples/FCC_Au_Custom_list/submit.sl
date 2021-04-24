#!/bin/bash -e
#SBATCH -J FCC_Au_Custom_list
#SBATCH -A uoo00084         # Project Account

#SBATCH --partition=large
#SBATCH --time=12:00:00     # Walltime
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem-per-cpu=2000MB

#SBATCH --output=slurmjob_%A.out
#SBATCH --error=slurmjob_%A.err
#SBATCH --mail-user=geoffreywealslurmnotifications@gmail.com
#SBATCH --mail-type=ALL

#SBATCH --hint=nomultithread

######################
# Begin work section #
######################

module load Python/3.6.3-gimkl-2017a
python -u Run_LatticeFinder.py