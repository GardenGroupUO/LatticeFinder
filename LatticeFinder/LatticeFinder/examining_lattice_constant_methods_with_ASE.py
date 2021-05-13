
def get_energies_across_lattice_constants_ASE(lattice_type,symbol,lattice_constant_generator,lattice_constant_types,size,directions=None,miller=None,calculator=None,no_of_cpus=1,lattice_data_file=None,energies_vs_lattice_constants={}):
	"""
	This method allows the user to obtain lattice constant information about your system using an ase based calculator (and local optimiser)
	"""
	print('================================================================================')
	global calculator_ASE
	calculator_ASE = calculator
	if no_of_cpus == 1:
		energies_vs_lattice_constants = get_energies_across_lattice_constants_ASE_one_cpu(lattice_type,symbol,lattice_constant_generator,lattice_constant_types,size,directions,miller,lattice_data_file,energies_vs_lattice_constants)
	else:
		energies_vs_lattice_constants = get_energies_across_lattice_constants_ASE_multi_cpu(lattice_type,symbol,lattice_constant_generator,lattice_constant_types,size,directions,miller,no_of_cpus,lattice_data_file,energies_vs_lattice_constants)
	print('================================================================================')
	return energies_vs_lattice_constants

def get_energies_across_lattice_constants_ASE_one_cpu(lattice_type,symbol,lattice_constant_generator,lattice_constant_types,size,directions=None,miller=None,lattice_data_file=None,energies_vs_lattice_constants={}):
	"""

	"""
	for latticeconstants in lattice_constant_generator:
		get_energies_across_lattice_constants_ASE_single(lattice_type,symbol,latticeconstants,lattice_constant_types,size,directions,miller,lattice_data_file,energies_vs_lattice_constants,qq=None)
	return energies_vs_lattice_constants

def get_energies_across_lattice_constants_ASE_single(lattice_type,symbol,latticeconstants,lattice_constant_types,size,directions,miller,lattice_data_file,energies_vs_lattice_constants,qq=None):
	"""

	"""
	if isinstance(latticeconstants,dict):
		latticeconstants_for_dict = tuple(latticeconstants[lattice_constant_types[index]] for index in range(len(lattice_constant_types)))
		one_lattice_constant = False
	else:
		latticeconstants_for_dict = latticeconstants
		one_lattice_constant = True
	if latticeconstants_for_dict in energies_vs_lattice_constants.keys():
		return
	print(latticeconstants)
	bulk_system = lattice_type(symbol=symbol, latticeconstant=latticeconstants, size=size) #, directions=directions, miller=miller)
	global calculator_ASE

	bulk_system.set_calculator(calculator_ASE)
	energy_per_atom = get_energy_per_atom(bulk_system)
	if one_lattice_constant:
		volume_per_atom = get_volume_per_atom(bulk_system)
		energies_vs_lattice_constants[latticeconstants_for_dict] = (energy_per_atom,volume_per_atom)
	else:
		volume_per_atom = None
		energies_vs_lattice_constants[latticeconstants_for_dict] = energy_per_atom
	if not qq is None:
		res = (lattice_data_file,latticeconstants_for_dict,energy_per_atom,volume_per_atom)
		qq.put(res)
	else:
		save_datum_to_file(lattice_data_file,latticeconstants_for_dict,energy_per_atom,volume_per_atom)

def get_energy_per_atom(bulk_system):
	energy = bulk_system.get_potential_energy(bulk_system)
	energy_per_atom = energy/float(len(bulk_system))
	return energy_per_atom

def get_volume_per_atom(bulk_system):
	volume_per_atom = round(bulk_system.get_volume()/float(len(bulk_system)),9)
	return volume_per_atom

def save_datum_to_file(lattice_data_file,latticeconstants,energy_per_atom, volume=None):
	"""

	"""
	with open(lattice_data_file,'a') as lattice_data_FILE:
		if volume is None:
			lattice_data_FILE.write(str(latticeconstants)+': '+str(energy_per_atom)+'\n')
		else:
			lattice_data_FILE.write(str(latticeconstants)+': '+str(energy_per_atom)+' ('+str(volume)+')\n')

def get_system_from_ASE(lattice_type,symbol,latticeconstants,size,directions,miller,calculator):
	"""

	"""	
	bulk_systems = []
	for a_latticeconstants in latticeconstants:
		bulk_system = lattice_type(symbol=symbol, latticeconstant=a_latticeconstants, size=size)
		bulk_system.set_calculator(calculator)
		bulk_systems.append(bulk_system)
	return bulk_systems

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------v
import multiprocessing as mp
def get_energies_across_lattice_constants_ASE_multi_cpu(lattice_type,symbol,lattice_constant_generator,lattice_constant_types,size,directions=None,miller=None,no_of_cpus=1,lattice_data_file=None,energies_vs_lattice_constants={}):
	"""

	"""
	# solution from https://stackoverflow.com/questions/13446445/python-multiprocessing-safely-writing-to-a-file
	manager = mp.Manager()
	qq = manager.Queue()    
	pool = mp.Pool(processes=no_of_cpus)
	#put listener to work first
	pool.apply_async(listener, (qq,))
	#fire off workers
	dictionary_multiprocessing = manager.dict()
	dictionary_multiprocessing.update(energies_vs_lattice_constants)
	del energies_vs_lattice_constants
	print('Performing calculations upon Lattices')
	jobs = []
	for latticeconstants in lattice_constant_generator:
		task = (lattice_type,symbol,latticeconstants,lattice_constant_types,size,directions,miller,lattice_data_file,dictionary_multiprocessing,qq)
		job = pool.apply_async(get_energies_across_lattice_constants_ASE_single, task)
		jobs.append(job)
	# collect results from the workers through the pool result queue
	for job in jobs: 
		job.get()
	print('Finished performing calculations upon Lattices')
	print('Performing last finishing off pieces of work')
	energies_vs_lattice_constants = dict(dictionary_multiprocessing)
	#now we are done, kill the listener
	qq.put('kill')
	pool.close()
	pool.join()
	print('Finished performing last finishing off pieces of work')
	return energies_vs_lattice_constants

def listener(qq):
	'''listens for messages on the q, writes to file. '''	
	while True:
		mm = qq.get()
		if mm == 'kill':
			break
		lattice_data_file,latticeconstants_for_dict,energy_per_atom,volume = mm
		save_datum_to_file(lattice_data_file,latticeconstants_for_dict,energy_per_atom,volume)

