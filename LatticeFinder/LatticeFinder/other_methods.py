from copy import deepcopy

from ase.lattice.cubic import SimpleCubic, FaceCenteredCubic, BodyCenteredCubic, Diamond 
from ase.lattice.tetragonal import SimpleTetragonal, CenteredTetragonal 
from ase.lattice.orthorhombic import SimpleOrthorhombic, BaseCenteredOrthorhombic, FaceCenteredOrthorhombic, BodyCenteredOrthorhombic 
from ase.lattice.monoclinic import SimpleMonoclinic, BaseCenteredMonoclinic 
from ase.lattice.triclinic import Triclinic 
from ase.lattice.hexagonal import Hexagonal, HexagonalClosedPacked, Graphite
from ase.lattice.compounds import B1, B2, B3, L1_2, L1_0 

def round_lattice_constant_parameters(lattice_constant_parameters):
	rounding_to = 8
	lattice_constant_parameters_copy = deepcopy(lattice_constant_parameters)
	new_lattice_constant_parameters = []
	if isinstance(lattice_constant_parameters_copy,list) or isinstance(lattice_constant_parameters_copy,tuple):
		for number in lattice_constant_parameters_copy:
			new_lattice_constant_parameters.append(round(number,rounding_to))
	return new_lattice_constant_parameters

def get_lattice_type(lattice_type):
	lattice_dictionary = {}
	lattice_dictionary['SimpleCubic'] = SimpleCubic
	lattice_dictionary['FaceCenteredCubic'] = FaceCenteredCubic
	lattice_dictionary['BodyCenteredCubic'] = BodyCenteredCubic
	lattice_dictionary['Diamond'] = Diamond
	lattice_dictionary['SimpleTetragonal'] = SimpleTetragonal
	lattice_dictionary['CenteredTetragonal'] = CenteredTetragonal
	lattice_dictionary['SimpleOrthorhombic'] = SimpleOrthorhombic
	lattice_dictionary['BaseCenteredOrthorhombic'] = BaseCenteredOrthorhombic
	lattice_dictionary['FaceCenteredOrthorhombic'] = FaceCenteredOrthorhombic
	lattice_dictionary['BodyCenteredOrthorhombic'] = BodyCenteredOrthorhombic
	lattice_dictionary['SimpleMonoclinic'] = SimpleMonoclinic
	lattice_dictionary['BaseCenteredMonoclinic'] = BaseCenteredMonoclinic
	lattice_dictionary['Triclinic'] = Triclinic
	lattice_dictionary['Hexagonal'] = Hexagonal
	lattice_dictionary['HexagonalClosedPacked'] = HexagonalClosedPacked
	lattice_dictionary['Graphite'] = Graphite
	lattice_dictionary['B1'] = B1
	lattice_dictionary['B2'] = B2
	lattice_dictionary['B3'] = B3
	lattice_dictionary['L1_2'] = L1_2
	lattice_dictionary['L1_0'] = L1_0
	for key, value in lattice_dictionary.items(): # lgtm [py/redundant-else]
		if lattice_type == key:
			return value
	else:
		print('Error in LatticeFinder: You have not given a valid lattice_type')
		print('The types of lattices that are valid are:')
		print(list(lattice_dictionary.keys()))
		print('See wiki.fysik.dtu.dk/ase/ase/lattice.html#available-crystal-lattices for more information')
		print('This program with finish without completing')
		exit()