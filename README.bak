=================================================
clewsy : A set of tools for building CLEWs models
=================================================

Welcome to CLEWsy - the Climate, Land, Energy and Water systems modelling framework tools repository.  The command line scripts in this repository provide tools for building CLEWs models using OSeMOSYS.

Description
===========

**clewsy** is a Python package which provides a command-line interface for building CLEWs models using OSeMOSYS.

Generlized clewsy: python script:

    Country Code 3 letters  == <ccd>
    Region Code 3 letters   == <rgn>
    Filter Code 3 letters   == <flt, rgn, ccd>

    Workflow:

        1- Input Data set preparation:
            [geofilter|canada + remove other technologies] >> 'osemosys_global' >>
                [./data-inp/osemosys-<ccd>/\*.csv]
            GAEZ[Land & Water Database] >> Clustering scripts >> [./data-inp/gaezclstr-<ccd>/\*.csv]

        2- clewsy:
            [./data-inp/gaezclstr-<ccd>/\*.csv + <clewsy parametrization file == CLEWS-CCD.yaml> +
            ./data-inp/osemosys-<ccd>/\*.csv] >>
            python src/build/build.py >>
                ./data-out/gaezclstr-<ccd>/\*.csv
        Supported OutputFormat == MoManI; otoole::Update; otoole::Append

clewsy 1.0 specific:
===================
clewsy 1.0 is Phase 1 of clewsy restructuring.

### Dependencies:
OS baseline required: Ubuntu 20.04LTS w/ stock kernel 5.4.0-136-generic
Note:
   Ubuntu 20.04 installs python3 by default.
   clewsy 1.0 requires python 2.7.18


### Installation:
* Note:
   The following manual installation steps will be automated (scripted) in subsequent releases of clewsy

#### python 2.7.18 packages to be installed:
On the Ubuntu 20.04 LTS console please run the following commands:
1) Install python-yaml
REF: How do I install the yaml package for Python?
   https://stackoverflow.com/questions/14261614/how-do-i-install-the-yaml-package-for-python
   $ apt install python-yaml

2) Install Python Preferred Installer Program (PIP) for python 2.7.18
REF: How to Install Python Pip on Ubuntu 20.04
   https://linuxize.com/post/how-to-install-pip-on-ubuntu-20.04/
   $ mkdir -p /home/python
   $ pushd /home/python
   $ curl https://bootstrap.pypa.io/pip/2.7/get-pip.py --output get-pip.py
   $ sudo python2 get-pip.py

3) Install colorama for python 2.7.18
REF: Python module not found even though "Requirement Already satisfied in Pip"
   https://stackoverflow.com/questions/45345377/python-module-not-found-even-though-requirement-already-satisfied-in-pip
   $ python -m pip install colorama

* Usage:
   $ cd <clewsy_dir>
   $ python src/build/build.py CLEWS-CAN.yaml

# General
Dependencies
------------

*clewsy* requires a number of dependencies, but these should be installed automatically when installing *clewsy*.

Installation
============

Install **clewsy** using pip::

    pip install clewsy


To upgrade **clewsy** using pip::

    pip install clewsy --upgrade

Usage
=====

For instructions of the use of the tool, run the command line

help function::

    clewsy --help

Directory & File naming convention
==================================

Country Code 3 letters  == <ccd>\
Region Code 3 letters   == <rgn>\
Filter Code 3 letters   == <flt, rgn, ccd>

CLEWS-CCD.yaml parametrization file:            CCD == 3 letter alphanumeric Code

clewsy input directory:                         data-inp
                                                Should contain: gaezclstr-<rgn>/\*.csv; osemosys-<flt>/\*.csv

clewsy output directory:                        data-out
                                                Directory is created if not present. gaezclstr-ccd/\*.csv generated here

Contributing
============

New ideas and bugs `should be submitted: <https://github.com/OSeMOSYS/clewsy/issues/new>`_ to the repository Issue Tracker.

Referncing
==========

When using **clewsy** for publications and reports, please cite:
*T. Niet and A. Shivakumar (2020):  clewsy:  Script for building CLEWs models.*

Note
====

This project has been set up using PyScaffold 3.2.3. For details and usage
information on PyScaffold see https://pyscaffold.org/.
