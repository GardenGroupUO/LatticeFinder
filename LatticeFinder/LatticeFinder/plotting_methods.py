import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

def get_plotting_lims(lattice_point,percent_diff):
		lattice_point_diff = max(lattice_point) - min(lattice_point)
		lattice_point_diff_with_percent  = lattice_point_diff*(percent_diff/100.0)
		lattice_point_low  = min(lattice_point) - lattice_point_diff_with_percent
		lattice_point_high = max(lattice_point) + lattice_point_diff_with_percent
		return lattice_point_low, lattice_point_high

def plot_energy_vs_lattice_constants_1D(lattice_energies_dict, limits, minimum_energy, lowest_energy_lattice_constants):
	lattice_point_c = []; lattice_energies = [];
	lattice_point_c_bottom, lattice_point_c_top = limits['c']
	for cc_LC, energy_per_atom in sorted(list(lattice_energies_dict.items())):
		if (lattice_point_c_bottom <= cc_LC <= lattice_point_c_top):
			lattice_point_c.append(cc_LC)
			lattice_energies.append(energy_per_atom)
	plt.scatter(lattice_point_c, lattice_energies, s=5, alpha=0.5,zorder=10)
	for cc_point in lowest_energy_lattice_constants:
		label = 'c = '+str(cc_point)+' Ang' #for aa_point, cc_point in lowest_energy_lattice_constants
		plt.scatter(lowest_energy_lattice_constants, minimum_energy, color='r', s=5, alpha=0.5,zorder=20, label=label)
	plt.xlabel('Lattice Constant ('+r'$\AA$'+')')
	plt.ylabel('Energy per Atom ('+r'$eV/Atom$'+')')
	percent_diff = 2.0
	lattice_point_low, lattice_point_high = get_plotting_lims(lattice_point_c,percent_diff)
	lattice_energies_low, lattice_energies_high = get_plotting_lims(lattice_energies,percent_diff)
	#x_diff = lattice_energies_high - lattice_energies_low
	#plt.hlines(minimum_energy,lattice_energies_low - x_diff,lattice_energies_high + x_diff,color='k',linestyles='dashed',zorder=1)
	plt.xlim((lattice_point_low,lattice_point_high))
	plt.ylim((lattice_energies_low,lattice_energies_high))
	leg = plt.legend(title='Cohensive Energy: '+str(round(minimum_energy,5))+' '+r'$ev/Atom$')
	plt.savefig('Energy_Vs_Lattice_Constant.png')
	plt.savefig('Energy_Vs_Lattice_Constant.svg')
	plt.savefig('Energy_Vs_Lattice_Constant.eps')
	plt.cla(); plt.clf()

def plot_energy_vs_lattice_constants_2D(lattice_energies_dict, limits, minimum_energy, lowest_energy_lattice_constants):
	lattice_point_a = []; lattice_point_c = []; lattice_energies = [];
	lattice_point_a_bottom, lattice_point_a_top = limits['a']
	lattice_point_c_bottom, lattice_point_c_top = limits['c']
	for (aa_LC, cc_LC), energy_per_atom in sorted(list(lattice_energies_dict.items())):
		if (lattice_point_a_bottom <= aa_LC <= lattice_point_a_top) and (lattice_point_c_bottom <= cc_LC <= lattice_point_c_top):
			lattice_point_a.append(aa_LC)
			lattice_point_c.append(cc_LC)
			lattice_energies.append(energy_per_atom)
	lattice_point_a  = np.array(lattice_point_a)
	lattice_point_c  = np.array(lattice_point_c)
	lattice_energies =  np.array(lattice_energies)

	zero_zero_value = lattice_point_a[0]
	for row_length in range(len(lattice_point_a)):
		if not lattice_point_a[row_length] == zero_zero_value:
			break
	column_length = int(float(len(lattice_point_a))/float(row_length))

	lattice_point_a_matrix = lattice_point_a.reshape(column_length,row_length)
	lattice_point_c_matrix = lattice_point_c.reshape(column_length,row_length)

	def Z_function(AA,CC):
		row_total_index, column_total_index = AA.shape
		data = np.zeros(shape=(row_total_index, column_total_index))#,fill_value=None)
		for row_index in range(row_total_index):
			for column_index in range(column_total_index):
				aa_LC = AA[row_index][column_index]
				cc_LC = CC[row_index][column_index]
				data[row_index][column_index] = lattice_energies_dict[(aa_LC,cc_LC)]
		#data = np.real(data)
		return data
	lattice_energies_matrix = Z_function(lattice_point_a_matrix, lattice_point_c_matrix)

	from mpl_toolkits import mplot3d
	fig = plt.figure()
	ax = plt.axes(projection='3d')

	levels_conf = np.linspace(min(lattice_energies), max(lattice_energies), 20)
	levels_confull = np.linspace(min(lattice_energies), max(lattice_energies), 1000)

	# https://jakevdp.github.io/PythonDataScienceHandbook/04.12-three-dimensional-plotting.html
	ax.plot_surface(lattice_point_a_matrix, lattice_point_c_matrix, lattice_energies_matrix, rstride=1, cstride=1,cmap='viridis', edgecolor='none', alpha=0.2, zorder=10)
	ax.contour3D(lattice_point_a_matrix, lattice_point_c_matrix, lattice_energies_matrix, levels=levels_conf, cmap='viridis', zorder=11)
	ax.set_xlabel('Lattice Constant (a) ('+r'$\AA$'+')')
	ax.set_ylabel('Lattice Constant (c) ('+r'$\AA$'+')')
	ax.set_zlabel('Cohensive Energy ('+r'$eV/Atom$'+')')
	percent_diff = 2.0
	lattice_point_a_low, lattice_point_a_high = get_plotting_lims(lattice_point_a,0)
	lattice_point_c_low, lattice_point_c_high = get_plotting_lims(lattice_point_c,0)
	_, lattice_energies_high = get_plotting_lims(lattice_energies,0)
	lattice_energies_low, _  = get_plotting_lims(lattice_energies,50)
	ax.set_xlim((lattice_point_a_low,lattice_point_a_high))
	ax.set_ylim((lattice_point_c_low,lattice_point_c_high))
	ax.set_zlim((lattice_energies_low,lattice_energies_high))
	# https://stackoverflow.com/questions/35445424/surface-and-3d-contour-in-matplotlib
	ax.contour(lattice_point_a_matrix, lattice_point_c_matrix, lattice_energies_matrix, levels=levels_conf, cmap='viridis', linestyles="solid",offset=lattice_energies_low,zorder=-11)
	plt.contourf(lattice_point_a_matrix, lattice_point_c_matrix, lattice_energies_matrix, levels=levels_confull, cmap='viridis', alpha=0.2, antialiased=True, linestyles=None,offset=lattice_energies_low,zorder=-10)
	
	lowest_lattice_points_a = []
	lowest_lattice_points_c = []
	for aa_point, cc_point in lowest_energy_lattice_constants:
		lowest_lattice_points_a.append(aa_point)
		lowest_lattice_points_c.append(cc_point)
		label = '(a = '+str(aa_point)+' Ang, c = '+str(cc_point)+' Ang)' #for aa_point, cc_point in lowest_energy_lattice_constants
		ax.scatter(lowest_lattice_points_a,lowest_lattice_points_c,[lattice_energies_low]*len(lowest_lattice_points_a),color='red',zorder=40, label=label)
		#ax.contour(lattice_point_a_matrix, lattice_point_c_matrix, lattice_energies_matrix, 10, lw=3, colors="k", linestyles="solid")
	leg = ax.legend(title='Cohensive Energy: '+str(round(minimum_energy,5))+' eV/Atom', facecolor='white', framealpha=0.8)#,handlelength=0, handletextpad=0, markerscale=0)
	#leg.set_facecolor('white')
	
	ax.scatter(lowest_lattice_points_a,lowest_lattice_points_c,[minimum_energy]*len(lowest_lattice_points_a),color='red',zorder=-9)

	cbar = plt.colorbar(pad=0.12)
	cbar.set_label('Cohensive Energy ('+r'$ev/Atom$'+')', rotation=270, labelpad=20)

	plt.tight_layout()
	plt.savefig('Energy_Vs_Lattice_Constant.png')
	plt.savefig('Energy_Vs_Lattice_Constant.svg')
	plt.savefig('Energy_Vs_Lattice_Constant.eps')
	plt.cla(); plt.clf()
	#plt.show()

	#https://jakevdp.github.io/PythonDataScienceHandbook/04.04-density-and-contour-plots.html
	fig, ax = plt.subplots()
	#ax.view_init(azim=0, elev=90)
	
	contours = plt.contour(lattice_point_a_matrix, lattice_point_c_matrix, lattice_energies_matrix, levels=levels_conf, cmap='viridis', zorder=10)
	plt.clabel(contours, inline=True, fontsize=10)

	levels_confull = np.linspace(min(lattice_energies), max(lattice_energies), 1000)
	plt.contourf(lattice_point_a_matrix, lattice_point_c_matrix, lattice_energies_matrix, levels=levels_confull, cmap='viridis', alpha=0.2, antialiased=True, linestyles=None, zorder=20)
	#plt.imshow(lattice_energies_matrix, extent=[lattice_point_a_low, lattice_point_a_high, lattice_point_c_low, lattice_point_c_high], origin='lower',cmap='viridis', alpha=0.2) # , interpolation='bilinear'
	
	#import pdb; pdb.set_trace()
	for aa_point, cc_point in lowest_energy_lattice_constants:
		label = '(a = '+str(aa_point)+', c = '+str(cc_point)+')' #for aa_point, cc_point in lowest_energy_lattice_constants
		plt.plot(lowest_lattice_points_a, lowest_lattice_points_c, 'ro', label=label, zorder=30)
	leg = ax.legend(title='Cohensive Energy: '+str(round(minimum_energy,5))+' '+r'$ev/Atom$', facecolor='white', framealpha=0.8) #,handlelength=0, handletextpad=0, markerscale=0)
	#leg.set_facecolor('white')
	#for item in leg.legendHandles:
	#	item.set_visible(False)

	cbar = plt.colorbar()
	cbar.set_label('Cohensive Energy ('+r'$ev/Atom$'+')', rotation=270, labelpad=20)
	#lattice_point_a_low, lattice_point_a_high = get_plotting_lims(lattice_point_a,0)
	#lattice_point_c_low, lattice_point_c_high = get_plotting_lims(lattice_point_c,0)
	#lattice_energies_low, lattice_energies_high = get_plotting_lims(lattice_energies,0)
	#import pdb; pdb.set_trace()

	plt.xlim((lattice_point_a_low,lattice_point_a_high))
	plt.ylim((lattice_point_c_low,lattice_point_c_high))
	plt.xlabel('Lattice Constant (a) ('+r'$\AA$'+')')
	plt.ylabel('Lattice Constant (c) ('+r'$\AA$'+')')

	plt.tight_layout()
	#plt.zlim((lattice_energies_low,lattice_energies_high))
	plt.savefig('Energy_Vs_Lattice_Constant_Contour.png')
	plt.savefig('Energy_Vs_Lattice_Constant_Contour.svg')
	plt.savefig('Energy_Vs_Lattice_Constant_Contour.eps')
	plt.cla(); plt.clf()