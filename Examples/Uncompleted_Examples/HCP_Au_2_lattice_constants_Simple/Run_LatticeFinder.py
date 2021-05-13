from LatticeFinder import LatticeFinder_Program
import numpy as np

symbol = 'Au'
lattice_type = 'HexagonalClosedPacked'

lattice_constant_parameters = {'a': (2.0,5.0,0.1), 'c': (3.0,6.0,0.1)}

from asap3.Internal.BuiltinPotentials import Gupta
# Parameter sequence: [p, q, a, xi, r0]
r0 = 4.07/(2.0 ** 0.5)
Au_parameters = {'Au': [10.53, 4.30, 0.2197, 1.855, r0]} # Baletto
cutoff = 8
calculator = Gupta(Au_parameters, cutoff=cutoff, debug=False)

size_single = 28
size=(size_single,size_single,size_single)

directions=[]
miller=[]

limits = {'a': (2.6,3.2), 'c': (4.4,5.0)}
no_of_cpus = 8


LatticeFinder_Program(symbol, lattice_type, lattice_constant_parameters, calculator, size=size, directions=directions, miller=miller, limits=limits, no_of_cpus=no_of_cpus)