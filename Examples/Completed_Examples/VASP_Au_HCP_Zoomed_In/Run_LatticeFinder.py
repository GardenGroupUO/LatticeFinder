from LatticeFinder import LatticeFinder_Program
import numpy as np

symbol = 'Au'
lattice_type = 'HexagonalClosedPacked'

#lattice_constant_parameters = {'a': (2.0,5.0,0.1), 'c': (3.0,6.0,0.1)}
#aa_list = np.arange(2.0,5.01,0.1)
aa_list = np.arange(2.8,3.001,0.001)
#cc_list = np.arange(3.0,6.01,0.1)
cc_list = np.arange(4.7,5.101,0.001)
lattice_constant_parameters = {'a': aa_list, 'c': cc_list}

calculator = 'VASP'
slurm_information = {}
slurm_information['project'] = 'uoo02568'
slurm_information['time'] = '0:10:00'
slurm_information['nodes'] = 1
slurm_information['ntasks_per_node'] = 2
slurm_information['mem-per-cpu'] = '3G'
slurm_information['partition'] = 'large'
slurm_information['email'] = 'geoffreywealslurmnotifications@gmail.com'
slurm_information['python_version'] = 'Python/3.6.3-gimkl-2017a'
slurm_information['vasp_version'] = 'VASP/5.4.4-intel-2017a'
slurm_information['vasp_execution'] = 'vasp_std'

slurm_information['Make individual or packet submitSL files'] = 'packets'
slurm_information['Number of VASP calculations to run per packet'] = 25

size=(1,1,1)

directions=[]
miller=[]

limits = {'a': (2.5, 3.5), 'c': (4.0, 5.5)}
make_svg_eps_files = False

no_of_cpus=1

LatticeFinder_Program(symbol, lattice_type, lattice_constant_parameters, calculator, size=size, directions=directions, miller=miller, no_of_cpus=no_of_cpus, limits=limits, make_svg_eps_files=make_svg_eps_files, slurm_information=slurm_information)
