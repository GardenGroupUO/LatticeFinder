import os
from ase.io import read
from shutil import copyfile
from LatticeFinder.LatticeFinder.examining_lattice_constant_methods_with_Manual_Mode import save_cluster_to_folder
from LatticeFinder.LatticeFinder.Create_submitSL_slurm_Main import make_submitSL, make_submitSL_packets_for_latticeFinder
from LatticeFinder.LatticeFinder.examining_lattice_constant_methods_with_ASE import save_datum_to_file, get_volume_per_atom

def get_system_from_VASP(latticeconstants,folder_name):
	"""

	"""
	systems = []
	for a_latticeconstants in latticeconstants:
		name = get_folder_name(a_latticeconstants)
		system = read(folder_name+'/'+name+'/OUTCAR')
		systems.append(system)
	return systems

def get_folder_name(latticeconstants):
	"""

	"""
	if isinstance(latticeconstants,dict):
		name = '_'.join([str(key)+'_'+str(value) for key, value in latticeconstants.items()])
	elif isinstance(latticeconstants,tuple) or isinstance(latticeconstants,list):
		raise Exception('Error: latticeconstants can not be a tuple or list.')
	else:
		name = 'c_'+str(latticeconstants)
	return name

def get_energies_across_lattice_constants_VASP(lattice_type,symbol,lattice_constant_generator,size,directions=None,miller=None,lattice_data_file=None,vasp_inputs='VASP_Files',folder_name='VASP_Clusters',slurm_information={},force_rewrite=False,lattice_type_name=None,make_packets='packet',energies_vs_lattice_constants={}):
	"""

	"""
	lattice_constants_with_obtained_energies = energies_vs_lattice_constants.keys()
	if force_rewrite:
		print('=============================================================================')
		print('PERFORMING FORCE REWRITE OF VASP FILES')
		print()
		print('NOT GETTING DATA, instead making clusters for running in VASP.')
		print('=============================================================================')
		make_VASP_folders(lattice_type,symbol,lattice_constants_with_obtained_energies,size,directions,miller,vasp_inputs,folder_name,slurm_information,make_packets)
		print('=============================================================================')
		print('All VASP files have been rewritten. You will need to turn the "force_rewrite" option to False now that this has been done, otherwise this program will only continue to rewrite your VASP files.')
		print('This program will not finish without completing.')
		print('=============================================================================')
		exit()
	else:
		lattice_constant_generator.reset()
		all_lattice_constants_to_make = list(lattice_constant_generator)
		if isinstance(all_lattice_constants_to_make[0],dict):
			for index in range(len(all_lattice_constants_to_make)):
				a_lattice_constant_to_make = all_lattice_constants_to_make[index]
				a_lattice_constant_to_make = sorted(a_lattice_constant_to_make.items(),key= lambda x:x[0])
				a_lattice_constant_to_make = tuple(value for key, value in a_lattice_constant_to_make)
				all_lattice_constants_to_make[index] = a_lattice_constant_to_make
			lattice_constant_generator.reset()
			lattice_constants_to_get_data_on = [item for item in all_lattice_constants_to_make if item not in lattice_constants_with_obtained_energies]
			#if not isinstance(all_lattice_constants_to_make[0],dict):
			#	for index in range(len(all_lattice_constants_to_make)):
			#		all_lattice_constants_to_make[index] = [all_lattice_constants_to_make[index]]
			lattice_constants_to_get_data_on = [{key: value for key, value in zip(lattice_constant_generator.lattice_constant_types,item)} for item in all_lattice_constants_to_make]
			#lattice_constants_to_get_data_on = [{key: value for key, value in zip(lattice_constant_generator.lattice_constant_types,item)} for item in all_lattice_constants_to_make]
			lc_data_files_to_make = compare_lc_with_ls_files_on_disk(lattice_constants_to_get_data_on,folder_name)
		else:
			lc_data_files_to_make = compare_lc_with_ls_files_on_disk(all_lattice_constants_to_make,folder_name)
		if len(lc_data_files_to_make) > 0:
			print('NOT GETTING DATA, instead making clusters for running in VASP.')
			make_VASP_folders(lattice_type,symbol,lc_data_files_to_make,size,directions,miller,vasp_inputs,folder_name,slurm_information,make_packets)
			exit()
	slurm_information = get_VASP_energies(lattice_constant_generator,lattice_data_file,folder_name,lattice_type_name,energies_vs_lattice_constants=energies_vs_lattice_constants)
	return slurm_information

def compare_lc_with_ls_files_on_disk(lattice_constants_to_get_data_on,folder_name):
	"""

	"""
	if not os.path.exists(folder_name):
		return lattice_constants_to_get_data_on
	lc_data_files_to_make = []
	for latticeconstants in lattice_constants_to_get_data_on:
		name = get_folder_name(latticeconstants)
		if not os.path.isdir(folder_name+'/'+name):
			lc_data_files_to_make.append(latticeconstants)
	return lc_data_files_to_make

def make_VASP_folders(lattice_type,symbol,lc_data_files_to_make,size,directions=None,miller=None,vasp_inputs='VASP_Files',folder_name='VASP_Clusters',slurm_information={},make_packets='packets'):
	"""

	"""
	if not os.path.exists(folder_name):
		os.makedirs(folder_name)
	check_VASP_files(vasp_inputs)
	if make_packets == 'packets':
		all_directories = []
	for latticeconstants in lc_data_files_to_make:
		name = get_folder_name(latticeconstants)
		bulk_system = lattice_type(symbol=symbol, latticeconstant=latticeconstants, size=size) #, directions=directions, miller=miller)
		bulk_system.set_pbc(True)
		save_cluster_to_folder(folder_name,name,'','vasp',bulk_system)
		copy_VASP_files(folder_name+'/'+name,vasp_inputs,slurm_information,make_packets)
		if make_packets == 'packets':
			all_directories.append(name)
	if make_packets == 'packets':
		make_packet_submitSL_files(folder_name,all_directories,slurm_information)
	else:
		make_individual_submitSL_files(folder_name,slurm_information)

def check_VASP_files(vasp_files_folder):
	"""

	"""
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

def copy_VASP_files(root,vasp_files_folder,slurm_information,make_packets):
	"""

	"""
	check_INCAR_Further(vasp_files_folder)
	print('Copying VASP files to '+root)
	for file in ['POTCAR', 'INCAR', 'KPOINTS']:
		copyfile(vasp_files_folder+'/'+file, root+'/'+file)


def check_INCAR_Further(vasp_files_folder):
	"""

	"""
	with open(vasp_files_folder+'/INCAR') as INCAR:
		for line in INCAR:
			if 'NSW' in line:
				line = line.rstrip().lstrip()
				number = line.replace('NSW', '').replace('=', '')
				print(line)
				#exec(line)
				NSW = int(number)
				#import pdb; pdb.set_trace()
				if NSW == 0:
					break
				else:
					print('================================================')
					print('Error in LatticeFinder')
					print('You need to set NSW = 0 in your INCAR')
					print('NSW = '+str(NSW))
					print('Check this out. This program will finish without completing.')
					print('================================================')
					exit()
		else:
			print('================================================')
			print('Error in LatticeFinder')
			print('You need to set NSW = 0 in your INCAR')
			prtin('You do not have NSW in your INCAR')
			print('Check this out. This program will finish without completing.')
			print('================================================')
			exit()

def make_packet_submitSL_files(root,all_directories,slurm_information):
	"""

	"""
	project = slurm_information['project']
	time = slurm_information['time']
	nodes = slurm_information['nodes']
	ntasks_per_node = slurm_information['ntasks_per_node']
	mem_per_cpu = slurm_information['mem-per-cpu']
	partition = slurm_information['partition']
	email = slurm_information['email']
	python_version = slurm_information['python_version']
	vasp_version = slurm_information['vasp_version']
	vasp_execution = slurm_information['vasp_execution']
	# other stuff
	number_of_vasp_calc_to_run_per_packet = slurm_information['Number of VASP calculations to run per packet']
	make_submitSL_packets_for_latticeFinder(number_of_vasp_calc_to_run_per_packet,all_directories,root,project,time,nodes,ntasks_per_node,mem_per_cpu,partition=partition,email=email,python_version=python_version,vasp_version=vasp_version,vasp_execution=vasp_execution)

def make_individual_submitSL_files(root,slurm_information):
	"""

	"""
	project = slurm_information['project']
	time = slurm_information['time']
	nodes = slurm_information['nodes']
	ntasks_per_node = slurm_information['ntasks_per_node']
	mem_per_cpu = slurm_information['mem-per-cpu']
	partition = slurm_information['partition']
	email = slurm_information['email']
	python_version = slurm_information['python_version']
	vasp_version = slurm_information['vasp_version']
	vasp_execution = slurm_information['vasp_execution']
	make_submitSL(root,project,time,nodes,ntasks_per_node,mem_per_cpu,partition=partition,email=email,python_version=python_version,vasp_version=vasp_version,vasp_execution=vasp_execution)

def get_VASP_energies(lattice_constant_generator,lattice_data_file=None,folder_name='VASP_Clusters',lattice_type_name=None,energies_vs_lattice_constants={}):
	"""

	"""
	#check_lattice_data_file(lattice_data_file,energies_vs_lattice_constants=energies_vs_lattice_constants)
	slurm_information = {}
	clusters_not_calculated = []
	lattice_constant_generator.reset()
	for latticeconstants in lattice_constant_generator:
		name = get_folder_name(latticeconstants)
		energy_per_atom, bulk_system = get_VASP_energy_per_atom(folder_name+'/'+name)
		if not isinstance(energy_per_atom,float):
			clusters_not_calculated.append((latticeconstants,folder_name+'/'+name))
			continue
		if isinstance(latticeconstants,dict):
			latticeconstants = tuple(lc_value for lc_key, lc_value in sorted(latticeconstants.items()))
			save_datum_to_file(lattice_data_file,latticeconstants,energy_per_atom, volume=None)
			slurm_information[latticeconstants] = energy_per_atom
		else:
			volume = get_volume_per_atom(bulk_system)
			save_datum_to_file(lattice_data_file,latticeconstants,energy_per_atom, volume=volume)
			slurm_information[latticeconstants] = (energy_per_atom,volume)
	if len(clusters_not_calculated):
		print('=======================================================================================')
		print('Error: The following data has not completed and need to be obtained before continuing.')
		for latticeconstants, path_to in clusters_not_calculated:
			print('Lattice Constant: '+str(latticeconstants)+ ' Angstrom ('+str(path_to)+')')
		lc_types = lattice_constant_generator.get_lattice_constant_types()
		if len(lc_types) == 1:
			print('As '+lattice_type_name+' only has one lattice constant, this is not an issue if you do not suspect this lattice constant to be the optimal lattice constant.')
			print('Will continue on, ONLY A WARNING HERE.')
		else:
			print('This program will finish without completing.')
			print('=======================================================================================')
			exit()
	lattice_constant_generator.reset()
	return slurm_information

def check_lattice_data_file(lattice_data_file,energies_vs_lattice_constants={}):
	"""

	"""
	suffix = '.new'
	with open(lattice_data_file,'r') as lattice_data_file_old:
		with open(lattice_data_file+suffix,'w') as lattice_data_file_new:
			for _ in range(12):
				lattice_data_file_new.write(lattice_data_file_old.readline())
	os.remove(lattice_data_file)
	os.rename(lattice_data_file+suffix,lattice_data_file)

def get_VASP_energy_per_atom(folder):
	"""

	"""
	try:
		system = read(folder+'/OUTCAR')
		energy = system.get_potential_energy()
		no_of_atoms = float(len(system))
		energy_per_atom = energy/no_of_atoms
	except Exception:
		energy_per_atom, system = None, None
	return energy_per_atom, system
