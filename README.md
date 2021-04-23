# The LatticeFinder Program

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/LatticeFinder)](https://docs.python.org/3/)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/GardenGroupUO/LatticeFinder)](https://github.com/GardenGroupUO/LatticeFinder)
[![PyPI](https://img.shields.io/pypi/v/LatticeFinder)](https://pypi.org/project/LatticeFinder/)
[![Conda](https://img.shields.io/conda/v/gardengroupuo/latticefinder)](https://anaconda.org/GardenGroupUO/latticefinder)
[![Documentation](https://img.shields.io/badge/Docs-click%20here-brightgreen)](https://latticefinder.readthedocs.io/en/latest/)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/GardenGroupUO/Organisms_Jupyter_Examples/main?urlpath=lab)
[![Licence](https://img.shields.io/github/license/GardenGroupUO/LatticeFinder)](https://www.gnu.org/licenses/agpl-3.0.en.html)
[![LGTM Grade](https://img.shields.io/lgtm/grade/python/github/GardenGroupUO/LatticeFinder)](https://lgtm.com/projects/g/GardenGroupUO/LatticeFinder/context:python)

Authors: Geoffrey R. Weal and Dr. Anna L. Garden (University of Otago, Dunedin, New Zealand)

Group page: https://blogs.otago.ac.nz/annagarden/

## What is LatticeFinder

LatticeFinder is designed to give you the optimum lattice constants for a 3D system. 

## Try LatticeFinder before you Clone/Pip/Conda (on Binder/Jupter Notebooks)!

If you are new to the LatticeFinder program, it is recommended try it out by running LatticeFinder live on our interactive Jupyter+Binder page before you download it. On Jupyter+Binder, you can play around with the LatticeFinder program on the web. You do not need to install anything to try LatticeFinder out on Jupyter+Binder. 

**Click the Binder button below to try LatticeFinder out on the web! (The Binder page may load quickly or may take 1 or 2 minutes to load)**

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/GardenGroupUO/Organisms_Jupyter_Examples/main?urlpath=lab)

Have fun!

## Installation

It is recommended to read the installation page before using the LatticeFinder program. 

[latticefinder.readthedocs.io/en/latest/Installation.html](https://latticefinder.readthedocs.io/en/latest/Installation.html)

Note that you can install LatticeFinder through ``pip3`` and ``conda``. 

## Output files that are created by LatticeFinder

The LatticeFinder program is designed to give the information that you can use to determine the optimise value of the lattice constant for your system. For example, for a Au face centred cubic (FCC) lattice you can first perform an broad overlook of the energy per atom for various lattice constants.

<p align="center">
	<img src="https://github.com/GardenGroupUO/LatticeFinder/blob/main/Documentation/source/Results/FCC_Focused/Energy_Vs_Lattice_Constant.png">
</p>

You can then add more lattice constant measurements around the point where you believe the lowest energy form of the Au FCC lattice resides

<p align="center">
	<img src="https://github.com/GardenGroupUO/LatticeFinder/blob/main/Documentation/source/Results/FCC_Focused/Energy_Vs_Lattice_Constant.png">
</p>

The data of the energies of all FCC lattices for various lattice constants are also given, as well as other final details about the optimum system, such as the stress tensor and bulk modulus.

```bash

Symbol: Au
Lattice_type: FaceCenteredCubic
calculator: <asap.RGL object at 0x0x2fcab40>
size: (16, 16, 16)
directions: []
miller: []
Lattice Constant Parameters: ['c']

Properties of System: 

Total energy: -62721.105237252974 eV
No. of atoms: 16384 Atoms (Note the number of atoms along each natural direction of the bulk is (16, 16, 16))
Cohesive energy: -3.8281924583284286 eV/Atom

Total Volume: 275741.9107614719 Angstroms^3
Volume per atom: 16.829950607999994 Angstroms^3/Atom

Stress tensor:
[[-3.97161678e-04  1.47073761e-19  4.09156132e-19]
 [ 1.47073761e-19 -3.97161678e-04  1.36259282e-19]
 [ 4.09156132e-19  1.36259282e-19 -3.97161678e-04]]

Bulk Modulus: 184.94027058847462 GPa

```

This program is designed to help obtain the optimal lattice constants for systems that contain more than one lattice constant. For example, for a Au hexagonal close packed (HCP) you will obtain the following plots:



## Where can I find the documentation for LatticeFinder

All the information about this program is found online at [latticefinder.readthedocs.io/en/latest/](https://latticefinder.readthedocs.io/en/latest/). Click the button below to also see the documentation: 

[![Documentation](https://img.shields.io/badge/Docs-click%20here-brightgreen)](https://latticefinder.readthedocs.io/en/latest/)

## About

<div align="center">

| Python | [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/LatticeFinder)](https://docs.python.org/3/) | 
|:----------------------:|:-------------------------------------------------------------:|
| Repositories | [![GitHub release (latest by date)](https://img.shields.io/github/v/release/GardenGroupUO/LatticeFinder)](https://github.com/GardenGroupUO/LatticeFinder) [![PyPI](https://img.shields.io/pypi/v/LatticeFinder)](https://pypi.org/project/LatticeFinder/) [![Conda](https://img.shields.io/conda/v/gardengroupuo/latticefinder)](https://anaconda.org/GardenGroupUO/latticefinder) |
| Documentation | [![Documentation](https://img.shields.io/badge/Docs-click%20here-brightgreen)](https://latticefinder.readthedocs.io/en/latest/) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/GardenGroupUO/Organisms_Jupyter_Examples/main?urlpath=lab) | 
| Tests | [![LGTM Grade](https://img.shields.io/lgtm/grade/python/github/GardenGroupUO/LatticeFinder)](https://lgtm.com/projects/g/GardenGroupUO/LatticeFinder/context:python)
| License | [![Licence](https://img.shields.io/github/license/GardenGroupUO/LatticeFinder)](https://www.gnu.org/licenses/agpl-3.0.en.html) |
| Authors | Geoffrey R. Weal, Dr. Anna L. Garden |
| Group Website | https://blogs.otago.ac.nz/annagarden/ |

</div>




