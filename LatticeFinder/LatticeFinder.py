import os, time
import numpy as np
from shutil import copyfile
from ase.io import write
import multiprocessing as mp

from LatticeFinder.lattice_constant_generator import lattice_constant_generator

from ase.lattice.cubic import SimpleCubic, FaceCenteredCubic, BodyCenteredCubic, Diamond
from ase.lattice.tetragonal import SimpleTetragonal, CenteredTetragonal
from ase.lattice.orthorhombic import SimpleOrthorhombic, BaseCenteredOrthorhombic, FaceCenteredOrthorhombic, BodyCenteredOrthorhombic
from ase.lattice.monoclinic import SimpleMonoclinic, BaseCenteredMonoclinic
from ase.lattice.triclinic import Triclinic
from ase.lattice.hexagonal import Hexagonal, HexagonalClosedPacked, Graphite
from ase.lattice.compounds import B1, B2, B3, L1_2, L1_0

from plotting_methods import plot_energy_vs_lattice_constants_1D, plot_energy_vs_lattice_constants_1D

class LatticeFinder_Program:
	"""

	"""
	def __init__(self, symbol, lattice_type, lattice_constant_parameters, calculator, size=(1,1,1), directions=None, miller=None, limits=None, no_of_cpus=1):
		# General options
		self.symbol = symbol
		self.get_lattice_type(lattice_type)
		self.lattice_constant_parameters = lattice_constant_parameters
		self.calculator = calculator
		self.size = size
		# Other options about constructing the cell
		self.directions = directions
		self.miller = miller
		# Plotting inuts
		self.limits = limits
		# Other options
		self.no_of_cpus = no_of_cpus
		# Run the program
		self.run()

	def get_lattice_type(self,lattice_type):
		"""

		"""
		self.lattice_type_name = lattice_type
		if isinstance(lattice_type,dict):
			if lattice_type['type'] == 'VASP':
				self.lattice_type = lattice_type['type']
				self.directory_with_vasp_files = lattice_type['Directory with VASP Files']
			else:
				exit('Error VASP')
		else:
			self.lattice_type = eval(lattice_type)

	############################################################################################################################

	def run(self):
		"""

		"""
		self.checks(self.lattice_constant_parameters)
		self.lattice_constant_generator = lattice_constant_generator(self.lattice_constant_parameters)
		self.lattice_constant_types = self.lattice_constant_generator.get_lattice_constant_types()
		self.lattice_data_file = 'lattice_data.txt'
		energies_vs_lattice_constants = self.setup_energies_vs_lattice_constants()
		self.get_data(energies_vs_lattice_constants)
		self.minimum_energy, self.lowest_energy_lattice_constants = self.get_minimum_energy(energies_vs_lattice_constants)
		self.plot_energy_vs_lattice_constants(energies_vs_lattice_constants)
		self.get_other_data_about_system(self.minimum_energy, self.lowest_energy_lattice_constants)

	############################################################################################################################

	def checks(self,lattice_constant_parameters):
		"""

		"""
		if isinstance(lattice_constant_parameters,tuple) or isinstance(lattice_constant_parameters,list):
			pass
		elif isinstance(lattice_constant_parameters,dict):
			for lattice_constant_type, lattice_constant_parameter in self.lattice_constant_parameters.items():
				if isinstance(lattice_constant_parameter,tuple) or isinstance(lattice_constant_parameter,list):
					continue
		else:
			exit('error 3')

	############################################################################################################################

	def setup_energies_vs_lattice_constants(self):
		"""

		"""
		if os.path.exists(self.lattice_data_file):
			energies_vs_lattice_constants = self.load_data()
		else:
			self.setup_initial_data_file()
			energies_vs_lattice_constants = {}
		return energies_vs_lattice_constants

	def load_data(self):
		"""

		"""
		energies_vs_lattice_constants = {}
		leading_data = False
		with open(self.lattice_data_file,'r') as lattice_data_FILE:
			for _ in range(9):
				lattice_data_FILE.readline()
			for line in lattice_data_FILE:
				lattice_constants, energy_per_atom = line.rstrip('\n').split(':')
				lattice_constants = eval(lattice_constants)
				energy_per_atom = float(energy_per_atom)
				energies_vs_lattice_constants[lattice_constants] = energy_per_atom
		return energies_vs_lattice_constants

	def setup_initial_data_file(self):
		"""

		"""
		with open(self.lattice_data_file,'w') as lattice_data_FILE:
			lattice_data_FILE.write('Symbol: '+str(self.symbol)+'\n')
			lattice_data_FILE.write('Lattice_type: '+str(self.lattice_type_name)+'\n')
			lattice_data_FILE.write('calculator: '+str(self.calculator)+'\n')
			lattice_data_FILE.write('size: '+str(self.size)+'\n')
			lattice_data_FILE.write('directions: '+str(self.directions)+'\n')
			lattice_data_FILE.write('miller: '+str(self.miller)+'\n')
			lattice_data_FILE.write('Lattice Constant Parameters: '+str(self.lattice_constant_types)+'\n')
			lattice_data_FILE.write('\n')
			lattice_data_FILE.write('Lattice Constant Results: \n')

	############################################################################################################################
	from examining_lattice_constant_methods import get_energies_across_lattice_constants_VASP, get_energies_across_lattice_constants_ASE
	def get_data(self, energies_vs_lattice_constants):
		"""

		"""
		if self.calculator == 'VASP':
			get_energies_across_lattice_constants_VASP(self.lattice_type,self.symbol,self.lattice_constant_generator,self.size,self.directions,self.miller)
			exit()
		else:
			get_energies_across_lattice_constants_ASE (self.lattice_type,self.symbol,self.lattice_constant_generator,self.size,self.directions,miller,self.calculator,self.no_of_cpus,self.lattice_data_file,self.energies_vs_lattice_constants)

	############################################################################################################################

	def get_minimum_energy(self,energies_vs_lattice_constants):
		"""

		"""
		lowest_energy_per_atoms = float('inf')
		all_lattice_constants = []
		for lattice_constants, energy_per_atoms in energies_vs_lattice_constants.items():
			if energy_per_atoms < lowest_energy_per_atoms:
				lowest_energy_per_atoms = energy_per_atoms
				all_lattice_constants = [lattice_constants]
			elif energy_per_atoms == lowest_energy_per_atoms:
				all_lattice_constants.append(lattice_constants)
		return lowest_energy_per_atoms, all_lattice_constants

	############################################################################################################################

	def plot_energy_vs_lattice_constants(self, energies_vs_lattice_constants):
		"""

		"""
		if len(self.lattice_constant_types) == 1:
			self.plot_energy_vs_lattice_constants_1D(energies_vs_lattice_constants)
		if len(self.lattice_constant_types) == 2:
			self.plot_energy_vs_lattice_constants_2D(energies_vs_lattice_constants)

	############################################################################################################################

	def get_other_data_about_system(self,minimum_energy,lowest_energy_lattice_constants):
		"""

		"""
		if len(lowest_energy_lattice_constants) == 1:
			latticeconstants = lowest_energy_lattice_constants[0]
		else:
			latticeconstants = {key: value for key, value in zip(self.lattice_constant_types,lowest_energy_lattice_constants)}
		bulk_system = self.lattice_type(symbol=self.symbol, latticeconstant=latticeconstants, size=self.size)
		bulk_system.set_calculator(self.calculator)
		
		energy = bulk_system.get_potential_energy(bulk_system)
		no_of_atoms = len(bulk_system)
		energy_per_atom = energy/float(no_of_atoms)

		Volume = bulk_system.get_volume()
		Volume_per_atom = float(Volume)/float(no_of_atoms)
		stress_tensor = bulk_system.get_stress(voigt=False)

		bulk_modulus = 1

		with open('results_file.txt','w') as results_fileTXT:
			results_fileTXT.write('Symbol: '+str(self.symbol)+'\n')
			results_fileTXT.write('Lattice_type: '+str(self.lattice_type_name)+'\n')
			results_fileTXT.write('calculator: '+str(self.calculator)+'\n')
			results_fileTXT.write('size: '+str(self.size)+'\n')
			results_fileTXT.write('directions: '+str(self.directions)+'\n')
			results_fileTXT.write('miller: '+str(self.miller)+'\n')
			results_fileTXT.write('Lattice Constant Parameters: '+str(self.lattice_constant_types)+'\n')
			results_fileTXT.write('\n')
			results_fileTXT.write('Properties of System: \n')	
			results_fileTXT.write('\n')
			results_fileTXT.write('Total energy: '+str(energy)+' eV\n')
			results_fileTXT.write('No. of atoms: '+str(no_of_atoms)+' Atoms (Note the number of atoms along each natural direction of the bulk is '+str(self.size)+')\n')
			results_fileTXT.write('Cohesive energy: '+str(energy_per_atom)+' eV/Atom\n')
			results_fileTXT.write('\n')
			results_fileTXT.write('Total Volume: '+str(Volume)+' Angstroms^3\n')
			results_fileTXT.write('Volume per atom: '+str(Volume_per_atom)+' Angstroms^3/Atom\n')
			results_fileTXT.write('\n')
			results_fileTXT.write('Stress tensor:\n'+str(stress_tensor)+'\n')
			results_fileTXT.write('\n')
			results_fileTXT.write('Bulk Modulus: '+str(bulk_modulus)+' GPa\n')

	############################################################################################################################