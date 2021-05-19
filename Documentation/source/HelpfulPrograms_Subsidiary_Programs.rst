
.. _HelpfulPrograms_Subsidiary_Programs:

Helpful Programs to run LatticeFinder
#####################################

LatticeFinder contains subsidary programs that you may find useful, especially for using LatticeFinder with VASP. In this article, we will introduce all of the programs that can be used with LatticeFinder. These programs can be run by typing the program you want to run into the terminal from whatever directory you are in. 

The scripts and programs that we will be mentioned here are:

.. contents::
    :depth: 1
    :local:

.. _What_to_make_sure_is_done_before_running_any_of_these_scripts:

What to make sure is done before running any of these scripts. 
**************************************************************

If you installed LatticeFinder through pip3
-------------------------------------------

If you installed the LatticeFinder program with ``pip3``, these scripts will be installed in your bin. You do not need to add anything into your ``~/.bashrc``. You are all good to go. 

If you performed a Manual installation
--------------------------------------

If you have manually added this program to your computer (such as cloning this program from Github), you will need to make sure that you have included the ``Subsidiary_Programs`` folder into your ``PATH`` in your ``~/.bashrc`` file. All of these program can be found in the ``Subsidiary_Programs`` folder. To execute these programs from the ``Subsidiary_Programs`` folder, you must include the following in your ``~/.bashrc``:

.. code-block:: bash

	export PATH_TO_LatticeFinder="<Path_to_LatticeFinder>" 

where ``<Path_to_LatticeFinder>"`` is the path to get to the genetic algorithm program. Also include somewhere before this in your ``~/.bashrc``:

.. code-block:: bash

	export PATH="$PATH_TO_LatticeFinder"/LatticeFinder/Subsidiary_Programs:$PATH

See more about this in :ref:`Installation of LatticeFinder <Installation>`. 


``Run_LatticeFinder_submitSL_slurm.py`` - How to execute all VASP jobs individually as single jobs on slurm for lattice constant calculations
*********************************************************************************************************************************************



``Run_overall_LatticeFinder_submitSL_slurm.py`` - How to execute all your VASP jobs that have been collected together as packets for submission to slurm
********************************************************************************************************************************************************



``LatticeFinder_Tidy_Finished_Jobs.py`` - How to ...
******************************************************************************************************************

