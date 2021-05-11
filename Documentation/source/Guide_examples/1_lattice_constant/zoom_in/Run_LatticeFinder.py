from LatticeFinder import LatticeFinder_Program
import numpy as np

symbol = 'Au'
lattice_type = 'FaceCenteredCubic'

lattice_constant_parameters = list(np.arange(3.0,4.0,0.1))+list(np.arange(4.0,4.2,0.001))+list(np.arange(4.2,5.01,0.1))

from asap3.Internal.BuiltinPotentials import Gupta
# Parameter sequence: [p, q, a, xi, r0]
r0 = 4.07/(2.0 ** 0.5)
Au_parameters = {'Au': [10.53, 4.30, 0.2197, 1.855, r0]} # Baletto
cutoff = 8
calculator = Gupta(Au_parameters, cutoff=cutoff, debug=False)

size=(16,16,16)

directions=[]
miller=[]
no_of_cpus=1

LatticeFinder_Program(symbol, lattice_type, lattice_constant_parameters, calculator, size=size, directions=directions, miller=miller, no_of_cpus=no_of_cpus)