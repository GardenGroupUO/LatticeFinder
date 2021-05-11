from copy import deepcopy

def round_lattice_constant_parameters(lattice_constant_parameters):
	rounding_to = 8
	lattice_constant_parameters_copy = deepcopy(lattice_constant_parameters)
	new_lattice_constant_parameters = []
	if isinstance(lattice_constant_parameters_copy,list) or isinstance(lattice_constant_parameters_copy,tuple):
		for number in lattice_constant_parameters_copy:
			new_lattice_constant_parameters.append(round(number,rounding_to))
	return new_lattice_constant_parameters