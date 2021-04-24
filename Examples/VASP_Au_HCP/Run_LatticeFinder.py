from LatticeFinder import LatticeFinder_Program
import numpy as np

symbol = 'Au'
lattice_type = 'HexagonalClosedPacked'

#lattice_constant_parameters = {'a': (2.0,5.0,0.1), 'c': (3.0,6.0,0.1)}
aa_list = list(np.arange(2.0,2.6,0.1))+list(np.arange(2.6,3.2,0.01))+list(np.arange(3.2,5.01,0.1))
cc_list = list(np.arange(3.0,4.4,0.1))+list(np.arange(4.4,5.0,0.01))+list(np.arange(5.0,6.01,0.1))
lattice_constant_parameters = {'a': aa_list, 'c': cc_list}

calculator = 'VASP'
size=(16,16,16)

directions=[]
miller=[]
no_of_cpus=1

LatticeFinder_Program(symbol, lattice_type, lattice_constant_parameters, calculator, size=size, directions=directions, miller=miller, no_of_cpus=no_of_cpus)