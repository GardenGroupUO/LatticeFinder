
.. _How_To_VASP_In_LatticeFinder:

How to perform LatticeFinder with VASP calculations
===================================================

In this article, we will look at how to run LatticeFinder where VASP is used to calculate the energies of systems at various lattice constants. The ``Run_LatticeFinder.py`` python script that is used is the same as shown previously in :ref:`How_To_Run_LatticeFinder`, but with an extra component. An example of a ``Run_LatticeFinder.py`` python script that uses VASP is shown below:

.. literalinclude:: Run_LatticeFinder_VASP.py
	:language: python
	:caption: Run_LatticeFinder.py
	:tab-width: 4
	:linenos:

The ``slurm_information`` parameter
-----------------------------------

The extra parameter that is included when performing VASP calculations is the ``slurm_information`` parameter, which is a dictionary that holds all the information that is needed to create the ``submit.sl`` files required to submit VASP calculations to slurm. The following information is needed in the ``'slurm_information'`` dictionary:

* **project** (*str.*): This is the name of the project that you want to submit this job to.
* **time** (*str.*): This is the amount of time you want to give to your slurm jobs, given as ``'HH:MM:SS'``, where ``'HH:MM:SS'`` is the hours, minutes, and seconds you want to give to a job. 
* **nodes** (*str.*): This is the number of nodes that you would like to give to a job.
* **ntasks_per_node** (*str./int*): This is the number of cpus that you give to a job. 
* **mem-per-cpu** (*str.*): This is the amount of momeory you are giving to your job per cpu

The following can also be included in ``'slurm_information'`` dictionary, but these are default value for these if you do not give a value for them.

* **partition** (*str.*): This is the partition that is given to your job. See `Mahuika Slurm Partitions <https://support.nesi.org.nz/hc/en-gb/articles/360000204076-Mahuika-Slurm-Partitions>`_ for more information about partition on NeSI (Default: ``'large'``).
* **email** (*str.*): This is the email address you would like notifications about your slurm job to be sent to (Default: ``''``).
* **vasp_version** (*str.*): This is the version of VASP that you would like to load in on slurm (Default: ``'VASP/5.4.4-intel-2017a'``).
* **vasp_execution** (*str.*): This is the name of the vasp program that you execute (Default: ``'vasp_std'``).

Commonly in VASP you will only need to use a (1,1,1) cell since VASP performs calculations with periodic boundary conditions. Because of this, you will be performing many small VASP calculations. As you may be performing many short VASP calculations, it is possible to break the slurm management system as slurm can get confused when its accepts many jobs at once which then finish very quickly. NeSI (support.nesi.org.nz) suggest that you should instead run packets of short VASP calculation in serial to minimise this happening. In this case, there are two additional setting to give the ``slurm_information`` dictionary:

* **Make individual or packet submitSL files** (*str.*): Determines how jobs are submitted to slurm. If ``'individual'``: a slurm.sl file is created for each VASP job to run; if ``'packet'``: Several individual VASP jobs will be packaged together and run one after the other (serial) in slurm (Default: ``'individual'``).
* **Number of VASP calculations to run per packet** (*int*): If you choose ``slurm_information['Make individual or packet submitSL files'] = 'packets'``, this is the number of individual VASP jobs that will be packaged together and run one after the other (serial) in slurm.

See an example of the ``slurm_information`` parameter below:

.. literalinclude:: Run_LatticeFinder_VASP.py
	:caption: Run_LatticeFinder.py
	:language: python
	:tab-width: 4
	:linenos:
	:lineno-start: 10
	:lines: 10-23

Make sure that you include ``'slurm_information'`` in the final line of ``Run_LatticeFinder.py`` in ``LatticeFinder_Program``. See the following code before to see this: 

.. literalinclude:: Run_LatticeFinder_VASP.py
	:caption: Run_LatticeFinder.py
	:language: python
	:tab-width: 4
	:linenos:
	:lineno-start: 31
	:lines: 31

Other files that you will need
------------------------------

You will also need to give LatticeFinder some other files that are needed by VASP to perform calculations. In the same place where you place your ``Run_LatticeFinder.py`` file, you want to create another folder called ``VASP_Files``. In this ``VASP_Files`` folder you want to include the following files:

* ``POTCAR``: This is the file that contains the information required to locally optimise a nanocluster with DFT using a certain functional.
* ``KPOINTS``: This contain the information used to specify the Bloch vectors (k-points) that will be used to sample the Brillouin zone in your calculation.
* ``INCAR``: This contains all the setting that are required by VASP to perform calculations. **Note that in the INCAR you must set** ``NSW = 0``. This prevents VASP from performing a local optimisation which you do not need to do in this program.

These files will be copied by LatticeFinder into each nanocluster folder. See `an example of a setup of LatticeFinder for VASP here <https://github.com/GardenGroupUO/LatticeFinder/tree/main/Examples/VASP>`_. 


What to do after you have run LatticeFinder
-------------------------------------------

After you run LatticeFinder, this will create a new folder called ``VASP_Systems``, which contains subfolders of your system at all the lattice constants that you want to examine. Each subfolder will contain a ``POSCAR``, ``INCAR``, ``POTCAR``, ``KPOINTS``, and ``submit.sl`` that are needed by VASP to perform DFT calculations. Each system is ready to be calculated by VASP. 

You will find that there are many systems are created by LatticeFinder. To submit all of these system to slurm to calculate energies for by VASP, you can execute the program called ``Run_LatticeFinder_submitSL_slurm.py`` which will execute all of DFT VASP jobs in slurm. To run this script, type ``Run_submitSL_slurm.py`` into the terminal inside of your newly created ``VASP_Systems`` folder. 