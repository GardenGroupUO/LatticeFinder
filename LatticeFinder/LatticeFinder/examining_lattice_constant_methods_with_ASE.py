import multiprocessing as mp

def get_energies_across_lattice_constants_ASE(lattice_type,symbol,lattice_constant_generator,lattice_constant_types,size,directions=None,miller=None,calculator=None,no_of_cpus=1,lattice_data_file=None,energies_vs_lattice_constants={}):
	"""
	This method allows the user to obtain lattice constant information about your system using an ase based calculator (and local optimiser)
	"""
	print('================================================================================')
	global calculator_ASE
	calculator_ASE = calculator
	if no_of_cpus == 1:
		get_energies_across_lattice_constants_ASE_one_cpu(lattice_type,symbol,lattice_constant_generator,lattice_constant_types,size,directions,miller,lattice_data_file,energies_vs_lattice_constants)
	else:
		get_energies_across_lattice_constants_ASE_multi_cpu(lattice_type,symbol,lattice_constant_generator,lattice_constant_types,size,directions,miller,no_of_cpus,lattice_data_file,energies_vs_lattice_constants)
	print('================================================================================')

def get_energies_across_lattice_constants_ASE_one_cpu(lattice_type,symbol,lattice_constant_generator,lattice_constant_types,size,directions=None,miller=None,lattice_data_file=None,energies_vs_lattice_constants={}):
	"""

	"""
	for latticeconstants in lattice_constant_generator:
		get_energies_across_lattice_constants_ASE_single(lattice_type,symbol,latticeconstants,lattice_constant_types,size,directions,miller,lattice_data_file,energies_vs_lattice_constants)

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
	energy = bulk_system.get_potential_energy(bulk_system)
	energy_per_atom = energy/float(len(bulk_system))
	if one_lattice_constant:
		volume = get_volume_per_atom(bulk_system)
		energies_vs_lattice_constants[latticeconstants_for_dict] = (energy_per_atom,volume)
	else:
		volume = None
		energies_vs_lattice_constants[latticeconstants_for_dict] = energy_per_atom
	if not qq is None:
		res = (lattice_data_file,latticeconstants_for_dict,energy_per_atom,volume)
		qq.put(res)
	else:
		save_datum_to_file(lattice_data_file,latticeconstants_for_dict,energy_per_atom,volume)

def get_volume_per_atom(bulk_system):
	volume = round(bulk_system.get_volume()/float(len(bulk_system)),9)
	return volume

def save_datum_to_file(lattice_data_file,latticeconstants,energy_per_atom, volume=None):
	"""

	"""
	with open(lattice_data_file,'a') as lattice_data_FILE:
		if volume == None:
			lattice_data_FILE.write(str(latticeconstants)+': '+str(energy_per_atom)+'\n')
		else:
			lattice_data_FILE.write(str(latticeconstants)+': '+str(energy_per_atom)+' ('+str(volume)+')\n')

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------v
import multiprocessing as mp
def get_energies_across_lattice_constants_ASE_multi_cpu(lattice_type,symbol,lattice_constant_generator,lattice_constant_types,size,directions=None,miller=None,no_of_cpus=1,lattice_data_file=None,energies_vs_lattice_constants={}):
	"""

	"""
	manager = mp.Manager()
	qq = manager.Queue()    
	pool = mp.Pool(processes=no_of_cpus)
	#put listener to work first
	watcher = pool.apply_async(listener, (q,))
	#fire off workers
	dictionary_multiprocessing = manager.dict()
	jobs = []
	for latticeconstants in lattice_constant_generator:
		task = (lattice_type,symbol,latticeconstants,lattice_constant_types,size,directions,miller,lattice_data_file,dictionary_multiprocessing,qq)
		job = pool.apply_async(get_energies_across_lattice_constants_ASE_single, task)
		jobs.append(job)
	# collect results from the workers through the pool result queue
	for job in jobs: 
		job.get()
	for key, value in dictionary_multiprocessing.items()
	energies_vs_lattice_constants[key] = value
	#now we are done, kill the listener
	pool.close()
	pool.join()

def listener(q):
    '''listens for messages on the q, writes to file. '''	
    m = q.get()
    lattice_data_file,latticeconstants_for_dict,energy_per_atom,volume = m
    save_datum_to_file(lattice_data_file,latticeconstants_for_dict,energy_per_atom,volume)

