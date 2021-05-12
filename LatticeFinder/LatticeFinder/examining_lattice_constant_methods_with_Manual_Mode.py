import os
from ase.io import write

def get_energies_across_lattice_constants_in_Manual_Mode(lattice_type,symbol,lattice_constant_generator,size,directions=None,miller=None,folder_name='Manual_Mode_Clusters'):
	"""

	"""
	for latticeconstants in lattice_constant_generator:
		bulk_system = lattice_type(symbol=symbol, latticeconstant=latticeconstants, size=size) #, directions=directions, miller=miller)
		print(bulk_system)

def save_cluster_to_folder(folder,name,filename_suffix,manual_mode,cluster):
	path_to_folder = folder+'/'+name
	if not os.path.exists(path_to_folder):
		os.mkdir(path_to_folder)
	if manual_mode == 'vasp':
		write(path_to_folder+'/'+'POSCAR',cluster,format='vasp')
	else:
		write(path_to_folder+'/'+name+'.'+filename_suffix,cluster,format='xyz')

def get_system_from_Manual_Mode(latticeconstants,Manual_Mode_Cluster_Folder):
	pass