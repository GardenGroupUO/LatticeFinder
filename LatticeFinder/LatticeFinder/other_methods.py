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

def get_lattice_type(self,lattice_type):
	lattice_dictionary = {'SimpleCubic': SimpleCubic, 'FaceCenteredCubic': FaceCenteredCubic, 'BodyCenteredCubic': BodyCenteredCubic, 'Diamond': Diamond, 'SimpleTetragonal': SimpleTetragonal, 'CenteredTetragonal': CenteredTetragonal, 'BaseCenteredOrthorhombic': BaseCenteredOrthorhombic, 'FaceCenteredOrthorhombic': FaceCenteredOrthorhombic, 'BodyCenteredOrthorhombic': BodyCenteredOrthorhombic, 'Triclinic': Triclinic, 'Hexagonal': Hexagonal, 'HexagonalClosedPacked': HexagonalClosedPacked, 'Graphite': Graphite, 'B1': B1, 'B2': B2, 'B3': B3, 'L1_2': L1_2, 'L1_0': L1_0}
	for key, value in lattice_dictionary.item():
		if lattice_type == key:
			return value
	else:
		print('Error in LatticeFinder: You have not given a valid lattice_type')
		print('The types of lattices that are valid are:')
		print(list(lattice_dictionary.keys())
		print('See https://wiki.fysik.dtu.dk/ase/ase/lattice.html#available-crystal-lattices for more information')
		print('This program with finish without completing')
		exit()