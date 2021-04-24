import os

from LatticeFinder.LatticeFinder.examining_lattice_constant_methods_with_Manual_Mode import save_cluster_to_folder
from LatticeFinder.LatticeFinder.Create_submitSL_slurm_Main import make_submitSL

def get_energies_across_lattice_constants_VASP(lattice_type,symbol,lattice_constant_generator,size,directions=None,miller=None,vasp_inputs='VASP_Files',folder_name='VASP_Clusters'):
	"""

	"""

	if not os.path.exists(folder_name):
		os.makedirs(folder_name)
	for latticeconstants in lattice_constant_generator:
		name = '_'.join([str(key)+'_'+str(value) for latticeconstant in latticeconstants])
		bulk_system = lattice_type(symbol=symbol, latticeconstant=latticeconstants, size=size) #, directions=directions, miller=miller)
		save_cluster_to_folder(folder_name,name,'','vasp',bulk_system)
	copy_VASP_files(folder_name,name,vasp_inputs,slurm_information)


def copy_VASP_files(folder,vasp_files_folder,slurm_information):
	if not os.path.exists(vasp_files_folder):
		print('Error in copying VASP files to cluster folder')
		print('There is no folder called "VASP_Files" in your working directory.')
		print('This folder is where you should place your VASP files in for DFT local optimisations.')
		print('Make this folder and place your "POTCAR", INCAR", "KPOINTS" files for VASP local optimisations')
		print('This program will exit without completing.')
		exit()
	VASP_Files_files = os.listdir(vasp_files_folder)
	have_POTCAR  = 'POTCAR'  in VASP_Files_files
	have_INCAR   = 'INCAR'   in VASP_Files_files
	have_KPOINTS = 'KPOINTS' in VASP_Files_files
	if not (have_POTCAR and have_INCAR and have_KPOINTS):
		print('Error in copying VASP files to cluster folder')
		print('You need the following files when you are performing VASP calculations:')
		print()
		print('\tPOTCAR:\t' +('You have this' if have_POTCAR  else 'You do not have this'))
		print('\tINCAR:\t'  +('You have this' if have_INCAR   else 'You do not have this'))
		print('\tKPOINTS:\t'+('You have this' if have_KPOINTS else 'You do not have this'))
		print()
		print('Check this out. This program will now end without completing.')
		exit()
	for root, dirs, files in os.walk(folder):
		dirs.sort()
		if not ('POSCAR' in files):
			continue
		print('Copying VASP files to '+root)
		for file in ['POTCAR', 'INCAR', 'KPOINTS']:
			copyfile(vasp_files_folder+'/'+file, root+'/'+file)
		project = slurm_information['project']
		time = slurm_information['time']
		nodes = slurm_information['nodes']
		ntasks_per_node = slurm_information['ntasks_per_node']
		mem_per_cpu = slurm_information['mem-per-cpu']
		partition = slurm_information['partition']
		email = slurm_information['email']
		vasp_version = slurm_information['vasp_version']
		vasp_execution = slurm_information['vasp_execution']
		make_submitSL(root,project,time,nodes,ntasks_per_node,mem_per_cpu,partition=partition,email=email,vasp_version=vasp_version,vasp_execution=vasp_execution)
