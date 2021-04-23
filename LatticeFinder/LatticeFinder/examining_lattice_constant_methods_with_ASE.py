import multiprocessing as mp

def get_energies_across_lattice_constants_ASE(lattice_type,symbol,lattice_constant_generator,lattice_constant_types,size,directions=None,miller=None,calculator=None,no_of_cpus=1,lattice_data_file=None,energies_vs_lattice_constants={}):
	"""
	This method allows the user to obtain lattice constant information about your system using an ase based calculator (and local optimiser)
	"""
	print('================================================================================')
	if no_of_cpus == 1:
		get_energies_across_lattice_constants_ASE_one_cpu(lattice_type,symbol,lattice_constant_generator,lattice_constant_types,size,directions,miller,calculator,lattice_data_file,energies_vs_lattice_constants)
	else:
		get_energies_across_lattice_constants_ASE_multi_cpu(lattice_type,symbol,lattice_constant_generator,lattice_constant_types,size,directions,miller,calculator,lattice_data_file,energies_vs_lattice_constants)
	print('================================================================================')

def get_energies_across_lattice_constants_ASE_one_cpu(lattice_type,symbol,lattice_constant_generator,lattice_constant_types,size,directions=None,miller=None,calculator=None,lattice_data_file=None,energies_vs_lattice_constants={}):
	"""

	"""
	for latticeconstants in lattice_constant_generator:
		get_energies_across_lattice_constants_ASE_single(lattice_type,symbol,latticeconstants,lattice_constant_types,size,directions,miller,calculator,lattice_data_file,energies_vs_lattice_constants)

def get_energies_across_lattice_constants_ASE_multi_cpu(lattice_type,symbol,lattice_constant_generator,lattice_constant_types,size,directions=None,miller=None,calculator=None,no_of_cpus=1,lattice_data_file=None,energies_vs_lattice_constants={}):
	"""

	"""
	with mp.Pool(processes=no_of_cpus) as pool: # pool = mp.Pool()
		results = pool.map_async(get_energies_across_lattice_constants_ASE_single, lattice_constant_generator)
		results.wait()
	offsprings = results.get()

def get_volume_per_atom(bulk_system):
	volume = round(bulk_system.get_volume()/float(len(bulk_system)),9)
	return volume

def get_energies_across_lattice_constants_ASE_single(lattice_type,symbol,latticeconstants,lattice_constant_types,size,directions,miller,calculator,lattice_data_file,energies_vs_lattice_constants):
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
	bulk_system.set_calculator(calculator)
	energy = bulk_system.get_potential_energy(bulk_system)
	energy_per_atom = energy/float(len(bulk_system))
	if one_lattice_constant:
		volume = get_volume_per_atom(bulk_system)
		energies_vs_lattice_constants[latticeconstants_for_dict] = (energy_per_atom,volume)
	else:
		volume = None
		energies_vs_lattice_constants[latticeconstants_for_dict] = energy_per_atom
	save_datum_to_file(lattice_data_file,latticeconstants_for_dict,energy_per_atom,volume)

def make_lock_file(self):
	with open('file.lock','w') as lockFILE:
			write('')

def save_datum_to_file(lattice_data_file,latticeconstants,energy_per_atom, volume=None):
	"""

	"""
	with open(lattice_data_file,'a') as lattice_data_FILE:
		if volume == None:
			lattice_data_FILE.write(str(latticeconstants)+': '+str(energy_per_atom)+'\n')
		else:
			lattice_data_FILE.write(str(latticeconstants)+': '+str(energy_per_atom)+' ('+str(volume)+' Ang/atom)\n')
			