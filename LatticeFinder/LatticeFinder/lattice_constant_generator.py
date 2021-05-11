import numpy as np
import itertools
from copy import deepcopy

# Using the generator pattern (an iterable)
class lattice_constant_generator:

	def __init__(self, lattice_constant_parameters):
		self.rounding_to = 8
		if isinstance(lattice_constant_parameters,tuple) or isinstance(lattice_constant_parameters,list):
			lattice_constant_parameters = {'c': lattice_constant_parameters}
		generators = []
		for lattice_constant_type, lattice_constant_parameter in lattice_constant_parameters.items():
			if (isinstance(lattice_constant_parameter,tuple) or isinstance(lattice_constant_parameter,list)) and len(lattice_constant_parameter) == 3:
				lc_low, lc_high, lc_resolution = lattice_constant_parameter
				if isinstance(lc_resolution,float):
					generators.append((lattice_constant_type, tuple(np.arange(lc_low, lc_high+lc_resolution, lc_resolution))))
				elif isinstance(lc_resolution,int):
					generators.append((lattice_constant_type, tuple(np.linspace(lc_low, lc_high, lc_resolution, endpoint=True))))
			else:
				generators.append((lattice_constant_type, lattice_constant_parameter))
		generators.sort()
		self.lattice_constant_types = sorted([lattice_constant_type for lattice_constant_type, generator in generators])
		self.generators = [generator for lattice_constant_type, generator in generators]
		self.lattice_constant_generator = itertools.product(*deepcopy(self.generators))

	def __iter__(self):
		return self

	def get_lattice_constant_types(self):
		return self.lattice_constant_types

	def reset(self):
		self.lattice_constant_generator = itertools.product(*deepcopy(self.generators))

	# Python 3 compatibility
	def __next__(self):
		return self.next()

	def next(self):
		try:
			lattice_constants = next(self.lattice_constant_generator)
			if isinstance(lattice_constants,tuple) or isinstance(lattice_constants,list):
				if len(lattice_constants) == 1:
					lattice_constants = round(lattice_constants[0],self.rounding_to)
				else:
					lattice_constants = {key: round(value,self.rounding_to) for key, value in zip(self.lattice_constant_types,lattice_constants)}
				#lattice_constants = {key: round(value,self.rounding_to) for key, value in zip(self.lattice_constant_types,lattice_constants)}
			return lattice_constants
		except StopIteration:
			raise StopIteration()