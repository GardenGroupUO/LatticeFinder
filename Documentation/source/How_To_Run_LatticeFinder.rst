
.. _How_To_Run_LatticeFinder:

*Run_LatticeFinder.py* - How to run LatticeFinder
#################################################

In this article, we will look at how to run LatticeFinder. LatticeFinder is run through the ``Run_LatticeFinder.py`` python script. You can find examples of ``Run_LatticeFinder.py`` files at `github.com/GardenGroupUO/LatticeFinder <https://github.com/GardenGroupUO/LatticeFinder>`_ under ``Examples``. Also, you can try out this program by running an example script through a Jupyter notebook. See :ref:`Examples of running LatticeFinder <Examples_of_Running_LatticeFinder>` to get access to examples of running LatticeFinder through this Jupyter notebook!

Running the ``Run_LatticeFinder.py`` script
*******************************************

We will explain how the ``Run_LatticeFinder.py`` code works by running though the example shown below:

.. literalinclude:: Run_LatticeFinder.py
	:language: python
	:caption: Run_LatticeFinder.py
	:name: Run_LatticeFinder.py
	:tab-width: 4
	:linenos:

Lets go through each part of the ``Run_LatticeFinder.py`` file one by one to understand how to use it. 

Input information for LatticeFinder
===================================

The following information is required by LatticeFinder:

* **symbol** (*str.*): This is the element that makes up your 2D/3D system.
* **lattice_type** (*str.*): This is the type of lattice that you which to obtain the optimal lattice constants for. See `Available crystal lattices in ASE <https://wiki.fysik.dtu.dk/ase/ase/lattice.html#available-crystal-lattices>`_ for more information. 
* **lattice_constant_parameters** (*list of floats*): These are the values of the lattice constant(s) that you would like to examine. There are two ways that this can be entered into LatticeFinder:

	* If you are locating the optimal lattice constant for a system that only contains one lattice constant, this can be entered in as a ``np.arange``. For example, if you want to scan between a lattice constant of 3.0 Å to 5.0 Å in 0.1 Å segments, ``lattice_constant_parameters = np.arange(3.0,5.01,0.1)``. You can also have an irregular list. For example, if you want to look further between 3.8 Å and 4.5 Å in 0.01 segments, you can set ``lattice_constant_parameters = list(np.arange(3.0,3.8,0.1))+list(np.arange(3.8,4.5,0.01))+list(np.arange(4.5,5.01,0.1))``
	* If you are locating the optimal lattice constanta for a system that only contains two lattice constants, this must be entered as a list, where each key is the name of the lattice constant. For example, for a hexagonal closed packed crystal, you can set ``lattice_constant_parameters = {'a': np.arange(2.0,5.01,0.1), 'c': np.arange(3.0,6.01,0.1)}``. The lists for each lattice constant must be regularly spaced; you can not use irregular spacing in LatticeFinder for system with more than one lattice constant. 

* **calculator** (*ase.calculator/str.*): The calculator is used to calculate the energy of the 2D/3D system at various lattice constants. See `Calculators in ASE <https://wiki.fysik.dtu.dk/ase/ase/calculators/calculators.html>`_ for information about how calculators works in ASE.

	* You can also use **VASP to perform DFT local optimisations** on your clusters. Do this by setting ``calculator = 'VASP'``. See :ref:`How_To_VASP_In_LatticeFinder` to learn more about how to perform VASP calculations on clusters created using NISP. 
	* You can also elect to **manually enter in the energies of the clusters**. To do this, enter in  ``calculator = 'Manual Mode'``. See :ref:`How_To_Manually_Enter_Energy_Results_Into_LatticeFinder` for more information about how to manually enter in energies for clusters into LatticeFinder. 

* **size** (*list of ints*): This is the size of the system within a cell. See `Usage in Lattices <https://wiki.fysik.dtu.dk/ase/ase/lattice.html#usage>`_ for more infotmation about the size parameter. 
* **directions** (*list of ints*): Still figuring this out. See `Usage in Lattices <https://wiki.fysik.dtu.dk/ase/ase/lattice.html#usage>`_ for more infotmation about the directions parameter. 
* **miller** (*list of ints*): Still figuring this out. See `Usage in Lattices <https://wiki.fysik.dtu.dk/ase/ase/lattice.html#usage>`_ for more infotmation about the miller parameter.

Parameters required by LatticeFinder for plotting plots:

* **limit** (*dict.*): This is the limits for plotting your lattice constant plots. For a lattice system with one lattice constant: give as ``{'c': (c_lower_limit, c_upper_limit)}``. For a lattice system with two lattice constant: give as ``{'c': (c_lower_limit, c_upper_limit), 'a': (a_lower_limit, a_upper_limit)}``. If no change to the plotting limits are needed, set this to ``None``. Default: ``None``. 
* **make_svg_eps_files** (*bool*): This tag tells LatticeFinder if you want to create svg and eps files of the plots made. Default: ``True``. 

Other parameters required by LatticeFinder:

* **no_of_cpus** (*int*): This is the number of cpus that you would like to use to perform calculations of 2D/3D system of various lattice constants. 

An example of these parameters in ``Run_LatticeFinder.py`` is given below:

.. literalinclude:: Run_LatticeFinder.py
	:language: python
	:tab-width: 4
	:linenos:
	:lineno-start: 1
	:lines: 1-24


Run LatticeFinder!
==================

You have got to the end of all the parameter setting stuff. Now on to running NISP. The next part of the ``Run_LatticeFinder.py`` script tells NISP to run. This is written as follows in the ``Run_LatticeFinder.py``:

.. literalinclude:: Run_LatticeFinder.py
	:language: python
	:tab-width: 4
	:linenos:
	:lineno-start: 26
	:lines: 26

Output files that are created by LatticeFinder
**********************************************

The LatticeFinder program will create a number of plots and text documents when it is run. See :ref:`Examples of Running LatticeFinder with Run_LatticeFinder.py <Examples_of_Running_LatticeFinder>` and `LatticeFinder examples here <https://github.com/GardenGroupUO/LatticeFinder/tree/main/Examples>`_ to see the types of plots and text documents that LatticeFinder will make. 
