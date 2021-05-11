#!/usr/bin/env python3
'''
Geoffrey Weal, make_mass_submit_sl_script_for_LatticeFinder.py, 30/04/2021

This program is designed to make lots of collective submit scripts

'''

import os
from ase.io import read

def make_submitSL_packets_for_latticeFinder(mass_submit_counter,local_path,project,newlist,time,nodes,ntasks_per_node,mem_per_cpu,partition='large',email='',python_version='Python/3.6.3-gimkl-2017a',vasp_version='VASP/5.4.4-intel-2017a',vasp_execution='vasp_std'):
    # create name for job
    print("creating collective_LatticeFinder_submit_"+str(mass_submit_counter)+".sl for "+str(local_path))
    name = local_path.replace('/','_')
    # writing the mass_submit.sl script
    with open(local_path+'/'+"collective_LatticeFinder_submit_"+str(mass_submit_counter)+".sl", "w") as submitSL:
        submitSL.write('#!/bin/bash -e\n')
        submitSL.write('#SBATCH -J ' + str(name) + '\n')
        submitSL.write('#SBATCH -A ' + str(project) + '         # Project Account\n')
        submitSL.write('\n')
        submitSL.write('#SBATCH --time=' + str(time) + '     # Walltime\n')
        submitSL.write('#SBATCH --nodes=' + str(nodes) + '\n')
        submitSL.write('#SBATCH --ntasks-per-node=' + str(ntasks_per_node) + '\n')
        submitSL.write('#SBATCH --mem-per-cpu=' + str(mem_per_cpu) + '\n')
        #submitSL.write('#SBATCH -C sb\n')
        submitSL.write('\n')
        submitSL.write('#SBATCH --partition='+str(partition)+'\n')
        submitSL.write('#SBATCH --output=slurm-%j.out      # %x and %j are replaced by job name and ID'+'\n')
        submitSL.write('#SBATCH --error=slurm-%j.err'+'\n')
        if not email == '':
            submitSL.write('#SBATCH --mail-user=' + str(email) + '\n')
            submitSL.write('#SBATCH --mail-type=ALL\n')
        #submitSL.write('\n')
        submitSL.write('#SBATCH --hint nomultithread\n')
        submitSL.write('\n')
        submitSL.write('######################\n')
        submitSL.write('# Begin work section #\n')
        submitSL.write('######################\n')
        submitSL.write('\n')
        submitSL.write('module load '+str(python_version)+'\n')
        submitSL.write('module load '+str(vasp_version)+'\n')
        submitSL.write('\n')
        submitSL.write('my_array=('+' '.join(newlist)+')\n')
        submitSL.write('\n')
        submitSL.write('for directory in "${my_array[@]}"\n')
        submitSL.write('do\n')
        submitSL.write('    echo "======================================"\n')
        submitSL.write('    echo "$directory"\n')
        submitSL.write('    cd "$directory"\n')
        submitSL.write('    srun -K '+str(vasp_execution)+'\n')
        submitSL.write('    # removing files except for OUTCAR as we assume it finished successfully\n')
        submitSL.write('    Check_LatticeFinder_to_Tidy_after_Job.py\n')
        submitSL.write('    cd ..\n')
        submitSL.write('    echo "======================================"\n')
        submitSL.write('done\n')

def OUTCAR_finished(directory):
    if os.path.exists(directory+'/OUTCAR'):
        return True
    else:
        return False


    if not os.path.exists(directory+'/OUTCAR'):
        return False
    try:
        system = read(directory+'/OUTCAR')
        system.get_potential_energy()
        system.get_volume()
        return True
    except:
        return False

directories = []
for directory in sorted(os.listdir('.')):
    if not os.path.isdir(directory):
        continue
    if not OUTCAR_finished(directory):
        print(directory)
        directories.append(directory)
directories.sort()

local_path = '.'
project = 'uoo00084'
time = '0:40:00'
nodes = 1
ntasks_per_node = 2
mem_per_cpu = '3G'

partition='large'
email='geoffreywealslurmnotification@gmail.com'
python_version='Python/3.6.3-gimkl-2017a'
vasp_version='VASP/5.4.4-intel-2017a'
vasp_execution='vasp_std'




