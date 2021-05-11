#!/usr/bin/env python3
'''
Geoffrey Weal, LatticeFinder_Tidy_Finished_Jobs.py, 30/04/2021

This program is designed to remove the files of jobs that have finished. 

'''
import os
from ase.io import read

files_to_remove = ['CHG','CHGCAR','CONTCAR','DOSCAR','EIGENVAL','IBZKPT','INCAR','KPOINTS','OSZICAR','PCDAT','POSCAR','POTCAR','REPORT','submit.sl','vasprun.xml','WAVECAR','XDATCAR']

finished = True
try:
    system = read('OUTCAR')
    system.get_potential_energy()
    system.get_volume()
except:
    finished = False

files = [file for file in os.listdir('.') if os.path.isfile(file)]

if finished:
    for file_to_remove in files_to_remove:
        if file_to_remove in files:
            os.remove(file_to_remove)
    for file in files:
        if file.startswith('slurm-') and file.endswith('.out'):
            os.remove(file)
        elif file.startswith('slurm-') and file.endswith('.err'):
            os.remove(file)
