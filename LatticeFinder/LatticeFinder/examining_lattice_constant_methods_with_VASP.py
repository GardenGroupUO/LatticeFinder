

def get_energies_across_lattice_constants_VASP(lattice_type,symbol,lattice_constant_generator,size,directions=None,miller=None):
	"""

	"""
	for latticeconstants in lattice_constant_generator:
		bulk_system = lattice_type(symbol=symbol, latticeconstant=latticeconstants, size=size) #, directions=directions, miller=miller)

