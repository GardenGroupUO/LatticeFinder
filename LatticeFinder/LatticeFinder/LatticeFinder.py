import os, time
import numpy as np
from shutil import copyfile
from ase.io import write
import multiprocessing as mp
import matplotlib.pyplot as plt

from LatticeFinder.LatticeFinder.lattice_constant_generator import lattice_constant_generator

from ase.lattice.cubic import SimpleCubic, FaceCenteredCubic, BodyCenteredCubic, Diamond
from ase.lattice.tetragonal import SimpleTetragonal, CenteredTetragonal
from ase.lattice.orthorhombic import SimpleOrthorhombic, BaseCenteredOrthorhombic, FaceCenteredOrthorhombic, BodyCenteredOrthorhombic
from ase.lattice.monoclinic import SimpleMonoclinic, BaseCenteredMonoclinic
from ase.lattice.triclinic import Triclinic
from ase.lattice.hexagonal import Hexagonal, HexagonalClosedPacked, Graphite
from ase.lattice.compounds import B1, B2, B3, L1_2, L1_0

from LatticeFinder.LatticeFinder.examining_lattice_constant_methods_with_ASE         import get_energies_across_lattice_constants_ASE
from LatticeFinder.LatticeFinder.examining_lattice_constant_methods_with_VASP        import get_energies_across_lattice_constants_VASP
from LatticeFinder.LatticeFinder.examining_lattice_constant_methods_with_Manual_Mode import get_energies_across_lattice_constants_in_Manual_Mode

from LatticeFinder.LatticeFinder.plotting_methods import plot_energy_vs_lattice_constants_1D, plot_energy_vs_lattice_constants_2D

class LatticeFinder_Program:
	"""
	This program is designed to give plots and data to help obtain the optimal lattice constants for a 2D and 3D system.
	"""
	def __init__(self, symbol, lattice_type, lattice_constant_parameters, calculator, size=(1,1,1), directions=None, miller=None, limits=None, no_of_cpus=1):
		# input options required for obtaining lattice constants
		self.check_input_information(symbol, lattice_type, lattice_constant_parameters, calculator, size, directions, miller)
		# Information about how to make plots
		self.check_output_information(limits)
		# Other options
		self.no_of_cpus = no_of_cpus
		# Run the program
		self.run()

	def check_input_information(self, symbol, lattice_type, lattice_constant_parameters, calculator, size, directions, miller):
		"""
		This method will take the input data from input_information, set it ready for running in this program, and do some checking of the varables in input_information to make sure that are in a correct format.
		"""
		# General options
		self.symbol = symbol
		self.lattice_type_name = str(lattice_type)
		self.lattice_type = eval(lattice_type)
		self.lattice_constant_parameters = lattice_constant_parameters
		self.calculator = calculator # This could be a string called 'VASP' or 'Manual Mode'
		if isinstance(self.calculator,str):
			self.calculator = self.calculator.lower()
			if self.calculator == 'vasp':
				self.VASP_Input_files = 'VASP_Files'
				self.VASP_Cluster_Folder = 'VASP_Clusters'
			elif self.calculator == 'manual mode':
				self.Manual_Mode_Cluster_Folder = 'Manual_Mode_Clusters'
			else:
				exit('Error, calculator needs to be a ASE calculator, "VASP" or "Manual Mode".')
		self.size = size
		# Other options about constructing the cell
		self.directions = directions
		self.miller = miller
		# The file of where to save lattice constant data to
		self.lattice_data_file = 'lattice_data.txt'

	def check_output_information(self, limits):
		"""
		This method will check the variables for making output data such as plots.
		"""
		# Plotting variables
		if isinstance(limits,dict):
			self.limits = limits
		else:
			self.limits = {'c': limits}
		for key, value in self.limits.items():
			if value == None:
				self.limits[key] = (-float('inf'), float('inf'))

	############################################################################################################################

	def run(self):
		"""
		This method will run the LatticeFinder program commands. 
		"""
		# Perform checks on the lattice_constant_parameters to make sure it is in an acceptable format
		self.lattice_constant_parameters_checks(self.lattice_constant_parameters)
		# Set up the lattice constant generator and types names for future work
		self.lattice_constant_generator = lattice_constant_generator(self.lattice_constant_parameters)
		self.lattice_constant_types = self.lattice_constant_generator.get_lattice_constant_types()
		# Set up lattice_data.txt for writing the energies of lattice constants into. 
		energies_vs_lattice_constants = self.setup_energies_vs_lattice_constants()
		# Process the range of lattice constants and determine the minimum energy and lattice constant, as well as the projected lattice constant
		energies_vs_lattice_constants = self.get_data(energies_vs_lattice_constants)
		self.sort_data_file()
		energies_vs_lattice_constants, energy_vs_volumes = self.divide_up_energies_and_volumes(energies_vs_lattice_constants)
		self.minimum_energy, self.lowest_energy_lattice_constants = self.get_minimum_energy(energies_vs_lattice_constants)
		# Plot the data and give other information about the system
		self.plot_energy_vs_lattice_constants(energies_vs_lattice_constants)
		self.get_other_data_about_system(self.minimum_energy, self.lowest_energy_lattice_constants, energy_vs_volumes)

	############################################################################################################################

	def lattice_constant_parameters_checks(self,lattice_constant_parameters):
		"""
`		This method is designed to check that lattice_constant_parameters in in the correct format before contining
		"""
		
		if isinstance(lattice_constant_parameters,tuple) or isinstance(lattice_constant_parameters,list):
			pass
		elif isinstance(lattice_constant_parameters,dict):
			for lattice_constant_type, lattice_constant_parameter in lattice_constant_parameters.items():
				if isinstance(lattice_constant_parameter,tuple) or isinstance(lattice_constant_parameter,list):
					continue
		else:
			exit('error 3')

	############################################################################################################################

	def setup_energies_vs_lattice_constants(self):
		"""
		This method is designed to load information that has already been gather from previous LatticeFinder runs, or if not setting up the lattice_data_file that lattice constant data will be recorded to.
		"""
		if os.path.exists(self.lattice_data_file):
			energies_vs_lattice_constants = self.load_data()
		else:
			self.setup_initial_data_file()
			energies_vs_lattice_constants = {}
		return energies_vs_lattice_constants

	def load_data(self):
		"""
		Load data from previous LatticeFinder runs
		"""
		energies_vs_lattice_constants = {}
		leading_data = False
		with open(self.lattice_data_file,'r') as lattice_data_FILE:
			for _ in range(12):
				lattice_data_FILE.readline()
			for line in lattice_data_FILE:
				lattice_constants, energy_per_atom = line.rstrip('\n').split(':')
				lattice_constants = eval(lattice_constants)
				if len(self.lattice_constant_types) == 1:
					energy_per_atom, volume = energy_per_atom.rstrip('\n').split('(')
					volume = float(volume.replace(')',''))
				energy_per_atom = float(energy_per_atom)
				if len(self.lattice_constant_types) == 1:
					energies_vs_lattice_constants[lattice_constants] = (energy_per_atom,volume)
				else:
					energies_vs_lattice_constants[lattice_constants] = energy_per_atom
		return energies_vs_lattice_constants

	def setup_initial_data_file(self):
		"""
		Set up the lattice_data_file file that data will be written to.
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
			lattice_data_FILE.write('\n')
			if len(self.lattice_constant_types) == 1:
				lattice_data_FILE.write('Lattice constant ('+str(','.join(self.lattice_constant_types))+')/Ang: Energy/eV (Volume (Ang^3 per atom))\n')
			else:
				lattice_data_FILE.write('Lattice constant ('+str(','.join(self.lattice_constant_types))+'/Ang: Energy/eV\n')
			lattice_data_FILE.write('----------------------------------------------\n')

	############################################################################################################################
	
	def get_data(self, energies_vs_lattice_constants):
		"""

		"""
		if self.calculator == 'vasp':

			get_energies_across_lattice_constants_VASP(self.lattice_type,self.symbol,self.lattice_constant_generator,self.lattice_constant_types,self.size,self.directions,self.miller,self.VASP_Input_files,self.Manual_Mode_Cluster_Folder)
		elif self.calculator == 'manual mode':

			get_energies_across_lattice_constants_in_Manual_Mode(self.lattice_type,self.symbol,self.lattice_constant_generator,self.lattice_constant_types,self.size,self.directions,self.miller,self.Manual_Mode_Cluster_Folder)
		else:
			energies_vs_lattice_constants = get_energies_across_lattice_constants_ASE(self.lattice_type,self.symbol,self.lattice_constant_generator,self.lattice_constant_types,self.size,self.directions,self.miller,self.calculator,self.no_of_cpus,self.lattice_data_file,energies_vs_lattice_constants)
		return energies_vs_lattice_constants

	def sort_data_file(self):
		"""
		If you are using multiple processes, the ordering or lattice constants in the lattice_data.txt can become muddled up
		# This method reorders lines
		"""
		new_suffix = '.new'
		with open(self.lattice_data_file+new_suffix,'w') as lattice_data_FILE_NEW:
			lines = []
			with open(self.lattice_data_file,'r') as lattice_data_FILE_OLD:
				for _ in range(12):
					lattice_data_FILE_NEW.write(lattice_data_FILE_OLD.readline())
				for line in lattice_data_FILE_OLD:
					lattice_constants = eval(line.rstrip().split(':')[0])
					lines.append((lattice_constants,line))
			lines.sort()
			for lattice_constants, line in lines:
				lattice_data_FILE_NEW.write(line)
		os.remove(self.lattice_data_file)
		os.rename(self.lattice_data_file+new_suffix,self.lattice_data_file)

	def divide_up_energies_and_volumes(self, energies_vs_lattice_constants):

		if len(self.lattice_constant_types) == 1:
			new_energies_vs_lattice_constants = {}
			energy_vs_volumes = [[], []]
			energies_vs_lattice_constants = sorted(energies_vs_lattice_constants.items())
			total_no_of_enteries = len(energies_vs_lattice_constants)
			for _ in range(total_no_of_enteries):
				lattice_constant, (energy, volume) = energies_vs_lattice_constants.pop(0)
				new_energies_vs_lattice_constants[lattice_constant] = energy
				energy_vs_volumes[0].append(volume)
				energy_vs_volumes[1].append(energy)
			energies_vs_lattice_constants = new_energies_vs_lattice_constants
		else:
			energy_vs_volumes = None
		return energies_vs_lattice_constants, energy_vs_volumes


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
			plot_energy_vs_lattice_constants_1D(energies_vs_lattice_constants, self.limits, self.minimum_energy, self.lowest_energy_lattice_constants)
		if len(self.lattice_constant_types) == 2:
			plot_energy_vs_lattice_constants_2D(energies_vs_lattice_constants, self.limits, self.minimum_energy, self.lowest_energy_lattice_constants)

	def get_other_data_about_system(self,minimum_energy,lowest_energy_lattice_constants,energy_vs_volumes=None):
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

		if len(self.lattice_constant_types) == 1:
			from ase.units import kJ
			from ase.eos import EquationOfState
			volumes = energy_vs_volumes[0]
			energies = energy_vs_volumes[1]
			eos = EquationOfState(volumes, energies, eos='sj')
			v0, e0, BB = eos.fit()
			bulk_modulus = (BB / kJ) * 1.0e24
			name_eos = 'Equation_of_State_Plot'
			# Save figure
			eos.plot()
			plt.savefig(name_eos+'.png')
			plt.savefig(name_eos+'.eps')
			plt.savefig(name_eos+'.svg')
			plt.cla(); plt.clf()

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
			if len(self.lattice_constant_types) == 1:
				results_fileTXT.write('\n')
				results_fileTXT.write('Bulk Modulus: '+str(bulk_modulus)+' GPa\n')

	############################################################################################################################