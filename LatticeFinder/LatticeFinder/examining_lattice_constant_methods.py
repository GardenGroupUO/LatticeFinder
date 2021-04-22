

def get_energies_across_lattice_constants_VASP(lattice_type,symbol,lattice_constant_generator,size,directions=None,miller=None):
	"""

	"""
	for latticeconstants in lattice_constant_generator:
		bulk_system = lattice_type(symbol=symbol, latticeconstant=latticeconstants, size=size) #, directions=directions, miller=miller)


def save_datum_to_file(lattice_data_file,latticeconstants,energy_per_atom):
	"""

	"""
	with open(lattice_data_file,'a') as lattice_data_FILE:
		lattice_data_FILE.write(str(latticeconstants)+': '+str(energy_per_atom)+'\n')

def get_energies_across_lattice_constants_ASE_single(lattice_type,symbol,latticeconstants,size,directions,miller,calculator,lattice_data_file,energies_vs_lattice_constants):
	"""

	"""
	latticeconstants_for_dict = tuple(latticeconstants[lattice_constant_types[index]] for index in range(len(lattice_constant_types)))
	if latticeconstants_for_dict in energies_vs_lattice_constants.keys():
		return
	print(latticeconstants)
	bulk_system = lattice_type(symbol=symbol, latticeconstant=latticeconstants, size=size) #, directions=directions, miller=miller)
	bulk_system.set_calculator(calculator)
	energy = bulk_system.get_potential_energy(bulk_system)
	energy_per_atom = energy/float(len(bulk_system))
	save_datum_to_file(lattice_data_file,latticeconstants_for_dict,energy_per_atom)
	energies_vs_lattice_constants[latticeconstants_for_dict] = energy_per_atom

def get_energies_across_lattice_constants_ASE(lattice_type,symbol,lattice_constant_generator,size,directions=None,miller=None,calculator=None,no_of_cpus=1,lattice_data_file=None,energies_vs_lattice_constants={}):
	print('================================================================================')
	if no_of_cpus == 1:
		get_energies_across_lattice_constants_ASE_one_cpu(lattice_type,symbol,lattice_constant_generator,size,directions,miller,calculator,lattice_data_file,energies_vs_lattice_constants)
	else:
		get_energies_across_lattice_constants_ASE_multi_cpu(lattice_type,symbol,lattice_constant_generator,size,directions,miller,calculator,lattice_data_file,energies_vs_lattice_constants)
	print('================================================================================')

def get_energies_across_lattice_constants_ASE_one_cpu(lattice_type,symbol,lattice_constant_generator,size,directions=None,miller=None,calculator=None,lattice_data_file=None,energies_vs_lattice_constants={}):
	for latticeconstants in lattice_constant_generator:
		get_energies_across_lattice_constants_ASE_single(lattice_type,symbol,latticeconstants,size,directions,miller,calculator,lattice_data_file,energies_vs_lattice_constants)

def get_energies_across_lattice_constants_ASE_multi_cpu(lattice_type,symbol,lattice_constant_generator,size,directions=None,miller=None,calculator=None,no_of_cpus=1,lattice_data_file=None,energies_vs_lattice_constants={}):
	pass