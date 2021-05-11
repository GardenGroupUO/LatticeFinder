from LatticeFinder import LatticeFinder_Program
import numpy as np

symbol = 'Au'
lattice_type = 'FaceCenteredCubic'

lattice_constant_parameters = (2.0,6.0,0.1)

calculator = 'VASP'
slurm_information = {}
slurm_information['project'] = 'uoo02568'
slurm_information['time'] = '40:00:00'
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
no_of_cpus=1

LatticeFinder_Program(symbol, lattice_type, lattice_constant_parameters, calculator, size=size, directions=directions, miller=miller, no_of_cpus=no_of_cpus, slurm_information=slurm_information)