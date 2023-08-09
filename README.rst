# clewsy : A set of tools for building CLEWs models
Welcome to CLEWsy - the Climate, Land, Energy and Water systems modelling framework tools repository.\
**clewsy** is a Python package which provides a command-line interface for building CLEWs models using OSeMOSYS.

## Directory & File naming convention
Country Code 3 letters  == <ccd>\
Region Code 3 letters   == <rgn>\
Filter Code 3 letters   == <flt, rgn, ccd>

CLEWS-CCD.yaml parametrization file:            CCD == 3 letter alphanumeric Code

clewsy input directory:                         data-inp
                                                Should contain: gaezclstr-<rgn>/\*.csv; osemosys-<flt>/\*.csv

clewsy output directory:                        data-out
                                                Directory is created if not present. gaezclstr-ccd/\*.csv generated here

## Workflow:
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

## Dependencies:
OS baseline required: Ubuntu 20.04LTS w/ stock kernel 5.4.0-136-generic\
**Note:**
- clewsy requires python3
- Ubuntu 20.04 installs python3 by default.

## Installation:
**Note:**
   The following manual installation steps will be automated (scripted) in subsequent releases of clewsy

### python packages to be installed:
On the Ubuntu 20.04 LTS console please run the following commands:
1) Install python-yaml\
   **REF:** [How do I install the yaml package for Python?](https://stackoverflow.com/questions/14261614/how-do-i-install-the-yaml-package-for-python)
   ```
   $ apt install python-yaml

2) Install Python Preferred Installer Program (PIP) for python\
   **REF:** [How to Install Python Pip on Ubuntu 20.04](https://linuxize.com/post/how-to-install-pip-on-ubuntu-20.04)
   ```
   $ mkdir -p /home/python
   $ pushd /home/python
   $ curl https://bootstrap.pypa.io/pip/2.7/get-pip.py --output get-pip.py
   $ sudo python2 get-pip.py

3) Install colorama for python\
   **REF:** [Python module not found even though "Requirement Already satisfied in Pip"](https://stackoverflow.com/questions/45345377/python-module-not-found-even-though-requirement-already-satisfied-in-pip)
   ```
   $ python -m pip install colorama

4) Clone & Configure repo
- Get clewsy & parametrize:
   ```
   $ cd <clewsy_dir>
   $ git clone [https://github.com/OSeMOSYS/clewsy.git](https://github.com/OSeMOSYS/clewsy.git)
   $ pushd src/build
   $ chmod a+x clewsy.py    Note: make clewsy.py executable
   $ popd
Parameterize Region/country specific CLEWS-CCD.yaml file. Follow CLEWS-STD.yaml template

- Get otoole & configure:
   ```
   $ git clone [https://github.com/OSeMOSYS/otoole.git](https://github.com/OSeMOSYS/otoole.git)

**Ensure otoole 1.0.0 is installed**
   ```
   $ pip3 install otoole==1.0.0
   ```

## Usage:
### Run clewsy:
   ```
   $ cd <clewsy_dir>\
   $ ./src/build/clewsy.py CLEWS-CCD.yaml\
   **E.g.:**\
    $./src/build/clewsy.py CLEWS-CAN.yaml
   ```
### Run otoole conversion:
   ```
   For csv file output:
   $ otoole --verbose convert csv datafile data-out data-test-KEN.txt config_otoole.yaml
   For xlsx file output:
   $ otoole --verbose convert csv excel data-out data-test-KEN.xlsx config_otoole.yaml
   ```
## Release notes
### clewsy 1.0
clewsy 1.0 is Phase 1 of clewsy restructuring starting [commit id 6a6ef52798caa1ec13bbb92285945881bbb33e62](https://github.com/OSeMOSYS/clewsy/commit/6a6ef52798caa1ec13bbb92285945881bbb33e62)\
Objective is to have clewsy.py be completely parametrized by CLEWS-CCD.yaml.\
Ideally every region/country specific application of clewsy should only adapt CLEWS-CCD.yaml with no changes to clewsy.py

clewsy 1.0 has been tested on linux platforms for both Canada and Kenya.\
Refer examples/CLEWS-CAN.yaml, CLEWS-KEN.yaml

### clewsy 1.x
Objective with further point releases will be to stabilize the code (clewsy.py) and data (CLEWS-CCD.yaml) separation.

### clewsy 2.0
Focus will be for packaged distrubution to run across different operating platforms- Linux, Windows

## Contributing
New ideas and bugs `should be submitted: <https://github.com/OSeMOSYS/clewsy/issues/new>`_ to the repository Issue Tracker.

## Referncing
When using **clewsy** for publications and reports, please cite:
*T. Niet and A. Shivakumar (2020):  clewsy:  Script for building CLEWs models.*

